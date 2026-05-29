<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthForm from '@/components/AuthForm.vue'
import FormField from '@/components/FormField.vue'
import { useAuthStore } from '@/stores/auth'
import { sanitizeEmail, sanitizeUsername } from '@/utils/sanitization'

const router = useRouter()
const auth = useAuthStore()
const email = ref('')
const username = ref('')
const userPassword = ref('')
const errorMessage = ref('')

const checkPasswordStrength = (password) => {
  if (password.length < 8) {
    throw new Error('Password too short')
  }
  if (!/(.*[A-Z]){2,}/.test(password)) {
    throw new Error('Password must have at least 2 uppercase letters')
  }
  if (!/(.*[!@#$&*])/.test(password)) {
    throw new Error('Password must contain one special character')
  }
  if (!/(.*[0-9]){2,}/.test(password)) {
    throw new Error('Password must have at least 2 numbers')
  }
  if (!/(.*[a-z]){3,}/.test(password)) {
    throw new Error('Password must contain 3 lowercase letters')
  }
}

const registerUser = async () => {
  try {
    checkPasswordStrength(userPassword.value)
    email.value = sanitizeEmail(email.value)
    username.value = sanitizeUsername(username.value)
  } catch (error) {
    errorMessage.value = error.message
    return
  }

  const result = await auth.register(username.value, email.value, userPassword.value)
  if (!result.success) {
    errorMessage.value = result.error
    return
  }

  errorMessage.value = ''
  router.push({ name: 'Home' })
}
</script>

<template>
  <AuthForm
    title="Create account"
    description="Save your itineraries and retrieve them from any session."
    submit-label="Create account"
    :loading="auth.loading"
    :error-message="errorMessage || auth.errorMsg"
    @submit="registerUser"
  >
    <FormField
      id="register-email"
      v-model="email"
      label="Email"
      type="email"
      placeholder="you@example.com"
      required
    />
    <FormField
      id="register-username"
      v-model="username"
      label="Username"
      placeholder="Your name"
      required
    />
    <FormField
      id="register-password"
      v-model="userPassword"
      label="Password"
      type="password"
      placeholder="8 characters minimum"
      required
    />

    <template #footer>
      Already registered?
      <router-link to="/login">Log in</router-link>
    </template>
  </AuthForm>
</template>
