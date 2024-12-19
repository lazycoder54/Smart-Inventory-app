<template>
    <div>
      <meta name="description" :content="description" />
      <meta name="keywords" :content="keywords" />
      <title>{{ title }}</title>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      title: String,
      description: String,
      keywords: String,
    },
  };
  </script>
  