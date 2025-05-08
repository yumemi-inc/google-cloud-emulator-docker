#!/bin/bash

echo "Starting delayed initialization..."
date +%s > /tmp/init-started

echo "Sleeping for 10 seconds to simulate long-running initialization..."
sleep 10
echo "Delayed initialization completed!"

# 完了時刻を記録
date +%s > /tmp/delayed-init-completed
