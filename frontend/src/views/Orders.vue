<template>
    <div class="container">
      <h1 class="title">Orders</h1>
      <p class="description">Track and manage orders.</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "Orders",
  };
  </script>
  
  <style scoped>
  .container {
    padding: 2rem;
    background-color: #ecfdf5;
    border: 1px solid #d1fae5;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    max-width: 800px;
    margin: 2rem auto;
  }
  
  .title {
    font-size: 2rem;
    font-weight: 700;
    color: #065f46;
    margin-bottom: 1rem;
  }
  
  .description {
    font-size: 1rem;
    color: #10b981;
  }
  </style>
  