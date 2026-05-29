<script setup>
import { ref } from 'vue'
import { sendPlacesRequest } from '@/api/backendApiRequests'
import { getSearchResult } from '@/api/geocodingApiRequests'
import AppButton from '@/components/AppButton.vue'
import AppCard from '@/components/AppCard.vue'
import LocationSearchBar from '@/components/LocationSearchBar.vue'

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
  const name = location.name || location.display_name?.split(',')[0]?.trim() || ''
  const country = location.address?.country || location.display_name?.split(',').pop()?.trim() || ''

  locations.value.push({
    PlaceName: name,
    Latitude: location.lat,
    Longitude: location.lon,
    Country: country,
  })
  searchResults.value = []
}

const send = () => {
  sendPlacesRequest(locations.value)
}
</script>

<template>
  <main class="page">
    <header class="page-header">
      <div>
        <h1>Plan a route</h1>
        <p>Build a trip from selected places, then save it as a public or private tour.</p>
      </div>
    </header>

    <AppCard class="planner-panel">
      <div class="tour-settings">
        <div class="field">
          <label for="tour-name">Tour name</label>
          <input id="tour-name" v-model="tourName" type="text" placeholder="Enter tour name">
        </div>
        <div class="field visibility-field">
          <span>Visibility</span>
          <label><input v-model="visibility" type="radio" value="true"> Public</label>
          <label><input v-model="visibility" type="radio" value="false"> Private</label>
        </div>
      </div>

      <form class="search-form" @submit.prevent="handleSearch">
        <LocationSearchBar v-model="userSearch" />
        <AppButton type="submit">Search</AppButton>
      </form>
    </AppCard>

    <AppCard v-if="searchResults.length > 0" class="results-panel">
      <h2>Search results</h2>
      <ul class="search-results">
        <li v-for="(result, index) in searchResults" :key="index">
          <button type="button" @click="handleLocationSelect(result)">
            {{ result.display_name }}
          </button>
        </li>
      </ul>
    </AppCard>

    <AppCard class="selected-panel">
      <div class="selected-header">
        <div>
          <h2>Selected places</h2>
          <p>{{ locations.length }} place(s)</p>
        </div>
        <AppButton :disabled="locations.length === 0" @click="send">Save places</AppButton>
      </div>

      <ul v-if="locations.length" class="selected-list">
        <li v-for="(location, index) in locations" :key="index">
          <span>{{ location.PlaceName }}, {{ location.Country }}</span>
          <AppButton variant="secondary" @click="locations.splice(index, 1)">Remove</AppButton>
        </li>
      </ul>
      <p v-else class="empty-state">No place selected yet.</p>
    </AppCard>
  </main>
</template>

<style scoped>
.planner-panel,
.results-panel,
.selected-panel {
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.tour-settings {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(180px, 240px);
  gap: 1rem;
  margin-bottom: 1rem;
}

.field {
  display: grid;
  gap: 0.45rem;
}

.field label,
.visibility-field span {
  font-weight: 700;
  color: #334155;
}

.field input[type="text"] {
  min-height: 2.85rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 0.75rem 0.85rem;
  background: white;
  color: #0f172a;
}

.field input[type="text"]:focus {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.14);
  outline: none;
}

.visibility-field label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #475569;
}

.search-form {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 0.75rem;
}

.results-panel h2,
.selected-panel h2 {
  margin: 0;
  color: #0f172a;
  font-size: 1.25rem;
}

.search-results,
.selected-list {
  display: grid;
  gap: 0.75rem;
  margin: 1rem 0 0;
  padding: 0;
  list-style: none;
}

.search-results button {
  width: 100%;
  padding: 0.85rem;
  border: 1px solid #dbe3ea;
  border-radius: 8px;
  background: #f8fafc;
  color: #334155;
  text-align: left;
  cursor: pointer;
}

.search-results button:hover {
  border-color: #0f766e;
  background: #ecfdf5;
}

.selected-header,
.selected-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.selected-header p {
  margin: 0.25rem 0 0;
  color: #64748b;
}

.selected-list li {
  padding: 0.85rem;
  border: 1px solid #dbe3ea;
  border-radius: 8px;
  background: #f8fafc;
}

.selected-list span {
  color: #334155;
  font-weight: 700;
}

.empty-state {
  margin: 1rem 0 0;
  color: #64748b;
}

@media (max-width: 720px) {
  .tour-settings,
  .search-form {
    grid-template-columns: 1fr;
  }

  .selected-header,
  .selected-list li {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
