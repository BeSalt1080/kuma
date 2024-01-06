<script setup>
import { ref } from 'vue';
import DropdownIcon from './icons/DropdownIcon.vue'

const isHovered = ref(0);

defineProps({
    title: String,
    content: Array
});
</script>
<template>
    <div @mouseover="isHovered = true" @mouseleave="isHovered=false">
        <div class="cursor-pointer flex gap-1">
            {{ title }}<DropdownIcon width="24px"/>
        </div>
        <div class="absolute pt-5 z-10" v-show="isHovered">
            <div class="border bg-white -translate-x-5 py-5 text-sm shadow-md flex flex-col">
                <slot/>
            </div>
        </div>
    </div>
</template>