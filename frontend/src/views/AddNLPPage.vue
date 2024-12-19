<template>
  <MainLayout>
    <div class="flex h-screen">
      <!-- Sidebar -->

      <div class="w-1/4 bg-gray-100 border-r p-4">
        <h2 class="text-lg font-bold mb-4">Recently Added Items</h2>
        <ul class="space-y-2">
          <li
            v-for="(item, index) in recentItems"
            :key="index"
            class="bg-white p-3 rounded-md shadow-sm flex justify-between"
          >
            <div>
              <p class="font-semibold">{{ item.name }}</p>
              <p class="text-sm text-gray-500">
                {{ item.quantity }} {{ item.unit }}
              </p>
            </div>
            <span class="text-sm text-green-600 font-semibold"
              >+{{ item.quantity }}</span
            >
          </li>
        </ul>
      </div>

      <!-- Main Content -->
      <div class="flex-grow p-6">
        <h1 class="text-2xl font-bold mb-4">Add Item via NLP Command</h1>
        <form @submit.prevent="addNLPItem" class="space-y-4">
          <div
            class="flex items-center space-x-2 border border-gray-300 p-3 rounded-md"
          >
            <span class="text-gray-400 text-lg"></span>
            <input
              v-model="command"
              type="text"
              placeholder="e.g., Add 5 kg of sugar"
              class="flex-grow outline-none"
              required
            />
          </div>
          <button
            type="submit"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
          >
            Submit Command
          </button>
        </form>

        <!-- Inventory Table -->
        <div class="mt-8">
          <h2 class="text-xl font-bold mb-4">Inventory</h2>
          <table
            class="w-full table-auto border-collapse border border-gray-300"
          >
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-4 py-2">Name</th>
                <th class="border border-gray-300 px-4 py-2">Quantity</th>
                <th class="border border-gray-300 px-4 py-2">Unit</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(item, index) in inventory"
                :key="index"
                class="hover:bg-gray-50"
              >
                <td class="border border-gray-300 px-4 py-2">
                  {{ item.name }}
                </td>
                <td class="border border-gray-300 px-4 py-2">
                  {{ item.quantity }}
                </td>
                <td class="border border-gray-300 px-4 py-2">
                  {{ item.unit }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script>
import MainLayout from "../components/MainLayout.vue";
import axios from "../api/inventory";
import { useToast } from "vue-toastification";
import { io } from "socket.io-client";

export default {
  components: {
    MainLayout,
  },
  data() {
    return {
      command: "",
      recentItems: [],
      inventory: [],
      socket: null,
      toast: useToast(),
    };
  },
  methods: {
    async addNLPItem() {
      try {
        await axios.post("/inventory/add-nlp", { command: this.command });
        this.toast.success("Item added successfully!");
        this.command = "";
      } catch (error) {
        this.toast.error("Failed to process command");
      }
    },
    initializeSocket() {
      const baseURL = axios.defaults.baseURL || "";
      this.socket = io(baseURL);
      this.socket.on("inventory_update", (data) => {
        if (data.action === "add" && data.item) {
          this.addRecentItem(data.item);
          this.updateInventory(data.item);
        }
      });
    },
    addRecentItem(item) {
      this.recentItems.unshift(item);
      if (this.recentItems.length > 5) {
        this.recentItems.pop();
      }
    },
    updateInventory(newItem) {
      const existingItemIndex = this.inventory.findIndex(
        (item) => item.name === newItem.name && item.unit === newItem.unit
      );
      if (existingItemIndex !== -1) {
        this.inventory[existingItemIndex].quantity += newItem.quantity;
      } else {
        this.inventory.unshift(newItem);
      }
    },
    async fetchInventory() {
      try {
        const response = await axios.get("/inventory/list");
        this.inventory = Array.isArray(response.data)
          ? response.data.items
          : [];
      } catch {
        this.toast.error("Failed to load inventory");
      }
    },
  },
  mounted() {
    this.fetchInventory();
    this.initializeSocket();
  },
  beforeDestroy() {
    if (this.socket) {
      this.socket.disconnect();
    }
  },
};
</script>

<style scoped>
.table-auto {
  width: 100%;
}
html,
body {
  overflow: hidden;
  height: 100%;
}
</style>
