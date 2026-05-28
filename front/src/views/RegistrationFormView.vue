<script setup>
import { ref } from 'vue'
import { sanitizeEmail, sanitizeUsername } from '@/utils/sanitization'

const email = ref("")
const username = ref("")
const userPassword = ref("")
const errorMessage = ref("")

const checkPasswordStrength = (password) => {
    if (password.length < 8) {
        throw new Error("Password too short")
    }
    const passwordRegex = /^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8}$/
    if (!passwordRegex.test(password)) {
        throw new Error("Your password must have 2 letter in upper case ")
    }
}

const registerUser = () => {
    try {
        checkPasswordStrength(userPassword.value)
        email.value = sanitizeEmail(email.value)
        username.value = sanitizeUsername(username.value)
    } catch (error) {
        errorMessage.value = error.message
        return
    }

    errorMessage.value = ""
    console.log("user tried to register")
    // SEND DATA TO BACKEND !!
}

</script>

<template>
    <h1>Registration Form</h1>

    <div v-if="errorMessage">
        {{ errorMessage }}
    </div>
    <form @submit.prevent="registerUser">
        <div>
            <label>Email</label>
            <input type="text" placeholder="email" v-model="email">
        </div>
        <div>
            <label>Username</label>
            <input type="text" placeholder="username" v-model="username">
        </div>
        <div>
            <label>Password</label>
            <input type="password" placeholder="password" v-model="password">
        </div>
        <button type="submit">btn</button>
    </form>

</template>

<style scoped>

</style>