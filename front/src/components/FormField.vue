<script setup>
const props = defineProps({
  id: String,
  label: String,
  type: String,
  modelValue: String,
  placeholder: String,
  required: Boolean,
})

defineEmits(['update:modelValue'])
</script>

<template>
  <label class="form-field" :for="props.id">
    <span>{{ props.label }}</span>
    <input
      :id="props.id"
      :type="props.type || 'text'"
      :value="props.modelValue || ''"
      :placeholder="props.placeholder || ''"
      :required="props.required ?? false"
      @input="$emit('update:modelValue', $event.target.value)"
    >
  </label>
</template>

<style scoped>
.form-field {
  display: grid;
  gap: 0.45rem;
  color: #334155;
  font-weight: 700;
}

.form-field input {
  width: 100%;
  min-height: 2.85rem;
  padding: 0.7rem 0.85rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #ffffff;
  color: #0f172a;
  font: inherit;
  font-weight: 500;
}

.form-field input:focus {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.14);
  outline: none;
}
</style>
