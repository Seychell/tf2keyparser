#!/bin/bash

chmod +x "$0"

while true; do
  python main.py
  echo "Restarting in 5 minutes..."
  sleep 300
done