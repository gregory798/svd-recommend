import { defineStore } from "pinia";

export const useMovieStore = defineStore("movie", {
  state: () => ({
    movies: [], // Existing movies list
    dauphine: [
      "Clay Pigeons",
      "Onegin",
      "Fallen",
      "Great Expectations",
      "Heartwood",
      "Homegrown",
      "Hope Floats",
      "The Horse Whisperer",
      "Hurlyburly",
      "Twilight",
      "Meet Joe Black",
      "Montana",
      "Music from Another Room",
      "Next Stop Wonderland",
      "Phantoms",
      "Primary Colors",
      "Sliding Doors",
      "Back to the Future",
      "Sphere",
      "Three Kings",
    ], // New dauphine list with default titles
  }),
  actions: {
    setMovies(titles) {
      this.movies = titles;
    },
    // Optionally, you can add an action to set titles for dauphine
    setDauphineTitles(titles) {
      this.dauphine = titles;
    },
  },
});
