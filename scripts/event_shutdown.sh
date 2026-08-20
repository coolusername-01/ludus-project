#!/bin/bash
#a script to delete all users and ranges at the end of an event
set -e
for userid in $(ludus users list --json | jq -r '.[] | select(.isAdmin == false) | .userID'); do
    echo "Processing $userid"
    ludus range rm --user "$userid"
    ludus users rm --userid "$userid"
done