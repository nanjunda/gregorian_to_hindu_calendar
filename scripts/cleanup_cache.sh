#!/bin/bash
# Hindu Panchanga Image Cache Cleanup Script
# Deletes generated images older than 24 hours to protect user privacy.

CACHE_DIRS=("/opt/panchanga/static/skyshots" "/opt/panchanga/static/solar_systems")

echo "🧹 Starting cache cleanup at $(date)"

for DIR in "${CACHE_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        echo "   Checking $DIR..."
        # Delete files older than 15 minutes
        find "$DIR" -name "*.png" -type f -mmin +15 -delete -print
    fi
done

echo "✅ Cleanup complete."
