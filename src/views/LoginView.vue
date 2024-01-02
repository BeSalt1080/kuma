<script setup>
import { object, string } from 'yup';
import PrimaryButton from '@/components/PrimaryButton.vue';
import { useAuthStore } from '../stores/auth.js'
import { RouterLink, useRouter } from 'vue-router';
import { ref } from 'vue';
import { HttpStatusCode } from 'axios';

const store = useAuthStore()

const email = ref('')
const password = ref('')
const errors = ref('');

async function login() {
    errors.email = ''
    errors.password = ''
    
    const form = {
        email: email.value,
        password: password.value
    }

    let userSchema = object({
        email: string().email(),
        password: string(), 
    }, { strict: true });

    const user = await userSchema.validate(form).then(async()=>{
        var response = await store.loginUser(form);
        console.log(response);
        if(response.status === HttpStatusCode.Ok)
        {
            router.push({name: 'home'});
        }
    }).catch(error =>{
        console.error(error);

        if (error.name === 'ValidationError') {
            // Handle validation errors
            error.inner.forEach((validationError) => {
                errors[validationError.path] = validationError.message;
            });
        } else {
            // Handle other errors (e.g., login error)
            // You may want to display a generic error message to the user
        }
    });
}
</script>
<template>
    <div class="flex justify-center items-center min-h-dvh w-full font-semibold text-gray-600">
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

                <PrimaryButton class="my-5" type="submit">Login</PrimaryButton>
                <!-- <button class="p-2 rounded-md font-semi my-5 bg-gray-200 hover:text-black hover:bg-green-400">Login</button> -->

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