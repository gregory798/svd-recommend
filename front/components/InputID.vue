<template>
    <div>
        <div flex bg-gray:10 items-center px6 py4 gap3 sticky>
            <div i-ph:magnifying-glass text-xl op50 />
            <input v-model="input" type="text" text-2xl bg-transparent outline-none w-full
                :placeholder="$t('Enter your user id ...')">
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

// const input = ref('')
// const error = ref<unknown>()
// const results = ref<any[]>([])


const input = ref(localStorage.getItem('inputID') || '')
const error = ref<unknown>()
const results = ref<any[]>([])

// // Function to call your API
// async function fetchResults(query: string) {
//     try {
//         const response = await fetch(`http://127.0.0.1:8000?query=${query}`);
//         const data = await response.json();
//         console.log(data)
//         results.value = data;  // Assuming the API returns an array
//     } catch (e) {
//         error.value = e;
//     }
// }

// Function to call your API
async function fetchResults(userId: string, algo: string) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/recommend?algorithm_name=${algo}&user_id=${userId}`);

        // Check if the response is OK
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);

        if (Array.isArray(data)) {
            results.value = data;
            console.log('API Response:', data); // Log the result here
        } else {
            results.value = []; // Set to empty array if data is not an array
        }
    } catch (e) {
        console.error('Error fetching results:', e);
        error.value = e;
        results.value = []; // Reset results to empty array on error
    }
}


// // Watch for changes in input and call fetchResults
// watch(input, () => {
//     fetchResults(input.value);
// });

const inputAlgo = localStorage.getItem('inputAlgo') || ''

// Watch for changes in inputID
watch(input, () => {
    localStorage.setItem('inputID', input.value)
    fetchResults(input.value, inputAlgo)
    logCombinedInputs()
})

function logCombinedInputs() {
    const inputAlgo = localStorage.getItem('inputAlgo') || ''
    console.log(`InputID = ${input.value} + InputAlgo = ${inputAlgo}`)
}

</script>

<style scoped>
/* Add your component-specific styles here */
</style>
