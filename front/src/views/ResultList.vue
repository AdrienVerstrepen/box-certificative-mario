<script setup>
import { ref, computed } from 'vue'

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

const clusters = computed(() => {
    const grouped = new Map()

    results.value.forEach((item) => {
        if (!grouped.has(item.cluster)) {
            grouped.set(item.cluster, [])
        }
        grouped.get(item.cluster).push(item)
    })

    return Array.from(grouped.entries()).map(([clusterId, items]) => ({
        id: clusterId,
        name: `Tour ${clusterId}`,
        items,
    }))
})
</script>

<template>
    <div class="tour-list">
        <h1>All tours</h1>
        <div class="tour-grid">
            <div v-for="cluster in clusters" :key="cluster.id" class="tour-card">
                <div class="tour-card-header">
                    <div>
                        <h2>{{ cluster.name }}</h2>
                        <p>{{ cluster.items.length }} stop(s)</p>
                    </div>
                    <router-link :to="{ name: 'tour', params: { id: cluster.id } }" class="tour-link">
                        Open tour
                    </router-link>
                </div>

                <ul class="tour-stops">
                    <li v-for="item in cluster.items" :key="item.id">
                        Step {{ item.step }}: {{ item.name }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style>
.tour-list {
    padding: 1rem;
}

.tour-grid {
    display: grid;
    gap: 1rem;
}

.tour-card {
    border: 1px solid #ccc;
    border-radius: 10px;
    padding: 1rem;
    background: #fff;
}

.tour-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.75rem;
}

.tour-link {
    padding: 0.5rem 0.75rem;
    background: #3b82f6;
    color: #fff;
    border-radius: 8px;
    text-decoration: none;
}

.tour-stops {
    margin: 0;
    padding-left: 1.2rem;
}

.tour-stops li {
    margin-bottom: 0.4rem;
}
</style>