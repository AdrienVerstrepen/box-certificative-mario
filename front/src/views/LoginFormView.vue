<script setup>
import { ref } from 'vue'
import { sanitizeEmail } from '@/utils/sanitization'
import { sendLoginRequest } from '@/api/backendApiRequests'

const userEmail = ref('')
const userPassword = ref('')
const errorMessage = ref("")

const handleLogin = () => {
    try {
        sanitizeEmail(userEmail.value)
    } catch (error) {
        errorMessage.value = error.message
    }

    console.log('Logging in with email:', email, 'and password:', password)
    sendLoginRequest(userEmail.value, userPassword.value)
};

</script>

<template>
    <div class="authentification">
        <h1>Connection</h1>
        <p>Please enter your credentials to log in.</p>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="userEmail" required />
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="userPassword" required />
            </div>
            <button type="submit">Log In</button>
        </form>
    </div>

</template>

<style scoped>
</style>
