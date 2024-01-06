<script setup>
import UserLayout from '@/views/layouts/UserLayout.vue'
</script>
<template>
    <UserLayout title="My Account">
        <div class="grid grid-cols-2 gap-10">
            <div>
                <h1 class="text-xl">Address Book</h1>
                <hr>
                <router-link :to="{name:'address'}">Edit</router-link>
            </div>
            <div class="flex flex-col gap-1">
                <h1 class="text-xl">Account Information</h1>
                <hr>
                <router-link :to="{name:'address'}">Contact Information</router-link>
                <router-link :to="{name:'account.info'}">Account Detail</router-link>
                <div class="inline">
                    <router-link :to="{name:'account.info'}">Edit</router-link>|<router-link :to="{name:'account.info'}">Change Password</router-link>
                </div>
            </div>
        </div>

    </UserLayout>
</template>