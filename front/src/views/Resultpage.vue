<script setup>
import { computed, ref } from 'vue'
import AppButton from '@/components/AppButton.vue'
import AppCard from '@/components/AppCard.vue'

const results = ref([
  { id: 1, name: 'Paris', lat: 48, lon: 2.35, country: 'France', step: 1, cluster: 1, hotel: 1 },
  { id: 2, name: 'Marseille', lat: 49, lon: 5.35, country: 'France', step: 2, cluster: 1, hotel: 1 },
  { id: 3, name: 'Nice', lat: 49, lon: 5.35, country: 'France', step: 3, cluster: 2, hotel: 3 },
])

const clusterOrder = ref([...new Set(results.value.map((item) => item.cluster))])

const clusters = computed(() => {
  return clusterOrder.value.map((clusterId) => ({
    id: clusterId,
    name: `Step ${clusterId}`,
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

  results.value = clusterOrder.value.flatMap((clusterId) =>
    results.value.filter((item) => item.cluster === clusterId)
  )
  refreshSteps()
}
</script>

<template>
  <main class="page">
    <header class="page-header">
      <div>
        <h1>Tour details</h1>
        <p>Reorder clusters and places before saving the final route.</p>
      </div>
      <AppButton>Update distance</AppButton>
    </header>

    <div class="clusters">
      <AppCard v-for="(cluster, clusterIndex) in clusters" :key="cluster.id" class="cluster-box">
        <div class="cluster-header">
          <div>
            <h2>{{ cluster.name }}</h2>
            <p>{{ cluster.items.length }} location(s)</p>
          </div>
          <div class="cluster-actions">
            <AppButton
              variant="secondary"
              :disabled="clusterIndex === 0"
              @click="moveCluster(clusterIndex, -1)"
            >
              Up
            </AppButton>
            <AppButton
              variant="secondary"
              :disabled="clusterIndex === clusters.length - 1"
              @click="moveCluster(clusterIndex, 1)"
            >
              Down
            </AppButton>
          </div>
        </div>

        <div class="cluster-items">
          <div v-for="(item, itemIndex) in cluster.items" :key="item.id" class="cluster-item">
            <span>{{ item.step }}. {{ item.name }} ({{ item.country }})</span>
            <div class="item-actions">
              <AppButton
                variant="secondary"
                :disabled="itemIndex === 0"
                @click="moveItem(clusterIndex, itemIndex, -1)"
              >
                Up
              </AppButton>
              <AppButton
                variant="secondary"
                :disabled="itemIndex === cluster.items.length - 1"
                @click="moveItem(clusterIndex, itemIndex, 1)"
              >
                Down
              </AppButton>
            </div>
          </div>
        </div>
      </AppCard>
    </div>
  </main>
</template>

<style scoped>
.clusters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.cluster-box {
  padding: 1.25rem;
}

.cluster-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.cluster-header h2 {
  margin: 0;
  color: #0f172a;
  font-size: 1.25rem;
}

.cluster-header p {
  margin: 0.25rem 0 0;
  color: #64748b;
}

.cluster-actions,
.item-actions {
  display: flex;
  gap: 0.5rem;
}

.cluster-items {
  display: grid;
  gap: 0.75rem;
}

.cluster-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem;
  border: 1px solid #dbe3ea;
  border-radius: 8px;
  background: #f8fafc;
}

.cluster-item span {
  color: #334155;
  font-weight: 700;
}

@media (max-width: 720px) {
  .cluster-header,
  .cluster-item {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
