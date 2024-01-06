<script setup>
import { object, string } from 'yup';
import PrimaryButton from '@/components/PrimaryButton.vue';
import { useAuthStore } from '../stores/auth.js'
import { RouterLink, useRouter } from 'vue-router';
import { ref } from 'vue';

const store = useAuthStore()
const router = useRouter()
const email = ref('')
const password = ref('')
const errors = ref({});

async function login() {
    errors.value ={}
    const form = {
        email: email.value,
        password: password.value
    }

    let userSchema = object({
        email: string().email().required(),
        password: string().required()
    }, { strict: true });

    try {
        await userSchema.validate(form, { abortEarly: false }).then(async () => {
            const response = await store.loginUser(form)
            if (response.status == 200) {
                store.isLoggedIn = true
                router.push({name:'home'})
            }
            if (response.status == 422) {
                errors.value.message = 'Incorrect email address or password.'
            }
        })
    }
    catch (error) {
        if (error.inner.some((e) => e.path === 'email')) {
            errors.value.email = error.inner.find((e) => e.path === 'email').message;
        } else {
            errors.value.email = '';
        }

        if (error.inner.some((e) => e.path === 'password')) {
            errors.value.password = error.inner.find((e) => e.path === 'password').message;
        } else {
            errors.value.password = '';
        }
    }
}
</script>
<template>
    <div class="flex justify-center items-center h-[calc(100dvh-64px)] w-full font-semibold text-gray-600">
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
                    <input type="password" class="w-full border-gray-400 rounded-md" v-model="password" name="password"
                        id="password">
                    <div class="text-red-300">{{ errors.password }}</div>
                </div>

                <PrimaryButton class="mt-5" type="submit">Login</PrimaryButton>
                <!-- <button class="p-2 rounded-md font-semi my-5 bg-gray-200 hover:text-black hover:bg-green-400">Login</button> -->
                <div class="text-red-300">{{ errors.message }}</div>

                <div class="flex flex-col gap-1 w-fit">
                    <RouterLink to="/register" class="text-green-500 hover:text-green-600 cursor-pointer">
                        Forgot Password?
                    </RouterLink>
                    <div class="border-t-2 border-gray-400"></div>
                    <p>Don't have an account? <RouterLink to="/register"
                            class="text-green-500 hover:text-green-600 cursor-pointer">Register</RouterLink>
                    </p>
                </div>
            </form>
        </div>
    </div>
</template>