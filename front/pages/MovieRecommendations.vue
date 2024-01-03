<template>
  <div>
    <div flex bg-gray:10 items-center px6 py4 gap3 sticky>
      <div i-ph:magnifying-glass text-xl op50 />
      <input v-model="userId" type="text" text-2xl bg-transparent outline-none w-full
        :placeholder="$t('Enter your user id ...')">

      <!-- Input field for algorithm -->
      <input v-model="algorithm" type="text" text-2xl bg-transparent outline-none w-full
        :placeholder="$t('Enter an algorithm : svd, nn')">
    </div>

<!-- Display results -->
<div v-if="state.results.length">
      <ul>
        <li v-for="(movieId, index) in state.results" :key="index">
          {{ movieId }}
        </li>
      </ul>
    </div>

    <!-- Error handling -->
    <div v-if="error" p8 flex flex-col gap-3 items-start>
      <h1 text-4xl text-red>
        {{ $t('Error occurred on fetching') }}
      </h1>
      <pre py2>{{ error }}</pre>
      <button n-link px4 py1 rounded @click="error = undefined">
        {{ $t('Retry') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { reactive } from 'vue';

const userStore = useUserStore()
const userId = ref(userStore.userId)
const algorithm = ref(userStore.algorithm)
const error = ref<unknown>()
const state = reactive({
  results: [] as string[], // Holds the fetched movie IDs or results
})

async function fetchResults(userId: string, algo: string) {
  try {
    const response = await fetch(`http://127.0.0.1:8000/recommend?algorithm_name=${algo}&user_id=${userId}`)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    console.log(data) // Make sure data is in the expected format

    if (data && Array.isArray(data["Top 10 Recommendations"])) {
      state.results = data["Top 10 Recommendations"] // Extract movie IDs from the response
    } else {
      state.results = []
    }
  } catch (e) {
    error.value = e
    state.results = []
  }
}

// Fetch recommendations when the component is mounted
onMounted(() => {
  fetchResults(userId.value, algorithm.value)
})

// Watch for changes in user ID and algorithm, also call fetchResults
watch([userId, algorithm], ([newUserId, newAlgorithm]) => {
  userStore.setUserId(newUserId)
  userStore.setAlgorithm(newAlgorithm)
  fetchResults(newUserId, newAlgorithm)
})
</script>



<style scoped>

html, body , #__nuxt{
  height: 100vh;
  margin: 0;
  padding: 0;
  background: #111;
  color: white;
  color-scheme: dark;
}
</style>
