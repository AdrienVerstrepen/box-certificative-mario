<script setup>
import { sendPlacesRequest } from '@/api/backendApiRequests';
import { getSearchResult } from '@/api/geocodingApiRequests';
import LocationSearchBar from '@/components/LocationSearchBar.vue';
import { ref } from 'vue';

const tourName = ref('')
const visibility = ref('true')
const userSearch = ref('')
const searchResults = ref([])
const locations = ref([])

const handleSearch = async () => {
    try {
        const results = await getSearchResult(userSearch.value)
        searchResults.value = results
        userSearch.value = ''
    } catch (error) {
        console.warn(error)
    }
}

const handleLocationSelect = (location) => {
    console.log(location)
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
    console.log(tourName.value, visibility.value)
    sendPlacesRequest(locations.value)
}

</script>

<template>
    <div class="tour-settings">
        <div class="field">
            <label for="tour-name">Tour name</label>
            <input id="tour-name" type="text" v-model="tourName" placeholder="Enter tour name" />
        </div>
        <div class="field visibility-field">
            <span>Visibility</span>
            <label><input type="radio" value="true" v-model="visibility" /> Public</label>
            <label><input type="radio" value="false" v-model="visibility" /> Private</label>
        </div>
    </div>

    <form @submit.prevent="handleSearch" class="search-form">
        <LocationSearchBar v-model="userSearch" />
        <button type="submit">SEARCH!</button>
    </form>

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
.tour-settings {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 1.25rem;
    padding: 1rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
}

.field {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    min-width: 220px;
}

.field label,
.visibility-field span {
    font-weight: 600;
    color: #1f2937;
}

.field input[type="text"] {
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    padding: 0.75rem 0.9rem;
    background: white;
    color: #0f172a;
}

.visibility-field {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.visibility-field label {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
    color: #334155;
}

.search-form {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}

.search-form button {
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 999px;
    background: #2563eb;
    color: white;
    cursor: pointer;
}

.search-form button:hover {
    background: #1d4ed8;
}
</style>