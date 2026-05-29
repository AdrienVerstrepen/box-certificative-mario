<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthForm from '@/components/AuthForm.vue'
import FormField from '@/components/FormField.vue'
import { useAuthStore } from '@/stores/auth'
import { sanitizeEmail } from '@/utils/sanitization'

const router = useRouter()
const auth = useAuthStore()
const userEmail = ref('')
const userPassword = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  try {
    userEmail.value = sanitizeEmail(userEmail.value)
  } catch (error) {
    errorMessage.value = error.message
    return
  }

  const result = await auth.login(userEmail.value, userPassword.value)
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
    title="Login"
    description="Access your saved tours and continue planning."
    submit-label="Log in"
    :loading="auth.loading"
    :error-message="errorMessage || auth.errorMsg"
    @submit="handleLogin"
  >
    <FormField
      id="login-email"
      v-model="userEmail"
      label="Email"
      type="email"
      placeholder="you@example.com"
      required
    />
    <FormField
      id="login-password"
      v-model="userPassword"
      label="Password"
      type="password"
      placeholder="Your password"
      required
    />

    <template #footer>
      No account yet?
      <router-link to="/register">Create one</router-link>
    </template>
  </AuthForm>
</template>
