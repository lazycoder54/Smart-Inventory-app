<template>
  <div class="bg-white h-full shadow-md w-1/6">
    <nav>
      <ul class="space-y-2">
        <li>
          <router-link
            to="/list-items"
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
          >
            <i class="fas fa-box text-2xl mr-4"></i> Inventory
          </router-link>
        </li>
        <li>
          <router-link
            to="/analytics"
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
          >
            <i class="fas fa-chart-line text-2xl mr-4"></i> Analytics
          </router-link>
        </li>
        <li>
          <router-link
            to="/sales"
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
          >
            <i class="fas fa-shopping-cart text-2xl mr-4"></i> Sales
          </router-link>
        </li>
        <li>
          <router-link
            to="/customers"
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
          >
            <i class="fas fa-users text-2xl mr-4"></i> Customers
          </router-link>
        </li>
        <li>
          <router-link
            to="/orders"
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
          >
            <i class="fas fa-receipt text-2xl mr-4"></i> Orders
          </router-link>
        </li>
        <li>
          <router-link
            to="/notifications"
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
          >
            <i class="fas fa-bell text-2xl mr-4"></i> Notifications
          </router-link>
        </li>
        <li>
          <router-link
            to="/activity-log"
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
          >
            <i class="fas fa-history text-2xl mr-4"></i> Activity Log
          </router-link>
        </li>
        <li>
          <router-link
            to="/help"
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
          >
            <i class="fas fa-question-circle text-2xl mr-4"></i> Help
          </router-link>
        </li>
        <li>
          <router-link
            to="/support"
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
          >
            <i class="fas fa-headset text-2xl mr-4"></i> Support
          </router-link>
        </li>
        <li>
          <button
            class="flex items-center justify-start w-full text-gray-700 hover:text-blue-500 font-medium text-xl py-4 px-4"
            @click="handleLogout"
          >
            <i class="fas fa-sign-out-alt text-2xl mr-4"></i> Logout
          </button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
export default {
  methods: {
    handleLogout() {
      localStorage.removeItem("jwt_token");
      localStorage.removeItem("refresh_token");

      sessionStorage.clear();
      const userStore = this.$userStore;
      if (userStore) {
        userStore.setUsername("");
      }
      this.$toast && this.$toast.info("You have been logged out successfully.");
      this.$router.push("/login");
    },
  },
};
</script>
