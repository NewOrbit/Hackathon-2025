#!/bin/bash

echo "🚀 Starting DeepseekTravels MCP Servers..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ uv is not installed. Please install it first.${NC}"
    echo "Install with: pip install uv"
    exit 1
fi

# Navigate to the MCP directory
MCP_DIR="../src/mcp"

if [ ! -d "$MCP_DIR" ]; then
    echo -e "${RED}❌ MCP directory not found at $MCP_DIR${NC}"
    echo "Make sure you're running this from the deepseek-travels-chat directory"
    exit 1
fi

echo -e "${YELLOW}Starting MCP servers in background...${NC}"
echo ""

# Function to start a server
start_server() {
    local server_name=$1
    local port=$2
    
    echo -e "${YELLOW}Starting $server_name server on port $port...${NC}"
    
    cd "$MCP_DIR/$server_name-mcp"
    
    if [ ! -f "main.py" ]; then
        echo -e "${RED}❌ main.py not found in $server_name-mcp${NC}"
        return 1
    fi
    
    # Start server in background
    nohup uv run main.py > "../../../deepseek-travels-chat/logs/$server_name.log" 2>&1 &
    echo $! > "../../../deepseek-travels-chat/logs/$server_name.pid"
    
    echo -e "${GREEN}✅ $server_name server started (PID: $!)${NC}"
    cd - > /dev/null
}

# Create logs directory
mkdir -p logs

# Start all servers
start_server "weather" 8009
start_server "attractions" 8008  
start_server "requirements" 8010
start_server "booking" 8011

echo ""
echo -e "${GREEN}🎉 All MCP servers started!${NC}"
echo ""
echo "Server status:"
echo "• Weather: http://127.0.0.1:8009"
echo "• Attractions: http://127.0.0.1:8008"
echo "• Travel Requirements: http://127.0.0.1:8010"
echo "• Booking: http://127.0.0.1:8011"
echo ""
echo "Logs are available in the logs/ directory"
echo "To stop servers, run: ./stop-servers.sh"
echo ""
echo "Now start the Vue app with: npm run dev"