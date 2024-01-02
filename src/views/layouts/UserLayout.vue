<script setup>

defineProps({
    title:String
})

</script>
<template>
    <div class="w-1/2 mx-auto mt-10">
        <h1 class="font-bold text-3xl">{{title}}</h1>
    </div>
    <div class="mx-auto w-5/6 flex p-10">
        <div class="flex flex-col w-3/12 text-2xl">
            <router-link class="border-y" :to="{name:'account'}"><i class="me-2 fas fa-regular fa-user"></i>My Account</router-link>
            <router-link class="border-y" :to="{name:'order'}"><i class="me-2 fas fa-solid fa-file-invoice"></i>My Order</router-link>
            <router-link class="border-y" :to="{name:'address'}"> <i class="me-2 fas fa-address-book"></i>Address Book</router-link>
            <router-link class="border-y text-xl" :to="{name:'account.info'}"><i class="me-2 fa-solid fa-circle-info"></i>Account Information</router-link>
            <router-link class="border-y" :to="{name:'wishlist'}"><i class="me-2 fas fa-heart"></i>My Wishlist</router-link>
        </div>
        <div class="w-full">
            <slot/>
        </div>
    </div>
</template>