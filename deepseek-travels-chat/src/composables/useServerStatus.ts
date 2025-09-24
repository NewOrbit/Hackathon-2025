import { ref, reactive } from 'vue'
import type { MCPServerConfig } from '@/types/chat'
import { useChatService } from '@/services/chatService'

const serverStatus = reactive<MCPServerConfig[]>([
  { name: 'API', url: 'http://127.0.0.1:8000', status: 'disconnected' },
  { name: 'Weather', url: 'http://127.0.0.1:8009', status: 'disconnected' },
  { name: 'Attractions', url: 'http://127.0.0.1:8008', status: 'disconnected' },
  { name: 'Travel-Req', url: 'http://127.0.0.1:8010', status: 'disconnected' },
  { name: 'Booking', url: 'http://127.0.0.1:8011', status: 'disconnected' }
])

const isChecking = ref(false)

export const useServerStatus = () => {
  const chatService = useChatService()

  const checkServerStatus = async () => {
    if (isChecking.value) return
    
    isChecking.value = true
    
    try {
      // Check main API server
      const apiServer = serverStatus.find(s => s.name === 'API')
      if (apiServer) {
        try {
          await chatService.getHealthStatus()
          apiServer.status = 'connected'
        } catch (error) {
          apiServer.status = 'disconnected'
        }
      }

      // Check MCP servers through the API
      try {
        const mcpStatus = await chatService.getServerStatus()
        
        for (const server of serverStatus) {
          if (server.name === 'API') continue // Already checked
          
          const serverKey = server.name.toLowerCase().replace('-', '_')
          const mcpServerInfo = mcpStatus.servers[serverKey]
          
          if (mcpServerInfo) {
            server.status = mcpServerInfo.status as 'connected' | 'disconnected' | 'error'
          } else {
            server.status = 'disconnected'
          }
        }
      } catch (error) {
        // If we can't get MCP status, mark all as disconnected except API
        for (const server of serverStatus) {
          if (server.name !== 'API') {
            server.status = 'disconnected'
          }
        }
      }
    } catch (error) {
      console.error('Error checking server status:', error)
      // Mark all as disconnected on error
      for (const server of serverStatus) {
        server.status = 'disconnected'
      }
    }
    
    isChecking.value = false
  }

  const getServerByName = (name: string) => {
    return serverStatus.find(server => server.name === name)
  }

  const areAllServersConnected = () => {
    return serverStatus.every(server => server.status === 'connected')
  }

  const getConnectionSummary = () => {
    const connected = serverStatus.filter(server => server.status === 'connected').length
    const total = serverStatus.length
    return { connected, total, allConnected: connected === total }
  }

  return {
    serverStatus,
    isChecking,
    checkServerStatus,
    getServerByName,
    areAllServersConnected,
    getConnectionSummary
  }
}