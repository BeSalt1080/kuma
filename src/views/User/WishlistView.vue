<script setup>
import { authService } from '@/api';
import Product from '@/components/Product.vue';
import UserLayout from '@/views/layouts/UserLayout.vue'
import { onMounted, ref } from 'vue';
import { RouterLink } from 'vue-router';

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

const wishlist = async (id) => {
    try {
        console.log(id);
        await authService.delete('/wishlist', {
            data: { id: id },
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
        fetchData()
    } catch (error) {
        console.error('Error deletinng data:', error);
    }
    fetchData()
}

onMounted(() => {
    fetchData()
})
</script>
<template>
    <UserLayout title="Wishlist">
        <div class="grid grid-cols-3 gap-20 w-full">
            <template v-for="product in products">
                <div class="" v-if="product.wishlist.length > 0">
                    <Product :brand="product.brand" :name="product.name" :image="product.image" :price=product.price
                        :id=product.id :sale="product.sale" />
                    <RouterLink :to="{ name: 'product.show', params: { id: product.id } }"
                        class="p-4 block text-center bg-green-400 hover:bg-green-300 rounded-lg w-full">
                        <i class="fas fa-shopping-cart"></i> Add to Cart
                    </RouterLink>
                    <div class="relative -top-[89%] left-[85%] w-fit cursor-pointer hover:text-slate-500"
                        @click="wishlist(product.wishlist[0])">
                        <i class="fas fa-close text-3xl"></i>
                    </div>
                </div>
            </template>
        </div>
    </UserLayout>
</template>