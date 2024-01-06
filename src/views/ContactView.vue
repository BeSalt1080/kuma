<script setup>
import PrimaryButton from '@/components/PrimaryButton.vue';
import CompanyLayout from './layouts/CompanyLayout.vue';
import { ref } from 'vue';

const msg = ref('')
const name = ref('')
const email = ref('')
const phone = ref('')
const message = ref('')

const isLoading = ref(false)
const send = async () => {
    isLoading.value = true
    setTimeout(() => {
        isLoading.value = false
        name.value = ''
        email.value = ''
        phone.value = ''
        message.value = ''
        msg.value = "Message Sent Successfully"
        setTimeout(() => { msg.value = '' }, 3000)
    }, 500);
}

</script>

<template>
    <CompanyLayout title="Contact Us" path="Contact Us">
        <form action="" @submit.prevent="send()">
            <p class="bg-green-400 text-white font-bold p-5 w-3/4 mb-5" v-if="msg">{{ msg }}</p>
            <div class="flex flex-col">
                <label class="font-bold" for="name">Full Name</label>
                <input v-model="name" class="mb-5 w-3/4 border border-black py-1" id="name" type="text" required>
                <label class="font-bold" for="email">Email Address</label>
                <input v-model="email" class="mb-5 w-3/4 border border-black py-1" id="email" type="email" required>
                <label class="font-bold" for="phone">Phone number (Optional)</label>
                <input v-model="phone" class="mb-5 w-3/4 border border-black py-1" id="phone" type="text">
                <label class="font-bold" for="message">Message</label>
                <textarea v-model="message" class="mb-5 w-3/4 border border-black py-1" name="" id="message" cols="30" rows="10" required></textarea>
                <PrimaryButton class="w-3/4" :class="{'disabled bg-gray-700 hover:bg-gray-700 cursor-not-allowed':isLoading}">Send Message</PrimaryButton>
            </div>
        </form>
    </CompanyLayout>
</template>
