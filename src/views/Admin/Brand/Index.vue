<script setup>
import { ref, onMounted } from 'vue';
import { authService } from '@/api';

const brands = ref([]);

const fetchData = async () => {
    try {
        const response = await authService.get('/brand_get');
        brands.value = response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const removeBrand = async (brandId) => {
    try {
        console.log(brandId)
        await authService.delete('/brand', {
            data: { id: brandId },
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
            <h2 class="text-2xl font-bold mb-4 text-green-700">Brand Index</h2>
            <router-link :to="{ name: 'brand.create' }" class="btn-add-brand">
                <i class="fas fa-plus mr-2"></i> Add Brand
            </router-link>
        </div>
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white border border-green-300">
                <thead>
                    <tr>
                        <th class="py-3 px-6 text-left border-b text-green-700">No</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Brand Name</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(brand, index) in brands" :key="brand.id">
                        <td class="py-4 px-6 border-b">{{ index + 1 }}</td>
                        <td class="py-4 px-6 border-b">{{ brand.name }}</td>
                        <td class="py-4 px-6 border-b">
                            <div class="flex items-center">
                                <router-link :to="{ name: 'brand.edit', params: { id: brand.id } }"
                                    class="text-green-500 hover:underline mr-2">
                                    Edit
                                </router-link>
                                <button @click="removeBrand(brand.id)"
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
.btn-add-brand {
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
  
  .btn-add-brand:hover {
    background-color: #45a049; /* Darker green color on hover */
  }
  
  .btn-add-brand i {
    margin-right: 6px;
  }</style>