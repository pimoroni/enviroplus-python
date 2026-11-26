"""Check example MQTT callbacks using a real Paho client and local peer."""
import importlib.util
import json
import socket
import sys
import threading
import warnings
from pathlib import Path
from unittest.mock import Mock

import paho.mqtt.client as mqtt
import pytest


def test_mqtt_example(monkeypatch, capsys):
    for name in ("st7735", "bme280", "pms5003", "enviroplus", "ltr559",
                 "fonts", "fonts.ttf", "PIL", "PIL.Image", "PIL.ImageDraw",
                 "PIL.ImageFont", "smbus2"):
        monkeypatch.setitem(sys.modules, name, Mock())
    spec = importlib.util.spec_from_file_location("mqtt_all", Path(__file__).parents[1] / "examples/mqtt-all.py")
    example = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example)
    connected = threading.Event()
    received = threading.Event()
    clients = []
    errors = []
    packets = []
    real_client = mqtt.Client

    def client(*args, **kwargs):
        instance = real_client(*args, **kwargs)
        clients.append(instance)
        return instance

    def packet(conn):
        header = conn.recv(1)
        length = 0
        shift = 0
        while True:
            digit = conn.recv(1)[0]
            length |= (digit & 127) << shift
            if digit < 128:
                break
            shift += 7
        body = b""
        while len(body) < length:
            chunk = conn.recv(length - len(body))
            if not chunk:
                raise EOFError("short MQTT packet")
            body += chunk
        return header[0], body

    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        listener.settimeout(5)

        def peer():
            try:
                with listener.accept()[0] as conn:
                    conn.settimeout(5)
                    assert packet(conn)[0] == 0x10
                    conn.sendall(b"\x20\x02\x00\x00")
                    connected.set()
                    packets.append(packet(conn))
                    received.set()
            except (OSError, EOFError, IndexError, AssertionError) as error:
                errors.append(error)
                connected.set()
                received.set()

        thread = threading.Thread(target=peer, daemon=True)
        thread.start()
        monkeypatch.setattr(mqtt, "Client", client)
        monkeypatch.setattr(sys, "argv", ["mqtt-all.py", "--broker", "127.0.0.1", "--port", str(listener.getsockname()[1]), "--interval", "0"])
        monkeypatch.setattr(example, "get_serial_number", lambda: "test-pi")
        monkeypatch.setattr(example, "check_wifi", lambda: True)
        monkeypatch.setattr(example, "display_status", lambda *_: None)
        example.SerialTimeoutError = TimeoutError
        example.PMS5003.side_effect = TimeoutError
        count = 0

        def readings(_):
            nonlocal count
            count += 1
            if count > 1:
                assert received.wait(5)
                raise KeyboardInterrupt
            assert connected.wait(5)
            return {"temperature": 21}

        monkeypatch.setattr(example, "read_bme280", readings)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", DeprecationWarning)
                with pytest.raises(KeyboardInterrupt):
                    example.main()
        finally:
            for instance in clients:
                instance.disconnect()
                instance.loop_stop()
            thread.join(6)
    assert not errors
    assert not thread.is_alive()
    assert packets[0][0] == 0x31  # retained QoS 0 publish
    body = packets[0][1]
    topic_length = int.from_bytes(body[:2], "big")
    assert body[2:2 + topic_length] == b"enviroplus"
    assert json.loads(body[2 + topic_length:]) == {"temperature": 21, "serial": "test-pi"}
    output = capsys.readouterr().out
    assert "connected OK" in output
    assert "mid: 1" in output
