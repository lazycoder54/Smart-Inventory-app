<template>
  <div class="container">
    <h1 class="title">Analytics</h1>
    <p class="description">Analyze your data and view insights in real-time.</p>
    <div v-if="loading" class="loading">Loading insights...</div>
    <div v-else class="insights">
      <h2>Key Metrics</h2>
      <ul>
        <li v-for="(metric, index) in metrics" :key="index">
          <strong>{{ metric.name }}:</strong> {{ metric.value }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "Analytics",
  data() {
    return {
      loading: true,
      metrics: [],
    };
  },
  methods: {
    fetchData() {
      setTimeout(() => {
        this.metrics = [
          { name: "Visitors", value: 1234 },
          { name: "Page Views", value: 5678 },
          { name: "Conversion Rate", value: "3.2%" },
        ];
        this.loading = false;
      }, 2000);
    },
  },
  mounted() {
    this.fetchData();

    this.interval = setInterval(this.fetchData, 5000);
  },
  beforeDestroy() {
    if (this.interval) {
      clearInterval(this.interval);
    }
  },
};
</script>

<style scoped>
.container {
  padding: 2rem;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 2rem auto;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1rem;
}

.description {
  font-size: 1rem;
  color: #4b5563;
}

.loading {
  color: #9ca3af;
  font-size: 1.2rem;
  text-align: center;
}

.insights {
  margin-top: 1.5rem;
}

.insights h2 {
  font-size: 1.5rem;
  color: #1f2937;
  margin-bottom: 1rem;
}

.insights ul {
  list-style: none;
  padding: 0;
}

.insights li {
  font-size: 1.1rem;
  color: #4b5563;
  margin-bottom: 0.5rem;
}
</style>
