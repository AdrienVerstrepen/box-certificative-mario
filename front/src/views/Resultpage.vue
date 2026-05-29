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

    <button @click="updateDistance()" class="update-button">Update distance</button>
</template>

<style>
:root {
    --bg: #f4f5f7;
    --panel: #ffffff;
    --border: #d6d6d8;
    --text: #2f3d4c;
    --accent: #2563eb;
    --accent-dark: #1e40af;
}

.clusters {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1.5rem;
    max-width: 1140px;
    margin: 0 auto;
    background: var(--bg);
}

.cluster-box {
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem;
    width: 100%;
    max-width: 540px;
    background: var(--panel);
    box-shadow: 0 8px 24px rgba(31, 41, 55, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cluster-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(31, 41, 55, 0.12);
}

.cluster-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #eef2f7;
}

.cluster-header h3 {
    margin: 0;
    color: var(--text);
    font-size: 1.1rem;
}

.cluster-header p {
    margin: 0.35rem 0 0;
    color: #64748b;
    font-size: 0.95rem;
}

.cluster-actions button,
.item-actions button,
.update-button {
    border: none;
    border-radius: 999px;
    padding: 0.55rem 0.85rem;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background-color 0.15s ease, transform 0.15s ease;
}

.cluster-actions button,
.update-button {
    background: var(--accent);
    color: #fff;
}

.item-actions button {
    background: #eef2ff;
    color: var(--accent-dark);
}

.cluster-actions button:disabled,
.item-actions button:disabled,
.update-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.cluster-actions button:not(:disabled):hover,
.update-button:not(:disabled):hover {
    background: var(--accent-dark);
}

.cluster-items {
    display: grid;
    gap: 0.85rem;
}

.cluster-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.75rem;
    padding: 0.9rem 1rem;
    border-radius: 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
}

.cluster-item span {
    color: var(--text);
    font-weight: 500;
}

.item-actions {
    display: flex;
    gap: 0.5rem;
}

.update-button {
    display: inline-flex;
    margin: 1rem 1.5rem;
}
</style>