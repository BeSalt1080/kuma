<script setup>

defineProps({
    title: String,
    path: String
})

</script>
<template>
    <div class="w-1/2 mx-auto mt-10">
        <h1 class="font-bold text-4xl text-center">{{ title }}</h1>
    </div>
    <div class="mx-auto w-5/6 flex p-10">
        <div class="flex flex-col w-3/12 text-2xl">
            <p class="text-lg border-b border-black select-none"><RouterLink class="cursor-pointer" :to="{name:'home'}">Home </RouterLink> / {{ path }}</p>
            <RouterLink class="border-b border-black py-3 font-bold" to="/policy">Privacy Policy</RouterLink>
            <RouterLink class="border-b border-black py-3 font-bold" to="/terms">Terms & Condition</RouterLink>
            <RouterLink class="border-b border-black py-3 font-bold" to="/contact">Contact Us</RouterLink>
        </div>
        <div class="w-full p-5 px-10">
            <slot />
        </div>
    </div>
</template>