<script setup>
import { computed, ref } from 'vue'
import AppCard from '@/components/AppCard.vue'

const results = ref([
  { id: 1, name: 'Paris', lat: 48, lon: 2.35, country: 'France', step: 1, cluster: 1, hotel: 1 },
  { id: 2, name: 'Marseille', lat: 49, lon: 5.35, country: 'France', step: 2, cluster: 1, hotel: 1 },
  { id: 3, name: 'Nice', lat: 49, lon: 5.35, country: 'France', step: 3, cluster: 2, hotel: 3 },
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
  <main class="page">
    <header class="page-header">
      <div>
        <h1>Saved tours</h1>
        <p>Review your generated routes and open a tour to adjust its steps.</p>
      </div>
      <router-link :to="{ name: 'Home' }" class="button-link">Create tour</router-link>
    </header>

    <div class="tour-grid">
      <AppCard v-for="cluster in clusters" :key="cluster.id" class="tour-card">
        <div class="tour-card-header">
          <div>
            <h2>{{ cluster.name }}</h2>
            <p>{{ cluster.items.length }} stop(s)</p>
          </div>
          <router-link :to="{ name: 'tour', params: { id: cluster.id } }" class="open-link">
            Open
          </router-link>
        </div>

        <ol class="tour-stops">
          <li v-for="item in cluster.items" :key="item.id">
            {{ item.name }}, {{ item.country }}
          </li>
        </ol>
      </AppCard>
    </div>
  </main>
</template>

<style scoped>
.button-link,
.open-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.75rem;
  padding: 0.7rem 1rem;
  border-radius: 8px;
  background: #0f766e;
  color: #ffffff;
  font-weight: 700;
  text-decoration: none;
}

.button-link:hover,
.open-link:hover {
  background: #115e59;
}

.tour-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}

.tour-card {
  padding: 1.25rem;
}

.tour-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
}

.tour-card h2 {
  margin: 0;
  color: #0f172a;
  font-size: 1.25rem;
}

.tour-card p {
  margin: 0.25rem 0 0;
  color: #64748b;
}

.tour-stops {
  display: grid;
  gap: 0.5rem;
  margin: 0;
  padding-left: 1.25rem;
  color: #334155;
}
</style>
