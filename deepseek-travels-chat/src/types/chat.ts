export interface ChatMessage {
  id: string
  content: string
  isUser: boolean
  timestamp: Date
  isLoading?: boolean
}

export interface WeatherData {
  location: string
  temperature: number
  description: string
  humidity: number
  windSpeed: number
  forecast?: DailyForecast[]
}

export interface DailyForecast {
  date: string
  temperatureMax: number
  temperatureMin: number
  description: string
  precipitation: number
}

export interface TravelRequirements {
  destination: string
  visaRequired: boolean
  vaccinations: string[]
  securityRestrictions: string[]
  baggageRules: string[]
}

export interface PackingItem {
  name: string
  category: string
  quantity: number
  weight: number
  volume: number
  priority: 'essential' | 'recommended' | 'optional'
  reason: string
}

export interface PackingListRequest {
  destination: string
  duration: number
  activities: string[]
  capacityLiters: number
  maxWeightKg: number
  airline?: string
  keepItSimple?: boolean
}

export interface PackingListResponse {
  items: PackingItem[]
  totalWeight: number
  totalVolume: number
  capacityUsed: number
  warnings: string[]
  suggestions: string[]
}

export interface BookingOption {
  type: 'flight' | 'hotel' | 'activity'
  title: string
  description: string
  price: number
  currency: string
  provider: string
  bookingUrl?: string
}

export interface MCPServerConfig {
  name: string
  url: string
  status: 'connected' | 'disconnected' | 'error'
}