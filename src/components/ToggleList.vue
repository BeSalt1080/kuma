<script setup>
import { ref } from 'vue';
const isToggled = ref(true);

defineProps({
    title: String
});
</script>
<template>
    <div class="pb-1">
        <div>
            <div class="cursor-pointer flex gap-1 justify-between text-xl font-bold pt-1 pb-2" @click="isToggled = !isToggled">
                {{ title }}<i class="fa-solid self-center"
                    :class="{ 'fa-chevron-up': isToggled, 'fa-chevron-down': !isToggled }"></i>
            </div>
            <div class="" v-show="isToggled">
                <slot />
            </div>
        </div>
    </div>
</template>