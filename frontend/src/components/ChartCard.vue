<template>
  <div class="bg-white rounded-lg shadow">
    <div class="p-6">
      <h2 class="text-lg font-medium text-gray-900">
        <slot name="title">{{ title }}</slot>
      </h2>
      <div
        :id="chartId"
        ref="chartContainer"
        class="h-80 w-full bg-gray-100"
      ></div>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import merge from "lodash/merge";

export default {
  name: "ChartCard",
  props: {
    title: {
      type: String,
      default: "Chart Title",
    },
    chartId: {
      type: String,
      required: true,
    },
    chartOptions: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initializeChart();
    });
  },
  methods: {
    initializeChart() {
      const chartContainer = this.$refs.chartContainer;

      if (!chartContainer) {
        console.error("Chart container not found");
        return;
      }

      if (this.chart) {
        this.chart.dispose();
      }

      this.chart = echarts.init(chartContainer);

      const defaultOptions = {
        tooltip: { trigger: "axis" },
        xAxis: {
          type: "category",
          data: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        },
        yAxis: { type: "value" },
        series: [
          {
            name: "Sample Data",
            type: "bar",
            data: [120, 200, 150, 80, 70, 110],
          },
        ],
      };

      const mergedOptions = merge({}, defaultOptions, this.chartOptions);
      this.chart.setOption(mergedOptions);

      window.addEventListener("resize", this.chart.resize);
    },
  },
  watch: {
    chartOptions: {
      deep: true,
      handler(newOptions) {
        if (this.chart) {
          this.chart.setOption(newOptions);
        }
      },
    },
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.dispose();
    }
    window.removeEventListener("resize", this.chart.resize);
  },
};
</script>
