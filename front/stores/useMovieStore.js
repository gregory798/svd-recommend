import { defineStore } from "pinia";

export const useMovieStore = defineStore("movie", {
  state: () => ({
    movies: [], // Default movies
  }),
  actions: {
    setMovies(titles) {
      this.movies = titles;
    },
  },
});
