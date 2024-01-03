<template>
    <div>
      <h1>Fetched Result Page</h1>
      <ul>
        <li v-for="result in fetchedMovies" :key="result.id">{{ result.name }}</li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { fetchedMovies } from '@/composables/sharedData';
  
  // Create a ref for fetched movies
  const localFetchedMovies = ref(fetchedMovies.inputAlgoMovies || []);
  
  // Export fetchedMovies
  export { localFetchedMovies as fetchedMovies };
  </script>
  
  <style scoped>
  /* Add styles if needed */
  </style>
  