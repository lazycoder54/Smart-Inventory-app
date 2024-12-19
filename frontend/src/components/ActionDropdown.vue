<template>
  <div class="relative" @click.stop>
    <!-- Trigger Button -->
    <button
      @click="$emit('toggle')"
      class="bg-blue-500 text-white px-4 py-2 rounded-md shadow hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-1"
    >
      Actions
    </button>

    <!-- Dropdown Menu -->
    <div
      v-if="isOpen"
      class="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden z-50"
    >
      <button
        @click="$emit('edit', itemId)"
        class="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-100 hover:text-blue-500 transition"
      >
        Edit
      </button>
      <button
        @click="$emit('delete', itemId)"
        class="w-full px-4 py-2 text-left text-red-500 hover:bg-red-100 hover:text-red-600 transition"
      >
        Delete
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isOpen: Boolean,
    itemId: {
      type: [String, Number],
      required: true,
    },
  },
};
</script>

<style>
.dropdown {
  position: relative;
}
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  padding: 8px 0;
  z-index: 10;
}
.dropdown.open .dropdown-menu {
  display: block;
}
.actions-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
}
.delete-button {
  color: red;
}
</style>
