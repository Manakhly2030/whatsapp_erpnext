<template>
  <div id="app" class="bg-sky-500 hover:bg-sky-700">
    <HomeView />
  </div>
</template>

<script>
import HomeView from './view/HomeView.vue';

export default {
  name: 'App',
  components: {
    HomeView,
  },
};
</script>

<style>
/* Add any global styles here */
</style>
