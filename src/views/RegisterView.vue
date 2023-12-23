<script setup>
import axios from 'axios'
import { ref } from 'vue';

const name = ref('');
const email = ref('');
const password = ref('');
const repassword = ref('');
const errors = ref('');

async function loginSubmit() {
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
    <div class="flex justify-center my-12">
        <div class="w-1/2 bg-slate-500 p-5">
            <h1 class="text-center text-3xl font-bold">CREATE AN ACCOUNT</h1>
            <form @submit.prevent="loginSubmit" class="">
                <div class="w-full">
                    <label for="">Full Name</label>
                    <input type="text" class="block w-full" v-model="name" id="">
                    <div class="text-red-300">{{ errors.name }}</div>
                </div>
                <div class="w-full">
                    <label for="">Email</label>
                    <input type="email" class="block w-full" v-model="email" id="">
                    <div class="text-red-300">{{ errors.email }}</div>
                </div>
                <div class="w-full">
                    <label for="">Password</label>
                    <input type="password" class="block w-full" v-model="password" id="">
                    <div class="text-red-300">{{ errors.password }}</div>
                </div>
                <div class="w-full">
                    <label for="">Confirm Password</label>
                    <input type="password" class="block w-full" v-model="repassword" id="">
                </div>
                <div>
                    <input type="checkbox" name="" id="">I have read and agree to the Terms and Condition that apply
                </div>
                <div>
                    <button class="px-2 py-3 bg-primary4" >Register</button>
                </div>
                <div>
                    Already a user? Login
                </div>
            </form>
        </div>
    </div>
</template>