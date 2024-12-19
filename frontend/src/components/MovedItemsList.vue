<template>
    <div class="bg-white rounded-lg shadow-lg p-4 mt-6">
      <h2 class="text-xl font-semibold mb-4">Moved Items</h2>
      <table class="w-full border-collapse">
        <thead>
          <tr class="bg-gray-100 text-left">
            <th class="border border-gray-300 px-4 py-2">Item ID</th>
            <th class="border border-gray-300 px-4 py-2">Source</th>
            <th class="border border-gray-300 px-4 py-2">Destination</th>
            <th class="border border-gray-300 px-4 py-2">Quantity Change</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(item, index) in movedItems"
            :key="index"
            class="hover:bg-gray-50"
          >
            <td class="border border-gray-300 px-4 py-2">{{ item.item_id }}</td>
            <td class="border border-gray-300 px-4 py-2">{{ item.source_location }}</td>
            <td class="border border-gray-300 px-4 py-2">{{ item.destination_location }}</td>
            <td class="border border-gray-300 px-4 py-2">{{ item.change }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      movedItems: {
        type: Array,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  table {
    width: 100%;
  }
  th, td {
    text-align: left;
  }
  </style>
  