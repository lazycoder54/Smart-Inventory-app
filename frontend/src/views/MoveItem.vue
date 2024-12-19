<template>
  <div class="flex min-h-screen bg-gray-100 relative">
    <!-- Sidebar -->
    <Sidebar class="w-64 bg-black shadow-lg" />

    <!-- Main Content -->
    <div class="flex-1 p-6 overflow-auto">
      <h1 class="text-3xl font-bold text-gray-800 mb-6">
        Warehouse Management
      </h1>

      <!-- Form to Move Items -->
      <form
        @submit.prevent="moveItem"
        class="bg-white p-6 rounded-lg shadow-lg h-full w-full"
      >
        <h2 class="text-xl font-semibold mb-4">Move Item</h2>

        <!-- Form Inputs -->
        <div class="mb-4">
          <label for="item_id" class="block text-gray-700 font-medium mb-2"
            >Item ID</label
          >
          <input
            v-model="form.item_id"
            type="text"
            id="item_id"
            placeholder="Enter Item ID"
            class="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div class="mb-4">
          <label
            for="source_location"
            class="block text-gray-700 font-medium mb-2"
            >Source Location</label
          >
          <input
            v-model="form.source_location"
            type="text"
            id="source_location"
            placeholder="Enter Source Location"
            class="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div class="mb-4">
          <label
            for="destination_location"
            class="block text-gray-700 font-medium mb-2"
            >Destination Location</label
          >
          <input
            v-model="form.destination_location"
            type="text"
            id="destination_location"
            placeholder="Enter Destination Location"
            class="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div class="mb-4">
          <label for="change" class="block text-gray-700 font-medium mb-2"
            >Quantity Change</label
          >
          <input
            v-model="form.change"
            type="number"
            id="change"
            placeholder="Enter Quantity Change"
            class="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full p-3 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 transition"
        >
          Move Item
        </button>
      </form>

      <!-- Moved Items List -->
      <MovedItemsList :movedItems="movedItems" />

      <div
        v-if="realTimeUpdates.length"
        class="mt-4 p-4 bg-blue-100 border-l-4 border-blue-500 text-blue-700"
      >
        <h3 class="text-lg font-bold">Inventory Updates:</h3>
        <ul>
          <li v-for="(update, index) in realTimeUpdates" :key="index">
            {{ update }}
          </li>
        </ul>
      </div>
    </div>

    <!-- Toast Notifications -->
    <div class="fixed top-4 right-4 space-y-2">
      <div
        v-for="(notification, index) in notifications"
        :key="index"
        class="p-4 rounded-lg shadow-lg text-white"
        :class="{
          'bg-green-500': notification.type === 'success',
          'bg-red-500': notification.type === 'error',
        }"
      >
        {{ notification.message }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/api/inventory";
import Sidebar from "@/components/Sidebar.vue";
import MovedItemsList from "@/components/MovedItemsList.vue";
import { io } from "socket.io-client";

export default {
  components: {
    Sidebar,
    MovedItemsList,
  },
  data() {
    return {
      form: {
        item_id: "",
        source_location: "",
        destination_location: "",
        change: null,
      },
      realTimeUpdates: [],
      notifications: [],
      movedItems: [],
    };
  },
  methods: {
    async moveItem() {
      try {
        const response = await axios.post("inventory/move", this.form);
        const newMovedItem = { ...this.form };
        this.movedItems.push(newMovedItem);
        this.addNotification(
          "success",
          response.data.message || "Stock moved successfully!"
        );
        // Reset form
        this.form = {
          item_id: "",
          source_location: "",
          destination_location: "",
          change: null,
        };
      } catch (error) {
        this.addNotification(
          "error",
          error.response?.data?.message ||
            "Failed to move stock. Please try again."
        );
      }
    },
    handleRealTimeUpdate(data) {
      if (!data) {
        console.error("No data received for inventory_update event");
        return;
      }

      const message = `Item ID ${data.item_id} moved from ${data.source_location} to ${data.destination_location} with change of ${data.change}. New Quantity: ${data.new_quantity}`;
      this.realTimeUpdates.push(message);
    },
    addNotification(type, message) {
      const id = Date.now();
      this.notifications.push({ type, message, id });
      setTimeout(() => {
        this.notifications = this.notifications.filter(
          (notif) => notif.id !== id
        );
      }, 5000);
    },
  },
  mounted() {
    this.socket = io();
    this.socket.on("connect", () => {});
    this.socket.on("inventory_update", this.handleRealTimeUpdate);
  },

  beforeDestroy() {
    if (this.socket) {
      this.socket.disconnect();
    }
  },
};
</script>

<style scoped>
body {
  font-family: "Inter", sans-serif;
}

.fixed {
  z-index: 50;
}
</style>
