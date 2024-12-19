<template>
  <div class="w-screen h-screen flex flex-col px-4 py-8 bg-gray-50">
    <div class="text-center mb-8">
      <h1 class="text-4xl font-extrabold text-gray-800">Sales Dashboard</h1>
      <p class="text-lg text-gray-600 mt-2">
        Easily analyze and manage your sales data.
      </p>
    </div>
    <div class="flex-1 grid md:grid-cols-2 gap-8 h-full">
      <ChartCard
        title="Sales Analytics"
        chartId="salesChart1"
        :chartOptions="{
          xAxis: {
            type: 'category',
            data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          },
          yAxis: {
            type: 'value',
          },
          series: [
            {
              type: 'bar',
              data: [120, 200, 150, 180, 230, 210],
            },
          ],
        }"
      />
      <ChartCard
        title="Total Sales"
        chartId="salesChart2"
        :chartOptions="{
          xAxis: {
            type: 'category',
            data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          },
          yAxis: {
            type: 'value',
          },
          series: [
            {
              type: 'line',
              data: [12000, 20000, 15000, 18000, 23000, 21000],
            },
          ],
        }"
      />
    </div>
  </div>
</template>

<script>
import ChartCard from "@/components/ChartCard.vue";
export default {
  components: {
    ChartCard,
  },
  name: "Sales",
};
</script>

<style scoped>
.container {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}
</style>

<style>
.title {
  @apply text-gray-900;
}
</style>
