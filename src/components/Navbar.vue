<script setup>
import { RouterLink } from 'vue-router';
import CartIcon from './icons/CartIcon.vue';
import ProfileIcon from './icons/ProfileIcon.vue';
import WishlistIcon from './icons/WishlistIcon.vue';
import SearchBar from './SearchBar.vue';
import DropdownLink from './DropdownLink.vue';
</script>

<template>
    <nav class="flex justify-between px-8 py-2 h-16 bg-gray-400 items-center">
        <div class="flex justify-between w-4/12 items-center">
            <RouterLink to="/" class="select-none font-bold text-2xl">Kuma</RouterLink>
            <div class="flex gap-4 uppercase font-bold">
                <div>latest</div>
                <DropdownLink title="Men">
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/men/new-arrival">New Arrival</RouterLink>
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/men/footwear">Footwear</RouterLink>
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/men/aparrel">Aparrel</RouterLink>
                </DropdownLink>
                <DropdownLink title="Women">
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/women/new-arrival">New Arrival</RouterLink>
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/women/footwear">Footwear</RouterLink>
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/women/aparrel">Aparrel</RouterLink>
                </DropdownLink>
                <DropdownLink title="Kids">
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/kids/footwear">Footwear</RouterLink>
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/kids/aparrel">Aparrel</RouterLink>
                </DropdownLink>
                <div>Accessories</div>
                <div>Sale</div>
            </div>
        </div>
        <div class="flex gap-4">
            <SearchBar></SearchBar>
            <div>
                <WishlistIcon height="24px"/>
            </div>
            <div>
                <CartIcon height="24px" />
            </div>
            <div>
            <ProfileIcon height="24px" />
        </div>
    </div>
</nav></template>