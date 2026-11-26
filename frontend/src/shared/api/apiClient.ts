import axios from 'axios'

// La URL del backend viene de VITE_API_URL, en local apunta a uvicorn
const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_URL.replace(/\/$/, ''),
  timeout: 20000,
  headers: { 'Content-Type': 'application/json' },
})
