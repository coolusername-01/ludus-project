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

for i in $(seq 1 "$num_ranges"); do
    ludus users add \
        --userid "LAB$i" \
        --name "Player$i" \
        --email "lab$i@example.invalid" \
        --password "password$i"
    echo "user has been added"    
    ludus range create \
        --name "range$i" \
        --users "LAB$i" \
        -r "range$1"
    echo "range has been created"
    ludus range config set -f "$range"
    echo "range config set"
    ludus range deploy \
        --user "LAB$i"
    echo "range $i has deployed"
done