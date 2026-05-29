<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const tourId = Number(route.params.id)

const results = ref([
    {
        id: 1,
        name: 'paris',
        lat: 48,
        lon: 2.35,
        country: 'france',
        step: 1,
        cluster: 1,
        hotel: 1,
    },
    {
        id: 2,
        name: 'marseille',
        lat: 49,
        lon: 5.35,
        country: 'france',
        step: 2,
        cluster: 1,
        hotel: 1,
    },
    {
        id: 3,
        name: 'nice',
        lat: 49,
        lon: 5.35,
        country: 'france',
        step: 3,
        cluster: 2,
        hotel: 3,
    },
])

const tourItems = computed(() => results.value.filter((item) => item.cluster === tourId))
const tourName = computed(() => `Tour ${tourId}`)

const goBack = () => router.push({ name: 'results' })
</script>

<template>
    <div class="tour-details">
        <button @click="goBack" class="back-button">Back to tours</button>
        <h1>{{ tourName }}</h1>
        <p v-if="!tourItems.length">No stops found for this tour.</p>
        <ul v-else class="tour-stop-list">
            <li v-for="item in tourItems" :key="item.id">
                <strong>Step {{ item.step }}:</strong> {{ item.name }} — {{ item.country }}
            </li>
        </ul>
    </div>
</template>

<style>
.tour-details {
    padding: 1rem;
}

.back-button {
    margin-bottom: 1rem;
    padding: 0.5rem 0.75rem;
    border: none;
    background: #6b7280;
    color: white;
    border-radius: 6px;
    cursor: pointer;
}

.tour-stop-list {
    margin: 0;
    padding-left: 1.2rem;
}

.tour-stop-list li {
    margin-bottom: 0.6rem;
}
</style>