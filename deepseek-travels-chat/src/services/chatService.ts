import type { 
  PackingListRequest, 
  PackingListResponse, 
  WeatherData, 
  TravelRequirements, 
  BookingOption 
} from '@/types/chat'

export class ChatService {
  private apiBaseUrl = 'http://127.0.0.1:8000'
  private sessionId = 'default'

  async sendMessage(message: string): Promise<string> {
    try {
      const response = await fetch(`${this.apiBaseUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
          session_id: this.sessionId
        })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `API returned ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      return data.response
    } catch (error) {
      console.error('Error calling DeepseekTravels API:', error)
      throw new Error(`Failed to process your request: ${error instanceof Error ? error.message : 'Unknown error'}`)
    }
  }

  async getServerStatus(): Promise<any> {
    try {
      const response = await fetch(`${this.apiBaseUrl}/servers/status`)
      if (!response.ok) {
        throw new Error(`Status check failed: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('Error checking server status:', error)
      throw error
    }
  }

  async getHealthStatus(): Promise<any> {
    try {
      const response = await fetch(`${this.apiBaseUrl}/health`)
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('Error checking health:', error)
      throw error
    }
  }

  async clearSession(): Promise<void> {
    try {
      const response = await fetch(`${this.apiBaseUrl}/sessions/${this.sessionId}`, {
        method: 'DELETE'
      })
      if (!response.ok) {
        console.warn('Failed to clear session:', response.status)
      }
    } catch (error) {
      console.error('Error clearing session:', error)
    }
  }

  setSessionId(sessionId: string): void {
    this.sessionId = sessionId
  }

  getSessionId(): string {
    return this.sessionId
  }
}

// Create a singleton instance
let chatServiceInstance: ChatService | null = null

export const useChatService = () => {
  if (!chatServiceInstance) {
    chatServiceInstance = new ChatService()
  }
  return chatServiceInstance
}