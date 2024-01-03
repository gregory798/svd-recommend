// stores/user.js
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    userId: "",
    algorithm: "",
  }),
  actions: {
    setUserId(id) {
      this.userId = id;
    },
    setAlgorithm(algo) {
      this.algorithm = algo;
    },
  },
});
