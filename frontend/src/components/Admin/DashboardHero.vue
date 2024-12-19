<template>
  <div class="flex justify-center items-center w-full h-screen bg-blue-50">
    <div class="p-8 bg-white rounded-lg shadow-lg w-full max-w-4xl mx-auto">
      <div class="text-center">
        <div class="flex justify-center items-center space-x-4 mb-6">
          <img
            src="https://www.w3schools.com/w3images/avatar2.png"
            alt="User Avatar"
            class="w-16 h-16 rounded-full border-2 border-blue-500"
          />
          <h1 class="text-4xl font-extrabold text-gray-800">
            Welcome, {{ username }}!
          </h1>
        </div>

        <p class="text-lg text-gray-700 mb-4">
          The Smart Inventory Management System designed to revolutionize your
          inventory process.
        </p>
        <p class="text-md text-gray-600 mb-6">
          Track, manage, and optimize your inventory with real-time updates and
          powerful AI-driven tools.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
          <div
            class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-all"
          >
            <div class="flex items-center space-x-4 mb-4">
              <img
                src="https://img.icons8.com/ios-filled/50/000000/box.png"
                alt="Stock Management Icon"
                class="w-12 h-12"
              />
              <h2 class="text-xl font-semibold text-gray-800">
                Real-Time Stock Management
              </h2>
            </div>
            <p class="text-gray-600">
              Monitor stock levels in real-time and get automated alerts when
              stocks run low.
            </p>
          </div>

          <div
            class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-all"
          >
            <div class="flex items-center space-x-4 mb-4">
              <img
                src="https://img.icons8.com/ios-filled/50/000000/graph.png"
                alt="Reports Icon"
                class="w-12 h-12"
              />
              <h2 class="text-xl font-semibold text-gray-800">
                Analytics & Reports
              </h2>
            </div>
            <p class="text-gray-600">
              Generate detailed reports with just a few clicks, making it easier
              to analyze and optimize your business performance.
            </p>
          </div>

          <div
            class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-all"
          >
            <div class="flex items-center space-x-4 mb-4">
              <img
                src="https://img.icons8.com/ios-filled/50/000000/connected.png"
                alt="Integration Icon"
                class="w-12 h-12"
              />
              <h2 class="text-xl font-semibold text-gray-800">
                Seamless Integrations
              </h2>
            </div>
            <p class="text-gray-600">
              Integrate with other tools and platforms for a smooth and
              automated inventory management experience.
            </p>
          </div>

          <div
            class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-all"
          >
            <div class="flex items-center space-x-4 mb-4">
              <img
                src="https://img.icons8.com/ios-filled/50/000000/robot.png"
                alt="AI Automation Icon"
                class="w-12 h-12"
              />
              <h2 class="text-xl font-semibold text-gray-800">
                AI-Driven Automation
              </h2>
            </div>
            <p class="text-gray-600">
              Automate repetitive tasks and use AI to optimize your inventory
              levels and reduce waste.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from "@/store/store";
import { computed } from "vue";

export default {
  setup() {
    const userStore = useUserStore();
    const username = computed(() => userStore.username);

    return { username };
  },
};
</script>

<style scoped>
.bg-blue-50 {
  background-color: #eff6ff;
}

button:hover {
  background-color: #2563eb;
}

button:focus {
  outline: none;
  box-shadow: 0 0 5px rgba(37, 99, 235, 0.5);
}

h1,
h2 {
  font-family: "Inter", sans-serif;
}

p {
  font-family: "Roboto", sans-serif;
}

.w-full {
  width: 100%;
}

.h-screen {
  height: 100vh;
}

.max-w-4xl {
  max-width: 1200px;
}

@media (max-width: 768px) {
  .grid-cols-1 {
    grid-template-columns: 1fr;
  }
  .grid-cols-2 {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
