<script setup>
import { getSearchResult } from '@/api/geocodingApiRequests';
import LocationSearchBar from '@/components/LocationSearchBar.vue';
import { ref, computed } from 'vue';

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

const clusterOrder = ref([...new Set(results.value.map((item) => item.cluster))])

const clusters = computed(() => {
    return clusterOrder.value.map((clusterId) => ({
        id: clusterId,
        name: `step ${clusterId}`,
        items: results.value.filter((item) => item.cluster === clusterId),
    }))
})

const refreshSteps = () => {
    let nextStep = 1
    results.value.forEach((item) => {
        item.step = nextStep++
    })
}

const moveItem = (clusterIndex, itemIndex, direction) => {
    const cluster = clusters.value[clusterIndex]
    if (!cluster) {
        return
    }

    const newItemIndex = itemIndex + direction
    if (newItemIndex < 0 || newItemIndex >= cluster.items.length) {
        return
    }

    const clusterGlobalIndices = results.value
        .map((item, idx) => (item.cluster === cluster.id ? idx : -1))
        .filter((idx) => idx !== -1)

    const [moved] = results.value.splice(clusterGlobalIndices[itemIndex], 1)
    results.value.splice(clusterGlobalIndices[newItemIndex], 0, moved)
    refreshSteps()
}

const moveCluster = (clusterIndex, direction) => {
    const newClusterIndex = clusterIndex + direction
    if (newClusterIndex < 0 || newClusterIndex >= clusterOrder.value.length) {
        return
    }

    const [movedClusterId] = clusterOrder.value.splice(clusterIndex, 1)
    clusterOrder.value.splice(newClusterIndex, 0, movedClusterId)

    const ordered = clusterOrder.value.flatMap((clusterId) =>
        results.value.filter((item) => item.cluster === clusterId)
    )
    results.value = ordered
    refreshSteps()
}

const updateDistance = async () => {
    // API
}

const handleLocationSelect = (location) => {
    locations.value.push(location)
    searchResults.value = []
}

const send = () => {
    console.log('Sending locations to back-end:', locations.value)
    // Send locations.value to back-end
}

</script>

<template>
    <div class="clusters">
        <div v-for="(cluster, clusterIndex) in clusters" :key="cluster.id" class="cluster-box">
            <div class="cluster-header">
                <div>
                    <h3>{{ cluster.name }}</h3>
                    <p>{{ cluster.items.length }} location(s)</p>
                </div>
                <div class="cluster-actions">
                    <button @click="moveCluster(clusterIndex, -1)" :disabled="clusterIndex === 0">Move step up</button>
                    <button @click="moveCluster(clusterIndex, 1)" :disabled="clusterIndex === clusters.length - 1">Move step down</button>
                </div>
            </div>

            <div class="cluster-items">
                <div v-for="(item, itemIndex) in cluster.items" :key="item.id" class="cluster-item">
                    <span>{{ item.step }}. {{ item.name }} ({{ item.country }})</span>
                    <div class="item-actions">
                        <button @click="moveItem(clusterIndex, itemIndex, -1)" :disabled="itemIndex === 0">↑</button>
                        <button @click="moveItem(clusterIndex, itemIndex, 1)" :disabled="itemIndex === cluster.items.length - 1">↓</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <button @click="updateDistance()">updateDistance</button>
</template>

<style>
.clusters {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}

.cluster-box {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 1rem;
    width: 100%;
    max-width: 520px;
    background: #f9f9f9;
}

.cluster-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
}

.cluster-actions button,
.item-actions button {
    margin-left: 0.25rem;
}

.cluster-items {
    display: grid;
    gap: 0.75rem;
}

.cluster-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    border-radius: 8px;
    background: #fff;
    border: 1px solid #ddd;
}

.item-actions {
    display: flex;
    gap: 0.25rem;
}
</style>