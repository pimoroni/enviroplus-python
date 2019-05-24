printf "\nOutstanding substitutions:\n"
grep -Irn --color "{{[A-Z:]*}}"

printf "\nOutstanding directory renames:\n"
find . -regex ".*{{[A-Z]*}}"
