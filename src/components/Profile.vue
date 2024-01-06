<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth.js'
import ProfileIcon from './icons/ProfileIcon.vue';
import { useRouter } from 'vue-router';


const router = useRouter()

const isHovered = ref(0);

const store = useAuthStore()

async function logout(){
    await store.logoutUser()
    router.push({name:'login'});
}

</script>
<template>
    <div class="overflow-x-clip" @mouseover="isHovered = true" @mouseleave="isHovered = false">
        <div class="cursor-pointer flex gap-1">
            <ProfileIcon height="24px" />
        </div>
        <div class="absolute w-40 pt-5 z-50 right-0" v-show="isHovered">
            <div class="border bg-white py-2 text-sm shadow-md font-semibold" >
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