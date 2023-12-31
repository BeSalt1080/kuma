<script setup>
import { ref, onMounted } from 'vue';
import { authService } from '@/api';

const products = ref([])

const fetchData = async () => {
    try {
        const response = await authService.get('/product_get');
        products.value = response.data;
        console.log(products)
        products.value.forEach(product => {
            console.log(product.name)
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const removeProduct = async (productId) => {
    try {
        console.log(productId)
        await authService.delete('/product', {
            data: { id: productId },
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
        fetchData()
    } catch (error) {
        console.error('Error deletinng data:', error);
    }
};

onMounted(() => {
    fetchData();
});
</script>

<template>
    <div class="container mx-auto">
        <div class="container mx-auto flex justify-between items-center">
            <h2 class="text-2xl font-bold mb-4 text-green-700">Product Index</h2>
            <router-link :to="{ name: 'product.create' }" class="btn-add-product">
                <i class="fas fa-plus mr-2"></i> Add Product
            </router-link>
        </div>
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white border border-green-300">
                <thead>
                    <tr>
                        <th class="py-3 px-6 text-left border-b text-green-700">No</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Image</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Product Name</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Description</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Price</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Sale</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Categories</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">SKU</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Color</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Stocks</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Brands</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Sizes</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Genders</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Created At</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(product, index) in products" :key="product.id">
                        <td class="py-4 px-6 border-b">{{ index + 1 }}</td>
                        <td class="py-4 px-6 border-b"><img :src="'/uploaded/'+product.image" :alt="product.image" /></td>
                        <td class="py-4 px-6 border-b">{{ product.name }}</td>
                        <td class="py-4 px-6 border-b">{{ product.description }}</td>
                        <td class="py-4 px-6 border-b">{{ product.price }}</td>
                        <td class="py-4 px-6 border-b">{{ product.sale }}</td>
                        <td class="py-4 px-6 border-b">{{ product.category }}</td>
                        <td class="py-4 px-6 border-b">{{ product.sku }}</td>
                        <td class="py-4 px-6 border-b">{{ product.color }}</td>
                        <td class="py-4 px-6 border-b">{{ product.stocks }}</td>
                        <td class="py-4 px-6 border-b">{{ product.brand }}</td>
                        <td class="py-4 px-6 border-b">{{ product.size }}</td>
                        <td class="py-4 px-6 border-b">{{ product.gender }}</td>
                        <td class="py-4 px-6 border-b">{{ product.created_at }}</td>
                        <td class="py-4 px-6 border-b">
                            <div class="flex items-center">
                                <router-link :to="{ name: 'product.edit', params: { id: product.id } }"
                                    class="text-green-500 hover:underline mr-2">
                                    Edit
                                </router-link>
                                <button @click="removeProduct(product.id)"
                                    class="text-red-500 hover:underline focus:outline-none">
                                    Remove
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<style>
.btn-add-product {
    padding: 8px 12px;
    background-color: #4caf50; /* Green color */
    color: #fff;
    text-decoration: none;
    border-radius: 4px;
    display: flex;
    align-items: center;
    transition: background-color 0.3s;
    border: 1px solid #4caf50; /* Solid border */
  }
  
  .btn-add-product:hover {
    background-color: #45a049; /* Darker green color on hover */
  }
  
  .btn-add-product i {
    margin-right: 6px;
  }</style>