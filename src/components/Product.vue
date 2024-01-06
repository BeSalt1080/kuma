<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  id: Number,
  name: String,
  brand: String,
  price: Number,
  image: String,
  sale: Number,
});
</script>

<template>
  <div class="p-4 max-w-md mx-auto">
    <RouterLink :to="{ name: 'product.show', params: { id: id } }">
      <div class="flex items-center justify-center overflow-hidden  mb-4 border border-gray-300">
        <img class="w-full h-full object-cover" :src="'/uploaded/' + image" :alt="image">
      </div>
      <div class="text-center">
        <div class="text-gray-600">{{ brand }}</div>
        <div class="font-semibold text-lg text-black">
          {{ name.length > 20 ? name.slice(0, 30) + '-…' : name }}
        </div>
        <div class="text-green-800 font-bold" v-if="sale == 0">
          {{ new Intl.NumberFormat('in-ID', { style: 'currency', currency: 'IDR' }).format(price) }}
        </div>
        <div class="text-green-800 font-bold" v-else>
          {{ new Intl.NumberFormat('in-ID', { style: 'currency', currency: 'IDR' }).format(price*(sale/100)) }}
          <sup class="line-through">{{ new Intl.NumberFormat('in-ID', { style: 'currency', currency: 'IDR' }).format(price) }}</sup>
        </div>
      </div>
    </RouterLink>
  </div>
</template>
