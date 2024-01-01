<script setup>
import { authService } from '@/api';
import { ref, onMounted } from 'vue';
import router from '@/router'

const route = router.currentRoute

const product = ref('')
console.log(route.value.params.id);
const fetchData = async () => {
    try {
        const response = await authService.get('/product_get',
            {
                params: { id: route.value.params.id },
                header: { "Content-Type": "application/x-www-form-urlencoded" }
            });
        product.value = response.data[0];
        console.log(product.value)
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};
onMounted(() => {
    fetchData();
});
</script>
<template>
    <div class="">
        <span>Home / {{ product.gender }} / {{ product.category }}</span>
        <div class="flex">
            <img :src="'/uploaded/' + product.image" :alt="product.image" />
            {{ product.name }}
            {{ product.description }}
            {{ product.price }}
            {{ product.sale }}
            {{ product.category }}
            {{ product.sku }}
            {{ product.color }}
            {{ product.stocks }}
            {{ product.brand }}
            {{ product.size }}
            {{ product.gender }}
            {{ product.created_at }}
        </div>
    </div>
</template>