<script setup lang="ts">
import type { MediaType } from '~/types'
import { QUERY_LIST } from '~/constants/lists'

const route = useRoute()
const type = computed(() => route.params.type as MediaType || 'movie')

const queries = computed(() => [
  // QUERY_LIST.recommendation[0],
  QUERY_LIST.movie[0],
  QUERY_LIST.tv[0],
])

// console.log(queries);

// const AsyncWrapper = defineComponent({
//   name: 'AsyncWrapper',
//   async setup(_, ctx) {
//     const list = await listMedia(type.value, queries.value[0].query, 1);
//     const item = await getMedia(type.value, list.results[0].id);
//     console.log("item :")
//     console.log(item)
//     return () => ctx.slots?.default?.({ item })
//   },
// })

const AsyncWrapper = defineComponent({
  name: 'AsyncWrapper',
  props: {
    initialItem: {
      type: Object as () => Media | null,
      default: null // Providing a default value of null
    }
  },
  setup(props, ctx) {
    const item = ref(props.initialItem);
    return () => ctx.slots?.default?.({ item: item.value })
  },
})

import { listMedia, searchShows, getMedia } from '../composables/tmdb';
import type { Media } from '../types';

import { useMovieStore } from '~/stores/useMovieStore';
const movieStore = useMovieStore();

// console.log(movieStore.dauphine);

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
const moviesInfo = ref<(Media | null)[]>([]);
const dauphineMoviesInfo = ref<(Media | null)[]>([]);


// Computed property to reactively update movie details when store changes
watchEffect(async () => {
  // Fetch movie details for each title
  const details = await Promise.all(
    movieStore.movies.map(title => getMovieInfoByTitle(title))
  );
  // Filter out null results and update moviesInfo
  moviesInfo.value = details.filter(detail => detail !== null);
  // console.log("moviesInfo")
  // console.log(moviesInfo)
});

watchEffect(async () => {
  // startLoading();
  const details = await Promise.all(
    movieStore.dauphine.map(title => getMovieInfoByTitle(title))
  );
  dauphineMoviesInfo.value = details.filter(detail => detail !== null);
  // finishLoading();
});


import { useLoading } from '@/composables/useLoading'
const { isLoading, startLoading, finishLoading } = useLoading();
// console.log(moviesInfo);

</script>

<template>
  <div>
    <!-- <AsyncWrapper v-slot="{ item }" v-if="moviesInfo.length > 0">
      <NuxtLink :to="`/${type}/${item.id}`">
        <MediaHero :item="item" />
      </NuxtLink>
    </AsyncWrapper> -->

      <AsyncWrapper 
        v-if="moviesInfo.length > 0"
        :initialItem="moviesInfo[0]"
        v-slot="{ item }"
      >
        <NuxtLink :to="`/${type}/${item.id}`">
          <MediaHero :item="item" />
        </NuxtLink>
      </AsyncWrapper>




    <div flex py3 px10 items-center mt5 v-if="moviesInfo.length > 0" style="margin-bottom: -2%;">
      <div text-2xl>
        Recommended Movies
      </div>
    </div>

    <CarouselItems v-if="moviesInfo.length > 0" :items="moviesInfo" :type="'movie'" />






    
    <!-- <p class="text-2xl" style="margin-left: 2%; margin-top: 1%;">Recommended Movies</p> -->
    

      <!-- Display a message if moviesInfo is empty -->
      <div v-if="moviesInfo.length === 0" class="empty-list-message m-10 text-2xl">
        <div v-if="isLoading">
          <!-- <p>Generating recommendations, please wait ...</p> -->
          <div class="atom-spinner">
            <div class="spinner-inner">
              <div class="spinner-line"></div>
              <div class="spinner-line"></div>
              <div class="spinner-line"></div>
              <!--Chrome renders little circles malformed :(-->
              <div class="spinner-circle">
                &#9679;
              </div>
            </div>
          </div>
        </div>
        <div v-else style="color: rgb(93, 93, 93);">
          <p>To generate recommendations, please enter your user id and wait a few seconds.</p>
          <p>Exemples of user id : 1380819, 185150, 1351377, 386143, 2173336, 716091, 671513, 1227848, 712664</p>
          <!-- <p>Exemples of algorithm : svd, mlp</p> -->
        </div>
      </div>

      <div flex py3 px10 items-center mt5 v-if="dauphineMoviesInfo.length > 0" style="margin-bottom: -2%;">
        <div text-2xl>
          Other Movies
        </div>
      </div>
      <div v-if="dauphineMoviesInfo.length > 0" class="dauphine-carousel">
        <CarouselItems :items="dauphineMoviesInfo" :type="type" />
      </div>
    <!-- <CarouselAutoQuery
      v-for="query of queries"
      :key="query.type + query.query"
      :query="query"
    /> -->
    <!-- <TheFooter /> -->
  </div>
</template>


<style scoped>

.empty-list-message {
  display: flex;
  justify-content: center;
}
.atom-spinner, .atom-spinner * {
      box-sizing: border-box;
    }

    .atom-spinner {
      height: 60px;
      width: 60px;
      overflow: hidden;
    }

    .atom-spinner .spinner-inner {
      position: relative;
      display: block;
      height: 100%;
      width: 100%;
    }

    .atom-spinner .spinner-circle {
      display: block;
      position: absolute;
      color: #1cf40c;
      font-size: calc(60px * 0.24);
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
    }

    .atom-spinner .spinner-line {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      animation-duration: 1s;
      border-left-width: calc(60px / 25);
      border-top-width: calc(60px / 25);
      border-left-color: #1cf40c;
      border-left-style: solid;
      border-top-style: solid;
      border-top-color: transparent;
    }

    .atom-spinner .spinner-line:nth-child(1) {
      animation: atom-spinner-animation-1 1s linear infinite;
      transform: rotateZ(120deg) rotateX(66deg) rotateZ(0deg);
    }

    .atom-spinner .spinner-line:nth-child(2) {
      animation: atom-spinner-animation-2 1s linear infinite;
      transform: rotateZ(240deg) rotateX(66deg) rotateZ(0deg);
    }

    .atom-spinner .spinner-line:nth-child(3) {
      animation: atom-spinner-animation-3 1s linear infinite;
      transform: rotateZ(360deg) rotateX(66deg) rotateZ(0deg);
    }

    @keyframes atom-spinner-animation-1 {
      100% {
        transform: rotateZ(120deg) rotateX(66deg) rotateZ(360deg);
      }
    }

    @keyframes atom-spinner-animation-2 {
      100% {
        transform: rotateZ(240deg) rotateX(66deg) rotateZ(360deg);
      }
    }

    @keyframes atom-spinner-animation-3 {
      100% {
        transform: rotateZ(360deg) rotateX(66deg) rotateZ(360deg);
      }
    }
</style>