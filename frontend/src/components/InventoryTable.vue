<template>
  <div class="overflow-x-auto bg-white border rounded-xl">
    <table class="min-w-full">
      <thead>
        <tr>
          <th class="px-4 py-3 text-left text-sm font-medium text-gray-800">
            ID
          </th>
          <th class="px-4 py-3 text-left text-sm font-medium text-gray-800">
            Name
          </th>
          <th class="px-4 py-3 text-left text-sm font-medium text-gray-800">
            Quantity
          </th>
          <th class="px-4 py-3 text-left text-sm font-medium text-gray-800">
            Unit
          </th>
          <th
            v-if="showActions"
            class="px-4 py-3 text-left text-sm font-medium text-gray-800"
          >
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in items" :key="index" class="border-t">
          <td class="px-4 py-2">{{ item.id }}</td>
          <td class="px-4 py-2">{{ item.name }}</td>
          <td class="px-4 py-2">{{ item.quantity }}</td>
          <td class="px-4 py-2">{{ item.unit }}</td>
          <td v-if="showActions" class="px-4 py-2">
            <button
              @click="$emit('edit', item.id)"
              class="text-blue-500 hover:underline"
            >
              Edit
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    items: Array,
    showActions: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
