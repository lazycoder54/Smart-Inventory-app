<template>
    <div class="flex gap-3 mb-5">
      <button
        v-for="(filter, index) in filters"
        :key="index"
        @click="$emit('filter-selected', filter)"
        class="px-4 py-2 bg-gray-100 rounded-xl text-sm font-medium text-gray-800"
      >
        {{ filter }}
      </button>
    </div>
  </template>
  
  <script>
  export default {
    props: ['filters'],
  };
  </script>
  

  