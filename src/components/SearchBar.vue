<script setup>
import SearchIcon from './icons/SearchIcon.vue';
</script>
<template>
    <div class="flex items-center gap-1">
        <SearchIcon height="24px" />
        <input class=" p-4 rounded-2xl h-8 appearance-none focus:border-green-500" type="text" placeholder="Search">
    </div>
</template>