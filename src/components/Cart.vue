<script setup>
import { ref } from 'vue';
import CartIcon from './icons/CartIcon.vue';
const isHovered = ref(0);

</script>
<template>
    <div @mouseover="isHovered = true" @mouseleave="isHovered=false">
        <div class="cursor-pointer flex gap-1">
            <CartIcon height="24px" />
        </div>
        <div class="absolute pt-5" v-show="isHovered">
            <div class="border bg-white -translate-x-5 py-5 text-sm shadow-md">
                
                <slot />
            </div>
        </div>
    </div>
</template>