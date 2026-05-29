<script setup>
import AppButton from '@/components/AppButton.vue'
import AppCard from '@/components/AppCard.vue'

const props = defineProps({
  title: String,
  description: String,
  errorMessage: String,
  submitLabel: String,
  loading: Boolean,
})

const emit = defineEmits(['submit'])
</script>

<template>
  <main class="auth-page">
    <AppCard class="auth-card">
      <div class="auth-heading">
        <h1>{{ props.title }}</h1>
        <p>{{ props.description }}</p>
      </div>

      <p v-if="props.errorMessage" class="auth-error">{{ props.errorMessage }}</p>

      <form class="auth-form" @submit.prevent="emit('submit')">
        <slot />
        <AppButton class="auth-submit" type="submit" :disabled="props.loading ?? false">
          {{ props.loading ? 'Please wait' : props.submitLabel }}
        </AppButton>
      </form>

      <div v-if="$slots.footer" class="auth-footer">
        <slot name="footer" />
      </div>
    </AppCard>
  </main>
</template>

<style scoped>
.auth-page {
  display: grid;
  place-items: center;
  min-height: calc(100vh - 5rem);
  padding: 2rem 1rem;
}

.auth-card {
  width: min(100%, 440px);
  padding: 1.5rem;
}

.auth-heading {
  margin-bottom: 1.25rem;
}

.auth-heading h1 {
  margin: 0;
  color: #0f172a;
  font-size: 1.8rem;
  line-height: 1.15;
}

.auth-heading p {
  margin: 0.5rem 0 0;
  color: #64748b;
}

.auth-error {
  margin: 0 0 1rem;
  padding: 0.8rem 0.9rem;
  border: 1px solid #fecdd3;
  border-radius: 8px;
  background: #fff1f2;
  color: #9f1239;
  font-weight: 600;
}

.auth-form {
  display: grid;
  gap: 1rem;
}

.auth-submit {
  width: 100%;
}

.auth-footer {
  margin-top: 1rem;
  color: #64748b;
  text-align: center;
}

.auth-footer :deep(a) {
  color: #0f766e;
  font-weight: 700;
}
</style>
