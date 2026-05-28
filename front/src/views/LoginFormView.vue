<script setup>
import { ref } from vue

const userEmail = ref('')
const userPassword = ref('')
const errorMessage = ref("")

const sanitizeEmail = (email) => {
    const trimmedEmail = email.trim().toLowerCase()
    const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    if (emailRegex.test(trimmedEmail)) {
        userEmail.value = trimmedEmail;
    } else {
        throw new Error("Invalid E-mail")
    }
}

const handleLogin = () => {
    try {
        sanitizeEmail(userEmail.value)
    } catch (error) {
        errorMessage.value = error.message
    }

    const user = {
        mail: userEmail,
        clearPassword: userPassword
    }
    console.log('Logging in with email:', email, 'and password:', password)
    // Send request to back-end
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
