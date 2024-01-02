<template>
    <div>
        <div flex bg-gray:10 items-center px6 py4 gap3 sticky>
            <div i-ph:magnifying-glass text-xl op50 />
            <input v-model="input" type="text" text-2xl bg-transparent outline-none w-full
                :placeholder="$t('Enter an algorithm : svd, nn')">
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
// ... other imports as needed

const input = ref(localStorage.getItem('inputAlgo') || '')
const error = ref<unknown>()
const results = ref<any[]>([])


watch(input, () => {
    // Save the current input (algorithm) to local storage
    localStorage.setItem('inputAlgo', input.value);

    // Fetch the user ID from local storage
    const userId = localStorage.getItem('inputID') || '';

    // Call fetchResults with both user ID and algorithm
    fetchResults(userId, input.value);

    // Log combined inputs
    logCombinedInputs();
});



async function fetchResults(userId: string, algo: string) {
    try {
        // Construct the URL with query parameters
        const url = `http://127.0.0.1:8000/recommend?algorithm_name=${algo}&user_id=${userId}`;

        // Make the API call
        const response = await fetch(url);

        // Check if the response is OK (status code 200-299)
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }

        // Parse the JSON response
        const data = await response.json();

        // Check if the data is an array and update 'results'
        if (Array.isArray(data)) {
            results.value = data;
        } else {
            results.value = []; // Set to empty array if data is not an array
        }
    } catch (e) {
        // Handle errors, such as network issues
        console.error('Error fetching results:', e);
        error.value = e;
        results.value = []; // Reset results to empty array on error
    }
}


function logCombinedInputs() {
    const inputID = localStorage.getItem('inputID') || ''
    console.log(`InputID = ${inputID} + InputAlgo = ${input.value}`)
}
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
