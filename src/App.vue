<script setup>
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue';
import Footer from './components/Footer.vue';
import router from './router';

const currentpath = router.currentRoute 

</script>

<template>
  <header v-if="!currentpath.fullPath.startsWith('/dashboard')">
    <Navbar />
  </header>
  <main class="min-h-screen">
    <RouterView />
  </main>
  <footer v-if="!currentpath.fullPath.startsWith('/dashboard')">
    <Footer />
  </footer>
</template>
