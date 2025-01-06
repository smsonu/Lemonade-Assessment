#Write a script to restart the Laravel backend service if CPU usage exceeds 80%.

#!/bin/bash
THRESHOLD=80
SERVICE_NAME="laravel-backend"

while true; do
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
    CPU_INT=${CPU_USAGE%.*}

    if [ "$CPU_INT" -gt "$THRESHOLD" ]; then
        echo "$(date): CPU usage is $CPU_USAGE%. Restarting $SERVICE_NAME..."
        systemctl restart $SERVICE_NAME
    fi
    sleep 10
done
