<template>
  <MainLayout>
    <div class="flex h-full w-full">
      <div class="flex-grow bg-gray-50 p-8 overflow-auto">
        <div class="w-full h-full bg-white shadow-xl rounded-lg">
          <!-- Header -->
          <div
            class="bg-blue-600 text-white px-6 py-4 flex items-center justify-between"
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
                  d="M17 14v6m-3-3h6M6 10h2a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v2a2 2 0 002 2zm10 0h2a2 2 0 002-2V6a2 2 0 00-2-2h-2a2 2 0 00-2 2v2a2 2 0 002 2zM6 20h2a2 2 0 002-2v-2a2 2 0 00-2-2H6a2 2 0 00-2 2v2a2 2 0 002 2z"
                />
              </svg>
              {{
                isUpdateMode ? "Update Item Quantity" : "Add New Inventory Item"
              }}
            </h1>
            <button
              @click="toggleMode"
              class="bg-white text-blue-600 px-4 py-2 rounded-md"
            >
              {{
                isUpdateMode ? "Switch to Add Mode" : "Switch to Update Mode"
              }}
            </button>
          </div>

          <!-- Form -->
          <form
            @submit.prevent="handleSubmit"
            class="p-8 h-[calc(100%-72px)] overflow-auto"
          >
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 h-full">
              <!-- Left Column -->
              <div class="space-y-6">
                <div v-if="isUpdateMode">
                  <label class="block text-gray-700 font-semibold mb-2"
                    >Item ID</label
                  >
                  <input
                    v-model="updateData.itemId"
                    type="text"
                    placeholder="Enter item ID"
                    required
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label class="block text-gray-700 font-semibold mb-2"
                    >Item Name</label
                  >
                  <input
                    v-model="itemData.name"
                    type="text"
                    placeholder="Enter item name"
                    required
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-gray-700 font-semibold mb-2"
                      >Quantity</label
                    >
                    <input
                      v-model.number="quantity"
                      type="number"
                      min="0"
                      placeholder="Enter quantity"
                      required
                      class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div v-if="!isUpdateMode">
                    <label class="block text-gray-700 font-semibold mb-2"
                      >Unit</label
                    >
                    <select
                      v-model="itemData.unit"
                      required
                      class="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="" disabled>Select Unit</option>
                      <option value="pcs">Pieces</option>
                      <option value="kg">Kilograms</option>
                      <option value="liters">Liters</option>
                      <option value="g">Grams</option>
                      <option value="lb">Pound</option>
                      <option value="oz">Ounce</option>
                      <option value="dozen">Dozen</option>
                      <option value="pack">Pack</option>
                      <option value="bottle">Bottle</option>
                      <option value="box">Box</option>
                      <option value="ton">Tons</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            <div class="pt-4">
              <button
                type="submit"
                :disabled="isSubmitting"
                class="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{
                  isSubmitting
                    ? "Processing..."
                    : isUpdateMode
                    ? "Update Item"
                    : "Add Item"
                }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script>
import MainLayout from "../components/MainLayout.vue";
import axios from "../api/inventory";
import { useToast } from "vue-toastification";

export default {
  components: {
    MainLayout,
  },
  data() {
    return {
      isUpdateMode: false,
      isSubmitting: false,
      itemData: {
        name: "",
        quantity: null,
        unit: "",
      },
      updateData: {
        itemId: "",
        name: "",
        quantity: null,
      },
    };
  },
  computed: {
    quantity: {
      get() {
        return this.isUpdateMode
          ? this.updateData.quantity
          : this.itemData.quantity;
      },
      set(value) {
        if (this.isUpdateMode) {
          this.updateData.quantity = value;
        } else {
          this.itemData.quantity = value;
        }
      },
    },
  },
  methods: {
    toggleMode() {
      this.isUpdateMode = !this.isUpdateMode;
      this.resetForm();
    },
    async handleSubmit() {
      const toast = useToast();
      this.isSubmitting = true;
      try {
        if (this.isUpdateMode) {
          await axios.put(`/inventory/update/${this.updateData.itemId}`, {
            quantity: this.updateData.quantity,
          });
          toast.success(`Item updated successfully`);
        } else {
          await axios.post("/inventory/add", this.itemData);
          toast.success(`Item "${this.itemData.name}" added successfully`);
        }
        this.resetForm();
      } catch (error) {
        console.error("Error:", error.response || error.message);
        toast.error("Failed to process the request");
      } finally {
        this.isSubmitting = false;
      }
    },
    resetForm() {
      this.itemData = { name: "", quantity: null, unit: "" };
      this.updateData = { itemId: "", quantity: null };
    },
  },
};
</script>

<style scoped>
.h-full {
  height: 100%;
}

input:focus,
select:focus,
textarea:focus {
  @apply ring-2 ring-blue-500 border-transparent;
}

.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.5s ease-in-out;
}

.toast-fade-enter,
.toast-fade-leave-to {
  opacity: 0;
}
</style>
