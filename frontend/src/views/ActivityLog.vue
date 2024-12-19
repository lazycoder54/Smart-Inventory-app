<template>
    <div class="container">
      <h1 class="title">Activity Log</h1>
      <p class="description">View your recent activities.</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "ActivityLog",
  };
  </script>
  
  <style scoped>
  .container {
    padding: 2rem;
    background-color: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 2rem auto;
  }
  
  .title {
    font-size: 2rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 1rem;
  }
  
  .description {
    font-size: 1rem;
    color: #374151;
  }
  </style>
  