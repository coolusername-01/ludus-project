#a script to automate event setup with personalisation of ranges using flags

while getopts "n:r:" opt; do
  case $opt in
	n) num_ranges="$OPTARG" ;;
	r) range="$OPTARG" ;;
	\?) echo "Invalid option: -$OPTARG" ;;
  esac
done

for i in $(seq 1 "$num_ranges"); do
    ludus users add \
        --userid "LAB$i" \
        --name "Player$i" \
        --email "lab$i@example.invalid" \
        --password "password$i"
    ludus range create \
        --name "range$i" \
        --user "LAB$i"
    ludus range config set "$range"
    ludus range deploy \
        --user "LAB$i"
done