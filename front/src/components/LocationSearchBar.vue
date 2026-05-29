<script setup>

const userQuery = defineModel()

</script>

<template>
    <input class="location-search" type="text" v-model="userQuery" placeholder="Paris, France...">
</template>

<style scoped>
.location-search {
    width: 100%;
    min-height: 2.85rem;
    padding: 0.75rem 0.85rem;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    background: #ffffff;
    color: #0f172a;
}

.location-search:focus {
    border-color: #0f766e;
    box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.14);
    outline: none;
}
</style>
