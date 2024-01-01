<script setup>
import axios from 'axios'
import { ref } from 'vue';

const name = ref('');
const email = ref('');
const password = ref('');
const repassword = ref('');
const errors = ref('');

async function register() {
    errors.value = ''
    await axios.post('http://127.0.0.1:5000/register', {
        name: name.value,
        email: email.value,
        password: password.value,
        repassword: repassword.value
    }, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).catch((error='')=>{
        if(!error=='')
        errors.value = error.response.data.error
    }); 
}
</script>
<template>
    <div class="flex justify-center items-center w-full min-h-dvh  font-semibold text-gray-600">
        <div class="w-96 bg-white rounded-sm p-5 flex flex-col gap-6 shadow-lg border-2 border-green-400">
            <h1 class="text-center text-3xl font-bold text-black">CREATE AN ACCOUNT</h1>

            <form @submit.prevent="register" class="">
                <div class="w-full">
                    <label for="">Full Name</label>
                    <input type="text" class="w-full border-gray-400 rounded-md" v-model="name" id="">
                    <div class="text-red-300">{{ errors.name }}</div>
                </div>
                <div class="w-full">
                    <label for="">Email</label>
                    <input type="email" class="w-full border-gray-400 rounded-md" v-model="email" id="">
                    <div class="text-red-300">{{ errors.email }}</div>
                </div>
                <div class="w-full">
                    <label for="">Password</label>
                    <input type="password" class="w-full border-gray-400 rounded-md" v-model="password" id="">
                    <div class="text-red-300">{{ errors.password }}</div>
                </div>
                <div class="w-full">
                    <label for="">Confirm Password</label>
                    <input type="password" class="w-full border-gray-400 rounded-md" v-model="repassword" id="">
                </div>
                <div class="mt-5">
                    <input type="checkbox" name="agreement" id="agreement">
                <label for="agreement" class="select-none">
                    I have read and agree to the Terms and Condition that apply
                </label>
                </div>
                <button class="p-2 rounded-md font-semi my-5 bg-gray-200 hover:text-black hover:bg-green-400 w-full" >Register</button>

                <div class="flex flex-col gap-1 w-fit">
                    <RouterLink to="/login" class="text-green-500 hover:text-green-600 cursor-pointer">
                        Forgot Password?
                    </RouterLink>
                    <div class="border-t-2 border-gray-400"></div>
                    <p>Already have an account? <RouterLink to="/login" class="text-green-500 hover:text-green-600 cursor-pointer">Login</RouterLink></p>
                </div>
            </form>
        </div>
    </div>
</template>