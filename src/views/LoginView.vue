<script setup>
import { useAuthStore } from '../stores/auth.js'
import { RouterLink } from 'vue-router';
import { ref } from 'vue';

const store = useAuthStore()

const email = ref('')
const password = ref('')
const errors = ref('');

async function login() {
    const form = {
        email: email.value,
        password: password.value
    }
    await store.loginUser(form)
        .then(result => {
            if(!result.error) 
            {
                errors.value = ""
            }
            else errors.value = result.error
            password.value = ""
        })
}
</script>
<template>
    <div class="flex justify-center items-center h-full w-full font-semibold text-gray-600">
        <div class="w-96 bg-white rounded-sm p-5 flex flex-col gap-6 shadow-lg border-2 border-green-400">
            <h1 class="text-center text-3xl font-bold text-black">Login</h1>
            <form @submit.prevent="login" class="flex-col justify-center gap-1 flex">
                <div class="w-full">
                    <label for="">Email</label>
                    <input type="email" class="w-full border-gray-400 rounded-md" v-model="email" name="" id="">
                    <div class="text-red-300">{{ errors.email }}</div>

                </div>
                <div class="w-full">
                    <label for="password">Password</label>
                    <input type="password" class="w-full border-gray-400 rounded-md" v-model="password" name="password" id="password">
                    <div class="text-red-300">{{ errors.password }}</div>
                </div>
                <button class="p-2 rounded-md font-semi my-5 bg-gray-200 hover:text-black hover:bg-green-400">Login</button>

                <div class="flex flex-col gap-1 w-fit">
                    <RouterLink to="/register" class="text-green-500 hover:text-green-600 cursor-pointer">
                        Forgot Password?
                    </RouterLink>
                    <div class="border-t-2 border-gray-400"></div>
                    <p>Don't have an account? <RouterLink to="/register" class="text-green-500 hover:text-green-600 cursor-pointer">Register</RouterLink></p>
                </div>
            </form>
        </div>
    </div>
</template>