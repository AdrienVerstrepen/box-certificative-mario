<template>
  <nav class="nav-bar">
    <div class="nav-brand">
      <router-link to="/">Travel Planner</router-link>
    </div>
    <div class="nav-links">
      <router-link to="/" class="nav-link" active-class="active-link">Plan</router-link>
      <router-link to="/results" class="nav-link" active-class="active-link">Tours</router-link>
      <router-link v-if="!auth.isAuthenticated" to="/login" class="nav-link" active-class="active-link">
        Login
      </router-link>
      <router-link v-if="!auth.isAuthenticated" to="/register" class="nav-link" active-class="active-link">
        Register
      </router-link>
      <button v-else class="nav-link nav-button" type="button" @click="auth.logout()">
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<style scoped>
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  min-height: 4.5rem;
  padding: 0.9rem max(1rem, calc((100vw - 1120px) / 2));
  background: rgba(255, 255, 255, 0.92);
  border-bottom: 1px solid #dbe3ea;
  color: #0f172a;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}

.nav-brand a {
  color: #0f172a;
  font-weight: 800;
  font-size: 1.15rem;
  text-decoration: none;
}

.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  min-height: 2.35rem;
  padding: 0.55rem 0.9rem;
  border-radius: 8px;
  color: #475569;
  text-decoration: none;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.nav-button {
  border: 0;
  background: transparent;
  cursor: pointer;
}

.nav-link:hover,
.nav-link.active-link {
  background: #e0f2f1;
  color: #0f766e;
}

@media (max-width: 640px) {
  .nav-bar {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
