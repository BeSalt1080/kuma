<script setup>
import { authService } from '@/api';
import PrimaryButton from '@/components/PrimaryButton.vue';
import { useAuthStore } from '@/stores/auth';
import UserLayout from '@/views/layouts/UserLayout.vue'
import { ref } from 'vue';

const store = useAuthStore()

const name = ref(store.user.name)
const error = ref('')
const password = ref('')
const changeEmail = ref('')
const email = ref(store.user.email)
const changePassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const msg = ref('')

const save = async () => {
    const form = {
        name: name.value,
        password: password.value,
        changeEmail: changeEmail.value,
        email: email.value,
        changePassword: changePassword.value,
        newPassword: newPassword.value
    }
    const response = await authService.put("/user", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
    }).then(response => {
        if (response.status == 200) {
            password.value = ''
            changeEmail.value =''
            changePassword.value = ''
            newPassword.value = ''
            msg.value = response.data
            setTimeout(() => { msg.value = '' }, 3000)
        }
        else {
            error.value = "Your pasword is incorrect"
            setTimeout(() => { error.value = '' }, 3000)
        }
    });
    return response;
}

</script>
<template>
    <UserLayout title="Account Information">
        <form @submit.prevent="save">
            <div class="flex flex-col w-1/2">
                <p class="bg-green-400 text-white font-bold p-5" v-if="msg">{{ msg }}</p>
                <p class="bg-red-400 text-white font-bold p-5" v-if="error">{{ error }}</p>
                <label class="font-bold" for="name">Fullname</label>
                <input v-model="name" id="name" type="text">
                <label class="flex my-2 items-center gap-5 w-fit" for="changeEmail"><input type="checkbox"
                        v-model="changeEmail" id="changeEmail">Change Email</label>
                <label class="flex my-2 items-center gap-5 w-fit" for="changePassword"><input type="checkbox"
                        v-model="changePassword" id="changePassword">Change Password</label>
                <label class="font-bold" v-if="changeEmail" for="email">Email</label>
                <input v-if="changeEmail" v-model="email" type="text" id="email">
                <label class="font-bold" for="email">Current Password</label>
                <input v-model="password" type="password" id="email">
                <label class="font-bold" v-if="changePassword" for="newPassword">New Password</label>
                <input v-if="changePassword" v-model="newPassword" type="password" id="newPassword">
                <label class="font-bold" v-if="changePassword" for="confirmPassword">Confirm New Password</label>
                <input v-if="changePassword" v-model="confirmPassword" type="password" id="confirmPassword">
                <PrimaryButton class="mt-3">Save</PrimaryButton>
            </div>
        </form>
    </UserLayout>
</template>