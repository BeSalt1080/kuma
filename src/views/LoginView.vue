<script setup>
import { useAuthStore } from '../stores/auth.js'
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
    <div class="flex justify-center my-12">
        <div class="w-1/2 bg-surface p-5">
            <h1 class="text-center text-3xl font-bold">Welcome</h1>
            <form @submit.prevent="login" class="">
                <div class="w-full">
                    <label for="">Email</label>
                    <input type="email" class="block w-full" v-model="email" name="" id="">
                    <div class="text-red-300">{{ errors.email }}</div>

                </div>
                <div class="w-full">
                    <label for="">Password</label>
                    <input type="password" class="block w-full" v-model="password" name="" id="">
                    <div class="text-red-300">{{ errors.password }}</div>
                </div>
                <div>
                    <button class="px-2 py-3 bg-primary4">Login</button>
                </div>
            </form>
        </div>
    </div>
</template>