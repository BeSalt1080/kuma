<script setup >
    
defineProps({
    id:Number,
    name: String,
    type: String,
});
</script>

<template>
<button class="bg-green-500 text-white p-2 rounded-md hover:bg-green-400 active:bg-green-500 hover:text-gray-700 transition-colors duration-300" :type="type" :name="name">
    <slot/>
</button>
</template>