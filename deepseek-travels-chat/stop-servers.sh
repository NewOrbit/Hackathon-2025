#!/bin/bash

echo "🛑 Stopping DeepseekTravels MCP Servers..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to stop a server
stop_server() {
    local server_name=$1
    local pid_file="logs/$server_name.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            echo -e "${GREEN}✅ Stopped $server_name server (PID: $pid)${NC}"
        else
            echo -e "${YELLOW}⚠️ $server_name server was not running${NC}"
        fi
        rm -f "$pid_file"
    else
        echo -e "${YELLOW}⚠️ No PID file found for $server_name${NC}"
    fi
}

# Stop all servers
stop_server "weather"
stop_server "attractions"
stop_server "travel-requirements" 
stop_server "booking"

echo ""
echo -e "${GREEN}🎉 All MCP servers stopped!${NC}"

# Clean up logs directory if empty
if [ -d "logs" ] && [ -z "$(ls -A logs)" ]; then
    rmdir logs
    echo "Cleaned up empty logs directory"
fi