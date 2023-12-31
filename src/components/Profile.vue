<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth.js'
import ProfileIcon from './icons/ProfileIcon.vue';
const isHovered = ref(0);

const store = useAuthStore()

async function logout(){
    store.logoutUser()
}

</script>
<template>
    <div @mouseover="isHovered = true" @mouseleave="isHovered = false">
        <div class="cursor-pointer flex gap-1">
            <ProfileIcon height="24px" />
        </div>
        <div class="absolute pt-5" v-show="isHovered">
            <div class="border bg-white -translate-x-20 py-5 text-sm shadow-md" >
                <div v-if="!store.isLoggedIn">
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/login">
                        Login
                    </RouterLink>
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/register">
                        Register
                    </RouterLink>
                    <a class="px-4 block hover:bg-slate-400 transition-all ease-in-out cursor-pointer" @click="logout">
                        Log Out
                    </a>
                </div>
                <div v-else>
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/account">
                        My Account
                    </RouterLink>
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/orders">
                        My Orders
                    </RouterLink>
                    <RouterLink class="px-4 block hover:bg-slate-400 transition-all ease-in-out" to="/adress">
                        Address Book
                    </RouterLink>
                    <a class="px-4 block hover:bg-slate-400 transition-all ease-in-out cursor-pointer" @click="logout">
                        Log Out
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>