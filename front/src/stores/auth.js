import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { sendLoginRequest, sendRegistrationRequest } from '@/api/backendApiRequests'

export const useAuthStore = defineStore('auth', () => {
  // Load initial state from localStorage if available
  const storedUser = localStorage.getItem('user')
  const user = ref(storedUser ? JSON.parse(storedUser) : null)
  const loading = ref(false)
  const errorMsg = ref(null)

  const isAuthenticated = computed(() => !!user.value)

  async function login(email, password) {
    loading.value = true
    errorMsg.value = null
    try {
      const data = await sendLoginRequest(email, password)
      if (data && data.success) {
        user.value = data.user
        localStorage.setItem('user', JSON.stringify(data.user))
        return { success: true }
      } else {
        throw new Error(data?.error || "Login failed")
      }
    } catch (err) {
      errorMsg.value = err.message || "An unknown error occurred"
      return { success: false, error: errorMsg.value }
    } finally {
      loading.value = false
    }
  }

  async function register(username, email, password) {
    loading.value = true
    errorMsg.value = null
    try {
      const data = await sendRegistrationRequest(username, email, password)
      if (data && data.success) {
        user.value = data.user
        localStorage.setItem('user', JSON.stringify(data.user))
        return { success: true }
      } else {
        throw new Error(data?.error || "Registration failed")
      }
    } catch (err) {
      errorMsg.value = err.message || "An unknown error occurred"
      return { success: false, error: errorMsg.value }
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    errorMsg.value = null
    localStorage.removeItem('user')
  }

  return {
    user,
    loading,
    errorMsg,
    isAuthenticated,
    login,
    register,
    logout
  }
})
