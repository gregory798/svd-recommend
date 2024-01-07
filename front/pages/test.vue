<template>
    <div>
        <button @click="fetchRandomApi">Fetch API Publique</button>
        <button @click="fetchYourApi">Fetch Votre API</button>
        <div v-if="apiResponse">
            <pre>{{ apiResponse }}</pre>
        </div>
        <div v-if="error">
            Erreur: {{ error }}
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        const apiResponse = ref(null);
        const error = ref(null);

        const fetchRandomApi = () => {
            fetch('https://api.publicapis.org/entries')
                .then(response => response.json())
                .then(data => {
                    apiResponse.value = data;
                    error.value = null;
                })
                .catch(err => {
                    error.value = err.message;
                    apiResponse.value = null;
                });
        };

        const fetchYourApi = () => {
            fetch('http://100.26.162.40/recommend?algorithm_name=als&user_id=1351377') // Remplacez par votre URL d'API
                .then(response => response.json())
                .then(data => {
                    apiResponse.value = data;
                    error.value = null;
                })
                .catch(err => {
                    error.value = err.message;
                    apiResponse.value = null;
                });
        };

        return { fetchRandomApi, fetchYourApi, apiResponse, error };
    }
};
</script>

<style>
/* Ajoutez votre CSS ici si nécessaire */
</style>
