<script setup>
import { sendPlacesRequest } from '@/api/backendApiRequests';
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
    console.log(location);
    const name = location.name || location.display_name?.split(',')[0]?.trim() || ''
    const country = location.address?.country || location.display_name?.split(',').pop()?.trim() || ''

    const locationInfos = {
        Name: name,
        latitude: location.lat,
        longitude: location.lon,
        Country: country,
    }
    console.log(locationInfos)

    locations.value.push(locationInfos)
    searchResults.value = []
}

const send = () => {
    console.log(locations.value)
    sendPlacesRequest(locations.value)
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
        <span>{{ location.Name }}, {{ location.Country }} </span> <button @click="locations.splice(index, 1)"> Remove</button>
    </div>
    
    <br />
    <br />
    <br />
    <button @click="send()">send locations</button>

</template>

<style>
</style>