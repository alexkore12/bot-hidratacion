#!/bin/bash
# Monitor script for bot-hidratacion
# Usage: ./monitor.sh

set -euo pipefail

echo "🔍 Monitoring bot-hidratacion..."

# Check if the process is running
if pgrep -f "python.*main.py" > /dev/null; then
    echo "✅ Bot process is running"
else
    echo "❌ Bot process is NOT running"
    exit 1
fi

# Check Docker container (if running in Docker)
if command -v docker &> /dev/null; then
    if docker ps --format '{{.Names}}' | grep -q "bot-hidratacion"; then
        echo "✅ Docker container is running"
        docker logs --tail 5 bot-hidratacion 2>/dev/null || true
    fi
fi

# Run health check
echo "🏥 Running health check..."
python3 health_check.py

# Check disk space
DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
echo "💾 Disk usage: ${DISK_USAGE}%"
if [ "${DISK_USAGE}" -gt 90 ]; then
    echo "⚠️ Warning: Disk usage above 90%"
fi

# Check memory usage
MEMORY_USAGE=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
echo "🧠 Memory usage: ${MEMORY_USAGE}%"
if [ "${MEMORY_USAGE}" -gt 90 ]; then
    echo "⚠️ Warning: Memory usage above 90%"
fi

echo "✅ Monitoring complete"