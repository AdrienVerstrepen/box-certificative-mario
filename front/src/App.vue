<script setup>
import NavBar from '@/components/NavBar.vue'
</script>

<template>
  <div class="app-shell">
    <NavBar />
    <router-view />
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}

html {
  min-height: 100%;
  background: #eef3f6;
}

body {
  min-width: 320px;
  min-height: 100vh;
  margin: 0;
  background:
    linear-gradient(180deg, rgba(15, 118, 110, 0.08), rgba(238, 243, 246, 0) 18rem),
    #eef3f6;
  color: #0f172a;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

a {
  color: inherit;
}

button,
input {
  font: inherit;
}

.app-shell {
  min-height: 100vh;
}

.page {
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto;
  padding: 2rem 0;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.page-header h1 {
  margin: 0;
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  line-height: 1.1;
}

.page-header p {
  max-width: 42rem;
  margin: 0.45rem 0 0;
  color: #64748b;
}

@media (max-width: 720px) {
  .page-header {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
