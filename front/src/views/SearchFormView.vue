<script setup>
import { getSearchResult } from '@/api/geocodingApiRequests';
import LocationSearchBar from '@/components/LocationSearchBar.vue';
import { ref } from 'vue';

const userSearch = ref('')
const searchResults = ref([])
const locations = ref([])

const handleSearch = async (userInput) => {
    try {
        const results = await getSearchResult(userSearch.value)
        searchResults.value = results
        userSearch.value = ''        
    } catch (error) {
        console.warn(error)
    }
}

const handleLocationSelect = (location) => {
    locations.value.push(location)
    searchResults.value = []
}

const send = () => {
    console.log("Sending locations to back-end:", locations.value)
    // Send locations.value to back-end
}

</script>

<template>

    <LocationSearchBar v-model="userSearch"></LocationSearchBar>
    <button @click="handleSearch(userSearch.value)">SEARCH!</button>

    <div v-if="searchResults.length > 0">
        <h2>Search Results:</h2>
        <ul>
            <li v-for="(result, index) in searchResults" :key="index">
                <button @click="handleLocationSelect(result)">{{ result.display_name }}</button>
            </li>
        </ul>
    </div>

    <div v-for="(location,index) in locations" :key="index">
        <span>{{ location.display_name }} </span> <button @click="locations.splice(index, 1)"> Remove</button>
    </div>
    
    <br />
    <br />
    <br />
    <button @click="send()">send locations</button>

</template>

<style>
</style>