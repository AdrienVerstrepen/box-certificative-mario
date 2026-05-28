<script setup>
import { getSearchResult } from '@/api/geocodingApiRequests';
import LocationSearchBar from '@/components/LocationSearchBar.vue';
import { ref } from 'vue';

const userSearch = ref('')

</script>

<template>
    <LocationSearchBar v-model="userSearch"></LocationSearchBar>
    <button @click="getSearchResult(userSearch)">SEARCH!</button>

</template>

<style>
</style>