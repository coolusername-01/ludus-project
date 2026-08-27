#!/bin/bash
set -e
iptables -t nat -A PREROUTING \
  -i enp4s0 \
  -p tcp \
  --dport 8080 \
  -j DNAT \
  --to-destination 10.1.10.10:80

iptables -A FORWARD \
  -i enp4s0 \
  -o vmbr1000 \
  -p tcp \
  -d 10.1.10.10 \
  --dport 80 \
  -j ACCEPT

iptables -A FORWARD \
  -i vmbr1000 \
  -o enp4s0 \ 
  -p tcp \
  -s 10.1.10.10 \
  --sport 80 \
  -m conntrack \
  --ctstate ESTABLISHED,RELATED \
  -j ACCEPT

iptables -t nat -A POSTROUTING \
  -o vmbr1000 \
  -p tcp \
  -d 10.1.10.10 \
  --dport 80 \
  -j MASQUERADE