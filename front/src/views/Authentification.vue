<script setup>


const handleLogin = () => {
  // Here you would typically handle the login logic, such as sending a request to your backend
  console.log('Logging in with email:', email, 'and password:', password);
};
</script>

<template>
  <div class="authentification">
    <h1>Connection</h1>
    <p>Please enter your credentials to log in.</p>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Log In</button>
    </form>
  </div>

</template>

<style scoped>
</style>