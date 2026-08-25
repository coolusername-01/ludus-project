#!/bin/bash
#a script to automate event setup with personalisation of ranges using flags
set -e
while getopts "n:r:" opt; do
  case $opt in
	n) num_ranges="$OPTARG" ;;
	r) range="$OPTARG" ;;
	\?) echo "Invalid option: -$OPTARG" ;;
  esac
done

##looking up each LAB id to find next available id
i=1
while ludus users list all | grep -q "LAB$i"; do
    ((i++))
done
end=$((i + num_ranges - 1))

for (( ; i <= end; i++)); do
    ludus users add \
        --userid "LAB$i" \
        --name "Player$i" \
        --email "lab$i@example.invalid" \
        --password "password$i"
    echo "user has been added"    
    ludus range config set -r "LAB$1" -f "$range"
    echo "range config set"
    ludus range deploy \
        --user "LAB$i"
    echo "range $i has deployed"
done