<template>
  <MainLayout>
    <div class="flex h-full w-full">
      <div class="flex-grow bg-gray-50 p-8 overflow-auto">
        <div class="w-full h-full bg-white shadow-xl rounded-lg">
          <div
            class="bg-green-600 text-white px-6 py-4 flex items-center justify-between"
          >
            <h1 class="text-3xl font-bold flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8 mr-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 10h11M9 21V3M19 4v16m-4-8h8"
                />
              </svg>
              Reports Dashboard
            </h1>
          </div>

          <div class="p-8 h-[calc(100%-72px)] overflow-auto">
            <div class="space-y-6">
              <div class="grid grid-cols-2 gap-6">
                <div>
                  <label class="block text-gray-700 font-semibold mb-2"
                    >Report Type</label
                  >
                  <select
                    required
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  >
                    <option value="" disabled>Select Report Type</option>
                    <option value="sales">Sales Report</option>
                    <option value="inventory">Inventory Report</option>
                    <option value="users">User Activity Report</option>
                  </select>
                </div>

                <div>
                  <label class="block text-gray-700 font-semibold mb-2"
                    >Date Range</label
                  >
                  <div class="grid grid-cols-2 gap-4">
                    <input
                      type="date"
                      required
                      class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    />
                    <input
                      type="date"
                      required
                      class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-green-500 focus:border-transparent"
                    />
                  </div>
                </div>
              </div>

              <div class="pt-4">
                <button
                  type="submit"
                  class="w-full bg-green-600 text-white py-3 rounded-md hover:bg-green-700 transition duration-300"
                >
                  Generate Report
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script>
import Sidebar from "@/components/Sidebar.vue";
import MainLayout from "../components/MainLayout.vue";

export default {
  components: {
    Sidebar,
    MainLayout,
  },
};
</script>

<style scoped>
input:focus,
select:focus {
  @apply ring-2 ring-green-500 border-transparent;
}
</style>
