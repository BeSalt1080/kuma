<script setup>
import { RouterLink } from 'vue-router'
</script>
<template>
    <div class="flex justify-center bg-green-500 text-gray-700">
        <div class="flex justify-center w-5/6 p-10">
            <div class="w-1/2">
                <RouterLink class="block" to="/about">About Us</RouterLink>
                <RouterLink class="block" to="/policy">Privacy Policy</RouterLink>
                <RouterLink class="block" to="/terms">Terms & Condition</RouterLink>
                <RouterLink class="block" to="/contact">Contact Us</RouterLink>
            </div>
            <div class="w-1/2 flex">
                <div class="w-1/2">
                    We Accept
                </div>
                <div class="w-1/2">
                    <h1>Connect With Us</h1>
                    <i class="fa fa-facebook"></i>

                </div>
            </div>

        </div>
    </div>
</template>