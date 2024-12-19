<template>
  <aside
    class="w-64 bg-gray-900 text-white h-screen overflow-y-auto flex flex-col p-6 shadow-lg"
  >
    <!-- Header -->
    <router-link
      to="/dashboard"
      class="text-3xl font-bold mb-10 text-center tracking-wide"
    >
      Smart Inventory
    </router-link>

    <ul class="space-y-4">
      <li>
        <router-link
          to="/list-items"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-list mr-4 text-xl"></i>
          <span>List Items</span>
        </router-link>
      </li>
      <li>
        <router-link
          to="/add-item"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-plus-circle mr-4 text-xl"></i>
          <span>Add Item</span>
        </router-link>
      </li>
      <li>
        <router-link
          to="/add-voice"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-microphone mr-4 text-xl"></i>
          <span>Add via Voice</span>
        </router-link>
      </li>
      <li>
        <router-link
          to="/show"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-search mr-4 text-xl"></i>
          <span>Show and Search</span>
        </router-link>
      </li>
      <li>
        <router-link
          to="/add-nlp"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-microchip mr-4 text-xl"></i>
          <span>Add via NLP</span>
        </router-link>
      </li>

      <li>
        <router-link
          to="/move"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-truck-moving mr-4 text-xl"></i>
          <span>Move Items</span>
        </router-link>
      </li>

      <li>
        <router-link
          to="/manage-users"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-user-cog mr-4 text-xl"></i>
          <span>Manage Users</span>
        </router-link>
      </li>
      <li>
        <router-link
          to="/reports"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-chart-line mr-4 text-xl"></i>
          <span>Reports</span>
        </router-link>
      </li>
      <li>
        <router-link
          to="/list-items?view=stock"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-boxes mr-4 text-xl"></i>
          <span>Stocks</span>
        </router-link>
      </li>
      <li>
        <router-link
          to="/profile"
          class="flex items-center text-lg font-medium text-gray-300 hover:text-white hover:bg-gray-700 py-3 px-4 rounded transition-colors"
        >
          <i class="fas fa-user-circle mr-4 text-xl"></i>
          <span>Profile</span>
        </router-link>
      </li>
    </ul>
  </aside>
</template>

<script>
export default {
  name: "Sidebar",
};
</script>
