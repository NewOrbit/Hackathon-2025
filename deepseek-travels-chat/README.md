# DeepseekTravels Chat App

A modern Vue3 + TypeScript chat interface for the DeepseekTravels intelligent packing assistant. This app provides a user-friendly web interface for the MCP-based travel packing system.

## Features

🧳 **Intelligent Packing Lists** - Generate smart packing recommendations based on destination, weather, and activities
🌦️ **Weather Integration** - Real-time weather forecasts to inform packing decisions  
✈️ **Travel Requirements** - Visa, documentation, and security restriction checking
🏨 **Booking Suggestions** - Flight, hotel, and activity recommendations
📱 **Mobile-Friendly** - Responsive design optimized for all devices
🎯 **Keep-It-Simple Mode** - Quick, printable checklists for fast planning

## Quick Start

### Prerequisites

- Node.js 20.19+ (or compatible version)
- The MCP servers from the parent project running

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production  
npm run build
```

### Full Stack Setup

The app now uses a FastAPI backend that replicates the Jupyter notebook functionality. Here's how to run everything:

**Step 1: Start MCP Servers**
```bash
# Start all MCP servers (run this first!)
./start-servers.sh
```

**Step 2: Start Backend API**
```bash
# Start the FastAPI backend server
./start-backend.sh
```

**Step 3: Start Frontend**
```bash
# Start the Vue3 frontend (in a new terminal)
npm run dev
```

The app will show server connection status in the header - all should be green when working properly.

## Architecture

### Full Stack Components

**Frontend (Vue3 + TypeScript)**
- **ChatInterface.vue** - Main chat component with message history and input
- **Message rendering** - Supports markdown-like formatting  
- **Typing indicators** - Shows when the assistant is processing
- **Server status** - Real-time connection monitoring

**Backend (FastAPI + Python)**
- **main.py** - FastAPI server with LangChain agent from notebook
- **Agent setup** - Azure OpenAI integration with MCP tools
- **Session management** - Persistent conversation memory
- **Health monitoring** - Real-time MCP server status checks

**Services & Integration**
- **chatService.ts** - Frontend HTTP client for FastAPI backend
- **MCP Integration** - LangChain MCP adapters for tool calling
- **CORS handling** - Proper cross-origin request support

## Usage Examples

Try these example queries in the chat:

- "What should I pack for a week in Tokyo in November?"
- "Beach weekend in Lisbon - keep it simple!"
- "Business trip to Singapore, 28L backpack, flying ANA"
- "Patagonia hiking for 10 days, 65L pack, 20kg limit"
- "What's the weather like in Paris?"
- "Do I need a visa for Japan?"

## Development

### Project Structure

```
deepseek-travels-chat/
├── backend/                # FastAPI Backend
│   ├── main.py            # FastAPI app with LangChain agent
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables (copied from agent)
├── src/                   # Vue3 Frontend
│   ├── components/        # Vue components
│   │   └── ChatInterface.vue
│   ├── services/         # HTTP client services
│   │   └── chatService.ts
│   ├── composables/      # Vue composables
│   │   └── useServerStatus.ts
│   ├── types/           # TypeScript interfaces
│   │   └── chat.ts
│   └── App.vue          # Root component
├── start-servers.sh      # Start all MCP servers
├── start-backend.sh      # Start FastAPI backend
├── stop-servers.sh       # Stop MCP servers
└── package.json         # Frontend dependencies
```

### Key Technologies

- **Vue 3** - Composition API with `<script setup>`
- **TypeScript** - Full type safety
- **Vite** - Fast development and building
- **CSS3** - Modern styling with gradients and animations

### Environment Variables

Configure MCP server URLs in `.env`:

```env
VITE_WEATHER_MCP_URL=http://127.0.0.1:8009
VITE_ATTRACTIONS_MCP_URL=http://127.0.0.1:8008
VITE_TRAVEL_REQUIREMENTS_MCP_URL=http://127.0.0.1:8010
VITE_BOOKING_MCP_URL=http://127.0.0.1:8011
```

## Production Deployment

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Deploy dist/ folder to your hosting platform
```

## Troubleshooting

### MCP Servers Not Connecting

1. Verify all MCP servers are running on correct ports
2. Check firewall/CORS settings
3. Review server logs for errors
4. Ensure servers are accessible at configured URLs

### Chat Not Responding

1. Check browser console for JavaScript errors
2. Verify MCP server endpoints are responding
3. Test individual server health endpoints
4. Review network tab for failed requests

## Contributing

This chat app was converted from the original Jupyter notebook (`packing_list.ipynb`) to provide a modern web interface. Key conversions:

- **Agent logic** → Service layer with intent parsing
- **MCP integration** → HTTP client with error handling  
- **Interactive cells** → Real-time chat interface
- **Notebook output** → Formatted message responses

## License

Part of the NewOrbit Hackathon 2025 project.
