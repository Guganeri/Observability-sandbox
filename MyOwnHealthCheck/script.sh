#!/bin/bash

check_service() {
    command="curl -s -o /dev/null -w '%{http_code}' https://httpbin.org/status/200"
    timestamp=$(date --iso-8601=seconds)
    
    result=$($command)
    status_code=$?

    if [ $status_code -eq 0 ]; then
        if [ "$result" = "'200'" ]; then
            status="success"
            error_message="null"
        else
            status="error"
            error_message="Unexpected status code: $result"
        fi
    else
        status="error"
        result="null"
        error_message="Failed to execute command: $command"
    fi
    
    log=$(cat <<EOF
{
    "timestamp": "$timestamp",
    "command": "$command",
    "status": "$status",
    "output": "$result",
    "error_message": "$error_message"
}
EOF
)

    echo "$log" >> service_check_log.json
}

check_service
