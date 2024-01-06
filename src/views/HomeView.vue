<script setup>
import Carousel from '@/components/Carousel.vue';
import { ref } from 'vue';

const images = ref([
  '/images/banner1.webp',
  '/images/banner2.webp',
  '/images/banner3.webp',
  '/images/banner4.webp',
  '/images/banner5.webp',
  '/images/banner6.webp',
  '/images/banner7.webp',
]);

</script>

<template>
  <Carousel :images="images"/>
</template>
