<script setup>
import { authService } from '@/api';
import Product from '@/components/Product.vue';
import UserLayout from '@/views/layouts/UserLayout.vue'
import { onMounted, ref } from 'vue';

const products = ref([])

const fetchData = async () => {
    try {
        const response = await authService.get('/product_get',
            {
                header: { "Content-Type": "application/x-www-form-urlencoded" }
            });
        products.value = response.data.filter(product => {
            return product.wishlist != null
        })
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

onMounted(() => {
    fetchData()
})
</script>
<template>
    <UserLayout>
        <div class="grid grid-cols-3 gap-20 mx-20 w-5/6">
            <Product v-for="product in products" :brand="product.brand" :name="product.name" :image="product.image"
                :price=product.price :id=product.id />
        </div>
    </UserLayout>
</template>