#!/bin/bash

# Default to index if not set (though docker-compose sets it)
TYPE="${BOT_TYPE:-index}"

if [ "$TYPE" = "file" ]; then
    echo "Starting File Bot..."
    python3 file_bot.py
else
    echo "Starting Index Bot..."
    python3 index_bot.py
fi
