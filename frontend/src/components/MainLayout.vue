<template>
    <div class="flex h-full">
      <Sidebar />
      <main class="flex-grow p-6 bg-gray-100">
        <slot />
      </main>
    </div>
  </template>
  
  <script>
  import Sidebar from './Sidebar.vue';
  
  export default {
    components: {
      Sidebar,
    },
  };
  </script>
  

  