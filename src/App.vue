<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue';
import Footer from './components/Footer.vue';
import router from './router';

console.log(router)
const currentpath = router.currentRoute 

</script>

<template class="overflow-x-clip">
  <header v-if="!currentpath.fullPath.startsWith('/dashboard')">
    <Navbar />
  </header>
  <main class="min-h-dvh h-dvh w-vw overflow-x-clip">
    <RouterView class="h-full"/>
  </main>
  <footer>
    <Footer />
  </footer>
</template>
