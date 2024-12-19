<template>
  <div
    v-if="isVisible"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    @click.self="closeModal"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-96">
      <h3 class="text-xl font-bold mb-4">Edit Item Quantity</h3>
      <p class="text-gray-700 mb-4">
        You are about to update the quantity for "{{ itemName }}".
      </p>
      <div class="mb-4">
        <label for="quantity" class="block text-sm font-medium text-gray-700"
          >Quantity</label
        >
        <input
          v-model="quantity"
          type="number"
          id="quantity"
          class="mt-1 p-2 w-full border border-gray-300 rounded-md"
          min="1"
          required
        />
      </div>
      <div class="flex justify-between">
        <button
          @click="closeModal"
          class="px-4 py-2 bg-gray-300 text-gray-800 rounded-md hover:bg-gray-400"
        >
          Cancel
        </button>
        <button
          @click="confirmUpdate"
          class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
        >
          Confirm
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isVisible: {
      type: Boolean,
      required: true,
    },
    itemName: {
      type: String,
      required: true,
    },
    currentQuantity: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      quantity: this.currentQuantity,
    };
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    confirmUpdate() {
      this.$emit("confirm", this.quantity);
    },
  },
  watch: {
    currentQuantity(newVal) {
      this.quantity = newVal;
    },
  },
};
</script>

<style scoped>
.bg-opacity-50 {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
