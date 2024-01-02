<script setup>
import { RouterLink } from 'vue-router';
import SearchBar from './SearchBar.vue';
import DropdownLink from './DropdownLink.vue';
import Profile from './Profile.vue';
import WishlistIcon from './icons/WishlistIcon.vue';
import CartIcon from './icons/CartIcon.vue';


</script>

<template>
    <nav class="flex justify-between px-8 py-2 h-16 bg-white border-b items-center">
        <div class="flex justify-between w-4/12 items-center">
            <RouterLink to="/" class="select-none font-bold text-2xl">Kuma</RouterLink>
            <div class="flex gap-4 uppercase font-bold">
                <RouterLink :to="{name:'latest'}">latest</RouterLink>
                <DropdownLink title="Men">
                    <RouterLink class="px-5 py-2 hover:bg-green-400" to="/men/new-arrival">New
                        Arrival</RouterLink>
                    <RouterLink class="px-5 py-2 hover:bg-green-400" to="/men/footwear">Footwear
                    </RouterLink>
                    <RouterLink class="px-5 py-2 hover:bg-green-400" to="/men/aparrel">Aparrel
                    </RouterLink>
                </DropdownLink>
                <DropdownLink title="Women">
                    <RouterLink class="px-5 py-2 hover:bg-green-400" to="/women/new-arrival">New
                        Arrival</RouterLink>
                    <RouterLink class="px-5 py-2 hover:bg-green-400" to="/women/footwear">
                        Footwear</RouterLink>
                    <RouterLink class="px-5 py-2 hover:bg-green-400" to="/women/aparrel">Aparrel
                    </RouterLink>
                </DropdownLink>
                <DropdownLink title="Kids">
                    <RouterLink class="px-5 py-2 hover:bg-green-400" to="/kids/footwear">
                        Footwear</RouterLink>
                    <RouterLink class="px-5 py-2 hover:bg-green-400" to="/kids/aparrel">Aparrel
                    </RouterLink>
                </DropdownLink>
                <RouterLink to="/accessory">Accessories</RouterLink>
                <RouterLink to="/sale">Sale</RouterLink>
            </div>
        </div>
        <div class="flex gap-4">
            <SearchBar></SearchBar>
            <RouterLink :to="{name:'wishlist'}">
                <WishlistIcon height="24px" />
            </RouterLink>
            <RouterLink :to="{name:'cart'}">
                <CartIcon height="24px" />
            </RouterLink>
            <Profile></Profile>
        </div>
    </nav>
</template>