<template>
  <div class="flex min-h-screen bg-gray-100">
    <Sidebar />

    <!-- Main Content -->
    <main class="flex-1 p-10">
      <header
        class="flex items-center justify-between border-b border-gray-200 mb-5"
      >
        <div class="flex items-center gap-4">
          <div
            class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center"
          >
            <img
              src="@/assets/inventory-logo.png"
              alt="Smart Inventory Logo"
              class="w-8 h-8"
            />
          </div>
          <h2 class="text-lg font-bold text-gray-800">Smart Inventory</h2>
        </div>
        <div class="flex gap-8">
          <label class="flex items-center bg-gray-100 rounded-xl px-4 py-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5 text-gray-500 mr-2"
              viewBox="0 0 256 256"
            >
              <path
                d="M229.66,218.34l-50.07-50.06..."
                fill="currentColor"
              ></path>
            </svg>
            <input
              type="text"
              placeholder="Search"
              class="bg-transparent focus:outline-none"
              v-model="searchQuery"
            />
          </label>
          <button
            class="flex items-center justify-center h-10 w-10 rounded-xl bg-gray-100"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-5 h-5 text-gray-800"
              viewBox="0 0 256 256"
            >
              <path d="M221.8,175.94C216.25..." fill="currentColor"></path>
            </svg>
          </button>
        </div>
      </header>

      <!-- Main Inventory Content -->
      <div>
        <h1 class="text-2xl font-bold text-gray-800 mb-5">
          {{ isStockView ? "Stock Inventory" : "Inventory" }}
        </h1>

        <!-- Categories -->
        <div class="mb-5" v-if="!isStockView">
          <FilterButtons
            :filters="['All', 'In Stock', 'Out of Stock']"
            @filter-selected="selectedFilter = $event"
          />
        </div>

        <!-- Inventory Table for Stock View -->
        <inventory-table
          v-if="isStockView"
          :items="filteredItems"
          @edit="editItem"
        />

        <!-- General Inventory List for Other Views -->
        <div v-else class="space-y-4">
          <div
            v-for="item in filteredItems"
            :key="item.id"
            class="relative flex items-center justify-between border p-4 mb-2"
          >
            <!-- Item details -->
            <span>{{ item.name }}</span>

            <!-- Edit button and dropdown -->
            <ActionDropdown
              :itemId="item.id"
              :isOpen="openDropdown === item.id"
              @toggle="() => toggleDropdown(item.id)"
              @edit="editItem"
              @delete="deleteItem"
            />
          </div>
        </div>
      </div>

      <PromptModal
        v-if="showPromptModal"
        :isVisible="showPromptModal"
        :itemName="modalItem.name"
        :currentQuantity="modalItem.quantity"
        @confirm="updateItem(modalItem.id, $event)"
        @close="closePromptModal"
      />
    </main>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar.vue";
import FilterButtons from "../components/FilterButtons.vue";
import ActionDropdown from "@/components/ActionDropdown.vue";
import InventoryTable from "@/components/InventoryTable.vue";
import axios from "../api/inventory";
import PromptModal from "../components/PromptModal.vue";
import { useToast } from "vue-toastification";

export default {
  components: {
    Sidebar,
    FilterButtons,
    ActionDropdown,
    InventoryTable,
    PromptModal,
  },
  data() {
    return {
      items: [],
      searchQuery: "",
      selectedFilter: "All",
      openDropdown: null,
      showPromptModal: false,
      modalItem: {},
      toast: useToast(),
    };
  },
  computed: {
    isStockView() {
      return this.$route.query.view === "stock";
    },
    filteredItems() {
      let filtered = this.items;
      if (this.searchQuery && typeof this.searchQuery === "string") {
        filtered = filtered.filter((item) =>
          item.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      if (this.selectedFilter !== "All") {
        filtered = filtered.filter(
          (item) => item.status === this.selectedFilter
        );
      }
      return filtered;
    },
  },
  methods: {
    toggleDropdown(itemId) {
      this.openDropdown = this.openDropdown === itemId ? null : itemId;
    },
    closeDropdown() {
      this.openDropdown = null;
    },
    editItem(itemId) {
      const item = this.items.find((item) => item.id === itemId);
      if (item) {
        this.modalItem = item;
        this.showPromptModal = true;
      }
    },
    async updateItem(itemId, quantity) {
      try {
        const response = await axios.put(`/inventory/update/${itemId}`, {
          quantity,
        });
        this.toast.success(
          response.data.message || "Item updated successfully!"
        );
        const updatedItem = this.items.find((item) => item.id === itemId);
        if (updatedItem) {
          updatedItem.quantity = quantity;
        }
        this.showPromptModal = false;
      } catch (error) {
        console.error(
          "Error updating item:",
          error.response?.data || error.message
        );
        this.toast.error("Failed to update item. Please try again.");
      }
    },
    async deleteItem(itemId) {
      try {
        const response = await axios.delete(`/inventory/delete/${itemId}`);
        this.toast.success(
          response.data.message || "Item deleted successfully!"
        );
        this.items = this.items.filter((item) => item.id !== itemId);
      } catch (error) {
        console.error(
          "Error deleting item:",
          error.response?.data || error.message
        );
        this.toast.error("Failed to delete item. Please try again.");
      }
    },
    closePromptModal() {
      this.showPromptModal = false;
    },
    handleOutsideClick(event) {
      if (!this.$el.contains(event.target)) {
        this.openDropdown = null;
      }
    },
  },
  async created() {
    try {
      const response = await axios.get("/inventory/list");
      this.items = response.data.items; // Adjust according to your API response structure
    } catch (error) {
      console.error("Error fetching inventory:", error.response?.data);
    }
  },
  mounted() {
    document.addEventListener("click", this.handleOutsideClick);

    this.$socket.on("inventory_update", (data) => {
      if (data.action === "update") {
        const updatedItem = this.items.find((item) => item.id === data.item.id);
        if (updatedItem) {
          updatedItem.quantity = data.item.quantity;
        }
      } else if (data.action === "delete") {
        this.items = this.items.filter((item) => item.id !== data.item_id);
      }
    });
  },
  beforeDestroy() {
    document.removeEventListener("click", this.handleOutsideClick);
  },
};
</script>
