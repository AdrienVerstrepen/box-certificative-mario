<template>
  <nav class="nav-bar">
    <div class="nav-brand">
      <span>Tour App</span>
    </div>
    <div class="nav-links">
      <router-link to="/" class="nav-link" active-class="active-link">Home</router-link>
      <router-link to="/register" class="nav-link" active-class="active-link">Register</router-link>
      <router-link to="/login" class="nav-link" active-class="active-link">Login</router-link>
      <router-link to="/results" class="nav-link" active-class="active-link">Tours</router-link>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: #1f2937;
  color: white;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.12);
}

.nav-brand span {
  font-weight: 700;
  font-size: 1.1rem;
}

.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  padding: 0.55rem 0.9rem;
  border-radius: 999px;
  color: #e5e7eb;
  text-decoration: none;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-link:hover,
.nav-link.active-link {
  background: #374151;
  color: white;
}
</style>
