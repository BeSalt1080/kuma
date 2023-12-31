<script setup>

import Profile from '@/components/Profile.vue';
</script>
  
<template>
    <div class="flex min-h-screen bg-gray-100">
        <!-- Sidebar -->
        <div class="w-64 bg-green-500 p-4">
            <!-- Sidebar Header -->
            <div class="text-white font-bold text-3xl mb-4 border-b-2 border-b-green-600 text-center pb-4">KumaAdmin</div>
            <!-- Sidebar Sections -->
            <router-link :to="{ name: 'banner' }" class="sidebar-link" :class="{ 'active': currentRoute === 'banner' }">
                <i class="fas fa-image mr-2"></i> Banners
            </router-link>
            <router-link :to="{ name: 'brand' }" class="sidebar-link" :class="{ 'active': currentRoute === 'brand' }">
                <i class="fas fa-building mr-2"></i> Brands
            </router-link>
            <router-link :to="{ name: 'category' }" class="sidebar-link" :class="{ 'active': currentRoute === 'category' }">
                <i class="fas fa-list-alt mr-2"></i> Category
            </router-link>
            <router-link :to="{ name: 'gender' }" class="sidebar-link" :class="{ 'active': currentRoute === 'gender' }">
                <i class="fas fa-venus-mars mr-2"></i> Gender
            </router-link>
            <router-link :to="{ name: 'size' }" class="sidebar-link" :class="{ 'active': currentRoute === 'size' }">
                <i class="fas fa-expand mr-2"></i> Size
            </router-link>
            <router-link :to="{ name: 'payment' }" class="sidebar-link" :class="{ 'active': currentRoute === 'payment' }">
                <i class="fas fa-credit-card mr-2"></i> Payment
            </router-link>
            <router-link :to="{ name: 'shipping' }" class="sidebar-link" :class="{ 'active': currentRoute === 'shipping' }">
                <i class="fas fa-truck mr-2"></i> Shipping
            </router-link>
            <router-link :to="{ name: 'product' }" class="sidebar-link" :class="{ 'active': currentRoute === 'product' }">
                <i class="fas fa-box mr-2"></i> Product
            </router-link>
            <router-link :to="{ name: 'order' }" class="sidebar-link" :class="{ 'active': currentRoute === 'order' }">
                <i class="fas fa-shopping-cart mr-2"></i> Order
            </router-link>

        </div>
        <div class="flex-1">
            <!-- Navbar -->
            <header class="flex justify-between items-center bg-white p-4 mb-10">
                <!-- Your existing title and add-category button code -->
                <router-link :to="{ name:'home'}">Go back to site</router-link>
                <!-- User Dropdown -->
                <Profile class="float-right"/>
            </header>

            <!-- Content goes here -->
            <router-view />
        </div>
    </div>
</template>
  
<style scoped>
.sidebar-link {
    display: block;
    padding: 8px;
    margin-bottom: 4px;
    color: #fff;
    text-decoration: none;
    transition: background-color 0.3s;
}

.sidebar-link:hover,
.sidebar-link.active {
    background-color: rgba(255, 255, 255, 0.1);
}

/* Add any additional styling specific to this component */
</style>