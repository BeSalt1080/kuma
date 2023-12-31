<script setup>
import { authService } from '@/api';
import DropdownLink from '@/components/DropdownLink.vue';
import Product from '@/components/Product.vue'
import { ref, onMounted } from 'vue';


const products = ref([])
defineProps({
    category: String
})


const fetchData = async () => {
    try {
        const response = await authService.get('/product_get');
        products.value = response.data;
        console.log(products.value)

    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

onMounted(() => {
    fetchData();
});

</script>
<template>
    <div class="p-5">
        <h1 class="text-center text-xl font-bold">{{ category }}</h1>
        <div class="flex gap-5">
            <div class="">
                <div class="border-b-black border-b">
                    Home / {{ category }} / {{ $route.params.categories }}
                </div>
                <DropdownLink title="Brand">

                </DropdownLink>
                <DropdownLink title="Category">
                    
                </DropdownLink>
                <DropdownLink title="Gender">
                    
                </DropdownLink>
                <DropdownLink title="Size">
                    
                </DropdownLink>
                <DropdownLink title="Price">
                    
                </DropdownLink>
            </div>
            <div class="grid grid-cols-3 gap-20 mx-20 w-3/4">
                <Product v-for="product in products" :brand="product.brand" :name="product.name" :image="product.image" :price=product.price :id=product.id />
            </div>
        </div>
    </div>
</template>