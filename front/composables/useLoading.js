import { ref } from "vue";

const isLoading = ref(false);

function startLoading() {
  isLoading.value = true;
}

function finishLoading() {
  isLoading.value = false;
}

export function useLoading() {
  return { isLoading, startLoading, finishLoading };
}
