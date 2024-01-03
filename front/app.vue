<script setup>
import { useRoute } from 'vue-router'
import '@unocss/reset/tailwind.css'

const route = useRoute()

const isRootPath = computed(() => route.path === '/')

useHead({
  htmlAttrs: {
    lang: 'en',
  },
  charset: 'utf-8',
  title: 'Nuxt Movies',
  titleTemplate: title => title !== 'Nuxt Movies' ? `${title} · Nuxt Movies` : title,
  meta: [
    { name: 'description', content: 'A TMDB client built with Nuxt Image to show the potential of it ✨' },
    { property: 'og:image', content: 'https://movies.nuxt.space/social-card.png' },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:site', content: '@nuxt_js' },
    { name: 'twitter:creator', content: '@nuxt_js' },
  ],
  link: [
    {
      rel: 'icon',
      type: 'image/webp',
      href: '/movies.webp',
    },
  ],
})
</script>

<template>
  <NuxtLoadingIndicator />
  
  <div
    h-full w-full font-sans
    grid="~ lt-lg:rows-[1fr_max-content] lg:cols-[max-content_1fr]"
    of-hidden view-transition-app transition duration-0
  >
  
    <div id="app-scroller" of-x-hidden of-y-auto relative>
      <!-- <router-link to="/login" class="login-button ">Login</router-link> -->
      <!-- Chatgpt : Cette div doit être visible uniquement lorsque path=/root -->
      <div v-if="isRootPath" class="divided-x">
        <InputID/>
        <InputAlgo/>
      </div>

      <NuxtPage />
    </div>
    
    <NavBar lg:order-first />
    <IframeModal />
    <PhotoModal />
    <router-link to="/MovieRecommendations" class="login-button">Show recommended movie</router-link>
  </div>
</template>

<style>
html, body , #__nuxt{
  height: 100vh;
  margin: 0;
  padding: 0;
  background: #111;
  color: white;
  color-scheme: dark;
}

.login-button {
  display: inline-block;
  padding: 10px 20px;
  right: 100px; 
  margin-top: 10px; /* Adjust the top margin to move the button down */
  background-color: #007bff; /* Set your desired background color */
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.divided-x {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.divided-x > * {
  flex: 1;
}

</style>
