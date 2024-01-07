<template>
    <div>
        <div flex bg-gray:10 items-center px6 py4 gap3 sticky>
            <div i-ph:magnifying-glass text-xl op50 />
            <input v-model="input" type="text" text-2xl bg-transparent outline-none w-full
                :placeholder="$t('Enter an algorithm')">
        </div>

        <!-- Display results -->
        <div v-if="results.length">
            <ul>
                <li v-for="result in results" :key="result.id">{{ result.name }}</li>
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
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const input = ref(userStore.algorithm) // Initialize input with algorithm from the store
const error = ref<unknown>()
const results = ref<any[]>([])

import { useLoading } from '@/composables/useLoading'
const { isLoading, startLoading, finishLoading } = useLoading();
import { useMovieStore } from '~/stores/useMovieStore';
const movieStore = useMovieStore();

async function fetchResults(userId: string, algo: string) {
    try {
        // Start the loading indicator
        movieStore.setMovies([]);
        startLoading();

        const response = await fetch(`http://127.0.0.1:8000/recommend?algorithm_name=${algo}&user_id=${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // console.log(data);
        if (data && data['Top 10 Recommendations']) {
            // Update the movieStore with the recommendations from the server
            movieStore.setMovies(data['Top 10 Recommendations']);
        } else {
            movieStore.setMovies([]);  // Set an empty array if no recommendations
            finishLoading();
        }
    } catch (e) {
        // console.error('Error fetching results:', e);
        error.value = e;
        results.value = [];
        movieStore.setMovies([]);
        // Finish the loading indicator
        finishLoading();
    }
}

watch(input, (newInput) => {
    userStore.setAlgorithm(newInput)
    // Assume userId is managed in another component and accessed here
    const userId = userStore.userId
    fetchResults(userId, newInput)
    // console.log(`InputID = ${userId} + InputAlgo = ${newInput}`)
})
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
