<script setup>
import { RouterLink } from 'vue-router';

defineProps({
    id:Number,
    name: String,
    brand: String,
    price: Number,
    image: String
});
</script>

<template>
  <div class="p-4 max-w-md mx-auto">
    <div class="flex items-center justify-center overflow-hidden  mb-4 border border-gray-300">
      <img class="w-full h-full object-cover" :src="'/uploaded/' + image" :alt="image">
    </div>
    <div class="text-center">
      <div class="text-gray-600">{{ brand }}</div>
      <RouterLink :to="{name:'product.show',params:{id:id}}" class="font-semibold text-lg text-black">
        {{ name.length > 20 ? name.slice(0, 30) + '-…' : name }}
      </RouterLink>
      <div class="text-green-800 font-bold">
        {{ new Intl.NumberFormat('in-ID', { style: 'currency', currency: 'IDR' }).format(price) }}
      </div>
    </div>
  </div>
</template>
