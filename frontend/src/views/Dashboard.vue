<template>
  <div class="flex h-screen bg-gray-50 dark:bg-gray-900 transition-all">
    <AdminSidebar />

    <div class="flex flex-col flex-1">
      <header
        class="bg-gradient-to-r from-blue-500 to-indigo-600 shadow-md fixed w-full z-10 transition-all"
      >
        <div
          class="flex justify-between items-center px-6 py-4 w-full max-w-screen-xl mx-auto"
        >
          <div class="flex-shrink-0">
            <h1 class="text-3xl font-bold text-white">Smart Inventory</h1>
          </div>

          <div class="flex items-center w-full max-w-full px-4">
            <input
              type="text"
              placeholder="Search..."
              class="w-full px-4 py-2 rounded-lg bg-white text-gray-800 placeholder-gray-400 border-2 border-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:placeholder-gray-500 transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div class="flex items-center space-x-4">
            <button class="text-white hover:text-indigo-400 transition-all">
              <i class="fas fa-bell"></i>
            </button>
          </div>
        </div>
      </header>

      <main class="mt-16 px-6 py-4 overflow-auto">
        <section class="mb-6">
          <DashboardHero />
        </section>

        <section>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div
              class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 transition-all hover:scale-105"
            >
              <h3
                class="text-xl font-semibold text-gray-800 dark:text-gray-200"
              >
                Total Inventory
              </h3>
              <p
                class="text-3xl font-bold text-indigo-600 dark:text-indigo-400"
              >
                1200
              </p>
            </div>
            <div
              class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 transition-all hover:scale-105"
            >
              <h3
                class="text-xl font-semibold text-gray-800 dark:text-gray-200"
              >
                Low Stock Alerts
              </h3>
              <p class="text-3xl font-bold text-red-500 dark:text-red-400">
                15
              </p>
            </div>
          </div>
        </section>

        <!-- Recent Activity -->
        <section class="mt-6">
          <Heading title="Recent Activity" />
          <table
            class="w-full bg-white dark:bg-white rounded-lg shadow-lg transition-all"
          >
            <thead>
              <tr class="bg-gray-100 dark:bg-gray-700">
                <th class="p-4 text-left text-gray-700 dark:text-gray-200">
                  Product Name
                </th>
                <th class="p-4 text-left text-gray-700 dark:text-gray-200">
                  Action
                </th>
                <th class="p-4 text-left text-gray-700 dark:text-gray-200">
                  Timestamp
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="hover:bg-white-50 dark:hover:bg-white transition-all">
                <td class="p-4">Widget A</td>
                <td class="p-4">Added</td>
                <td class="p-4">2024-12-13 10:00 AM</td>
              </tr>
              <tr class="hover:bg-gray-50 dark:hover:bg-white transition-all">
                <td class="p-4">Widget B</td>
                <td class="p-4">Updated</td>
                <td class="p-4">2024-12-13 11:30 AM</td>
              </tr>
            </tbody>
          </table>
        </section>

        <section class="mt-6">
          <ChartCard />
        </section>
      </main>
    </div>
  </div>
</template>

<script>
import AdminSidebar from "@/components/Admin/sidebar/AdminSidebar.vue";
import DashboardHero from "@/components/Admin/DashboardHero.vue";
import Heading from "@/utils/Heading.vue";
import InventoryTable from "@/components/InventoryTable.vue";
import ChartCard from "@/components/ChartCard.vue";

export default {
  name: "DashboardView",
  components: {
    AdminSidebar,
    DashboardHero,
    Heading,
    InventoryTable,
    ChartCard,
  },
};
</script>

<style scoped>
body {
  font-family: "Inter", sans-serif;
}
button,
input:focus {
  outline: none;
}

button:hover {
  cursor: pointer;
}

table th {
  border-bottom: 1px solid #e2e8f0;
}

table td {
  padding: 12px;
}

.grid .rounded-lg:hover {
  transform: scale(1.05);
}

.transition-all {
  transition: all 0.3s ease-in-out;
}
</style>
