<script setup>
import { RouterView, useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';

const route = useRoute()

console.log(route.fullPath)

</script>

<template class="overflow-x-clip min-h-dvh">
  <header v-if="!route.fullPath.startsWith('/dashboard')">
    <Navbar />
  </header>
  <main class="min-h-[calc(100vh-64px)] w-vw overflow-x-clip ">
    <RouterView />
  </main>
  <footer>
    <Footer />
  </footer>
</template>
