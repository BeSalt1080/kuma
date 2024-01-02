<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
import router from './router';

console.log(router)
const currentpath = router.currentRoute 

</script>

<template class="overflow-x-clip min-h-dvh">
  <header v-if="!currentpath.fullPath.startsWith('/dashboard')">
    <Navbar />
  </header>
  <main class="h-full w-vw overflow-x-clip min-h-dvh">
    <RouterView class="h-full w-full"/>
  </main>
  <footer>
    <Footer />
  </footer>
</template>
