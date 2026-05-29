<script setup>
const props = defineProps({
  type: String,
  variant: String,
  disabled: Boolean,
})
</script>

<template>
  <button
    class="app-button"
    :class="`app-button--${props.variant || 'primary'}`"
    :type="props.type || 'button'"
    :disabled="props.disabled ?? false"
  >
    <slot />
  </button>
</template>

<style scoped>
.app-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.75rem;
  padding: 0.7rem 1rem;
  border: 1px solid transparent;
  border-radius: 8px;
  font: inherit;
  font-weight: 700;
  line-height: 1;
  cursor: pointer;
  transition: background-color 0.16s ease, border-color 0.16s ease, color 0.16s ease;
}

.app-button:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.app-button--primary {
  background: #0f766e;
  color: #ffffff;
}

.app-button--primary:hover:not(:disabled) {
  background: #115e59;
}

.app-button--secondary {
  background: #ffffff;
  border-color: #cbd5e1;
  color: #334155;
}

.app-button--secondary:hover:not(:disabled) {
  border-color: #64748b;
  color: #0f172a;
}

.app-button--danger {
  background: #be123c;
  color: #ffffff;
}

.app-button--danger:hover:not(:disabled) {
  background: #9f1239;
}
</style>
