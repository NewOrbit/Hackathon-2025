<template>
  <div class="chat-container">
    <header class="chat-header">
      <div class="logo">
        <h1>🧳 DeepseekTravels</h1>
        <p>Your intelligent travel packing assistant</p>
      </div>
    </header>

    <div class="chat-messages" ref="messagesContainer">
      <div class="welcome-message" v-if="messages.length === 0">
        <h2>Welcome to DeepseekTravels! 🌍</h2>
        <p>I'm your intelligent packing assistant. I can help you:</p>
        <ul>
          <li>🌦️ Generate weather-aware packing lists</li>
          <li>✈️ Check airline baggage restrictions</li>
          <li>📋 Optimize for capacity and weight limits</li>
          <li>🏨 Suggest relevant bookings</li>
          <li>📝 Create simple, printable checklists</li>
        </ul>
        <div class="example-prompts">
          <h3>Try asking:</h3>
          <button 
            v-for="example in examplePrompts" 
            :key="example"
            @click="sendMessage(example)"
            class="example-prompt"
          >
            {{ example }}
          </button>
        </div>
      </div>

      <div 
        v-for="message in messages" 
        :key="message.id"
        :class="['message', { 'user-message': message.isUser, 'assistant-message': !message.isUser }]"
      >
        <div class="message-content">
          <div class="message-text" v-html="formatMessage(message.content)"></div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>
        <div v-if="message.isLoading" class="typing-indicator">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
      </div>
    </div>

    <div class="chat-input-container">
      <form @submit.prevent="handleSubmit" class="chat-input-form">
        <input
          v-model="currentInput"
          type="text"
          placeholder="Ask about packing for your next trip..."
          :disabled="isLoading"
          class="chat-input"
          ref="inputRef"
        />
        <button 
          type="submit" 
          :disabled="isLoading || !currentInput.trim()"
          class="send-button"
        >
          <span v-if="isLoading">⏳</span>
          <span v-else>🚀</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue'
import type { ChatMessage, MCPServerConfig } from '@/types/chat'

const messages = ref<ChatMessage[]>([])
const currentInput = ref('')
const isLoading = ref(false)
const messagesContainer = ref<HTMLElement>()
const inputRef = ref<HTMLInputElement>()

const examplePrompts = [
  "What should I pack for a week in Tokyo in November?",
  "Beach weekend in Lisbon - keep it simple!",
  "Business trip to Singapore, 28L backpack",
  "Patagonia hiking for 10 days, 65L pack"
]

const formatMessage = (content: string) => {
  // Convert markdown-like formatting to HTML
  return content
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
    .replace(/• /g, '• ')
}

const formatTime = (timestamp: Date) => {
  return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async (text: string = currentInput.value) => {
  if (!text.trim() || isLoading.value) return

  const userMessage: ChatMessage = {
    id: `user-${Date.now()}`,
    content: text.trim(),
    isUser: true,
    timestamp: new Date()
  }

  messages.value.push(userMessage)
  currentInput.value = ''
  isLoading.value = true

  // Add loading message
  const loadingMessage: ChatMessage = {
    id: `assistant-${Date.now()}`,
    content: '',
    isUser: false,
    timestamp: new Date(),
    isLoading: true
  }
  messages.value.push(loadingMessage)

  await scrollToBottom()

  try {
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text.trim() })
    }).then(res => {
      if (!res.ok) throw new Error(`Server error: ${res.statusText}`)
      return res.json()
    }).then(data => data.response as string);
    
    // Remove loading message and add actual response
    messages.value.pop()
    
    const responseMessage: ChatMessage = {
      id: `assistant-${Date.now()}`,
      content: response,
      isUser: false,
      timestamp: new Date()
    }
    
    messages.value.push(responseMessage)
  } catch (error) {
    // Remove loading message and add error message
    messages.value.pop()
    
    const errorMessage: ChatMessage = {
      id: `error-${Date.now()}`,
      content: `❌ Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}. Please make sure the MCP servers are running.`,
      isUser: false,
      timestamp: new Date()
    }
    
    messages.value.push(errorMessage)
  } finally {
    isLoading.value = false
    await scrollToBottom()
    inputRef.value?.focus()
  }
}

const handleSubmit = () => {
  sendMessage()
}

onMounted(() => {
  inputRef.value?.focus()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 800px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.logo h1 {
  margin: 0;
  color: #2d3748;
  font-size: 1.5rem;
}

.logo p {
  margin: 0;
  color: #718096;
  font-size: 0.875rem;
}

.server-status {
  display: flex;
  gap: 0.5rem;
}

.status-indicator {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.75rem;
  color: white;
}

.status-indicator.connected {
  background-color: #48bb78;
}

.status-indicator.disconnected {
  background-color: #ed8936;
}

.status-indicator.error {
  background-color: #f56565;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.welcome-message {
  background: rgba(255, 255, 255, 0.95);
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.welcome-message h2 {
  margin-top: 0;
  color: #2d3748;
}

.welcome-message ul {
  color: #4a5568;
  margin: 1rem 0;
}

.example-prompts {
  margin-top: 1.5rem;
}

.example-prompts h3 {
  margin-bottom: 0.5rem;
  color: #2d3748;
  font-size: 1rem;
}

.example-prompt {
  display: block;
  width: 100%;
  text-align: left;
  background: #edf2f7;
  border: none;
  padding: 0.75rem 1rem;
  margin: 0.25rem 0;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #2d3748;
}

.example-prompt:hover {
  background: #e2e8f0;
}

.message {
  display: flex;
  max-width: 80%;
}

.user-message {
  align-self: flex-end;
  justify-content: flex-end;
}

.assistant-message {
  align-self: flex-start;
  justify-content: flex-start;
}

.message-content {
  background: rgba(255, 255, 255, 0.95);
  padding: 1rem 1.25rem;
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 100%;
}

.user-message .message-content {
  background: #4299e1;
  color: white;
  border-bottom-right-radius: 0.25rem;
}

.assistant-message .message-content {
  border-bottom-left-radius: 0.25rem;
}

.message-text {
  line-height: 1.5;
  word-wrap: break-word;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 0.5rem;
  text-align: right;
}

.user-message .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 0.5rem;
}

.dot {
  width: 0.5rem;
  height: 0.5rem;
  background: #a0aec0;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.chat-input-container {
  padding: 1rem 2rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.chat-input-form {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.chat-input {
  flex: 1;
  padding: 0.875rem 1.25rem;
  border: 2px solid #e2e8f0;
  border-radius: 2rem;
  font-size: 1rem;
  background: white;
  transition: border-color 0.2s;
}

.chat-input:focus {
  outline: none;
  border-color: #4299e1;
}

.chat-input:disabled {
  background: #f7fafc;
  cursor: not-allowed;
}

.send-button {
  width: 3rem;
  height: 3rem;
  border: none;
  border-radius: 50%;
  background: #4299e1;
  color: white;
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover:not(:disabled) {
  background: #3182ce;
  transform: scale(1.05);
}

.send-button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .chat-header {
    padding: 1rem;
  }
  
  .chat-messages {
    padding: 0.75rem;
  }
  
  .message {
    max-width: 90%;
  }
  
  .welcome-message {
    padding: 1.5rem;
  }
  
  .chat-input-container {
    padding: 1rem;
  }
}
</style>