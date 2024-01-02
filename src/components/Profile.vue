<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth.js'
import ProfileIcon from './icons/ProfileIcon.vue';
import router from '../router';
const isHovered = ref(0);

const store = useAuthStore()

async function logout(){
    store.logoutUser()
    router.push('login');
}

</script>
<template>
    <div class="overflow-x-clip" @mouseover="isHovered = true" @mouseleave="isHovered = false">
        <div class="cursor-pointer flex gap-1">
            <ProfileIcon height="24px" />
        </div>
        <div class="absolute w-full p-5" v-show="isHovered">
            <div class="border bg-white -translate-x-20 py-2 text-sm shadow-md font-semibold" >
                <div v-if="!store.isLoggedIn">
                    <RouterLink class="px-4 block p-2 hover:bg-green-400 transition-all ease-in-out" to="/login">
                        Login
                    </RouterLink>
                    <RouterLink class="px-4 block p-2 hover:bg-green-400 transition-all ease-in-out" to="/register">
                        Register
                    </RouterLink>
                </div>
                <div v-else>
                    <RouterLink class="px-4 block p-2 hover:bg-green-400 transition-all ease-in-out" :to="{name:'account'}">
                        My Account
                    </RouterLink>
                    <RouterLink class="px-4 block p-2 hover:bg-green-400 transition-all ease-in-out" :to="{name:'order'}">
                        My Orders
                    </RouterLink>
                    <RouterLink class="px-4 block p-2 hover:bg-green-400 transition-all ease-in-out" :to="{name:'address'}">
                        Address Book
                    </RouterLink>
                    <a class="px-4 block p-2 hover:bg-green-400 transition-all ease-in-out cursor-pointer" @click="logout">
                        Log Out
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>