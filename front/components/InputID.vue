<template>
    <div>
        <div flex bg-gray:10 items-center px6 py4 gap3 sticky>
            <div i-ph:magnifying-glass text-xl op50 />
            <input v-model="input" type="text" text-2xl bg-transparent outline-none w-full
                :placeholder="$t('Enter your user id')">
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
const input = ref(userStore.userId) // Initialize input with userId from the store
const error = ref<unknown>()
const results = ref<any[]>([])

import { useLoading } from '@/composables/useLoading'
const { isLoading, startLoading, finishLoading } = useLoading();
import { useMovieStore } from '~/stores/useMovieStore';
const movieStore = useMovieStore();

async function fetchResults(userId: string, algo: string) {
    try {
        // Trim the userId to remove leading/trailing whitespace
        const trimmedUserId = userId.trim();

        // Check if the trimmed userId is empty
        if (!trimmedUserId) {
            // If userId is empty or only contains whitespace, set the movie list to empty and return
            movieStore.setMovies([]);
            return;
        }

        // Start the loading indicator
        startLoading();

        // Make the fetch request
        // const response = await fetch(`http://127.0.0.1:8000/recommend?algorithm_name=${algo}&user_id=${userId}`); --> local
        const response = await fetch(`http://100.26.162.40/recommend?algorithm_name=als&user_id=${userId}`); //--> online
        console.log(response)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // console.log(data)

        // Process the response
        if (data && data['Top 10 Recommendations']) {
            movieStore.setMovies(data['Top 10 Recommendations']);
        } else {
            movieStore.setMovies([]);
        }
    } catch (e) {
        error.value = e;
        results.value = [];
        movieStore.setMovies([]);
        // alert("Please verify your user id or algorithm: " + e);
    } finally {
        // Finish the loading indicator in both success and error cases
        finishLoading();
    }
}



import { listMedia, searchShows, getMedia } from '../composables/tmdb';
import type { Media } from '../types';

/**
 * Given a movie title, retrieves detailed information about the movie.
 * @param title The title of the movie.
 * @returns Promise containing movie details.
 */
async function getMovieInfoByTitle(title: string): Promise<Media | null> {
    // Search for the movie
    const searchResults = await searchShows(title);
    const movies = searchResults.results.filter((result) => result.media_type === 'movie');

    // Check if any movies were found
    if (movies.length === 0) {
        return null; // No movies found
    }

    // Assuming the first result is the desired movie
    const movieId = movies[0].id;

    // Get detailed information about the movie
    const movieDetails = await getMedia('movie', movieId);
    return movieDetails;
}



// Watch for changes in input and update the store, also call fetchResults
watch(input, (newInput) => {
    userStore.setUserId(newInput)
    const inputAlgo = userStore.algorithm
    fetchResults(newInput, inputAlgo)
    // console.log(`InputID = ${newInput} + InputAlgo = ${inputAlgo}`)
})
</script>

<style scoped>
/* Add your component-specific styles here */
</style>
