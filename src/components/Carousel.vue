<script setup>
import { ref, toRef } from 'vue';

const currentIndex = ref(0)
const isHovered = ref(false)
const previous = ref(false)
const next = ref(false)

const props = defineProps({
  images: {
    type: Array,
    required: true,
  }
})


const prevImage = () => {
  currentIndex.value = (currentIndex.value - 1 + props.images.length) % props.images.length;
}
const nextImage = () => {
  currentIndex.value = (currentIndex.value + 1) % props.images.length;
}

</script>

<template>
  <div class="relative overflow-hidden" @mouseover="isHovered = true" @mouseleave="isHovered = false">
    <div v-for="(image, index) in images" :key="index" :class="{ 'hidden': index !== currentIndex}">
      <img :src="image" alt="carousel-image" class="w-full" />
    </div>
    <div class="flex justify-center">
      <div class="absolute top-1/2 -translate-y-1/2 flex justify-between z-10 ease-in-out transition-all"
        :class="{ 'w-[95%]': isHovered, 'w-[120%]': !isHovered }">
        <button @click="prevImage" class="bg-[rgba(0,0,0,0.3)] p-2 border-0 text-white text-3xl cursor-pointer"><i
            class="fa-solid fa-chevron-left"></i></button>
        <button @click="nextImage" class="bg-[rgba(0,0,0,0.3)] p-2 border-0 text-white text-3xl cursor-pointer"><i
            class="fa-solid fa-chevron-right"></i></button>
      </div>
    </div>
  </div></template>
