<script setup>
import { ref, onMounted } from 'vue';
import { authService } from '@/api';

const services = ref([]);

const fetchData = async () => {
    try {
        const response = await authService.get('/shipping_get');
        services.value = response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const removeShipping = async (shippingId) => {
    try {
        await authService.delete('/shipping', {
            data: { id: shippingId },
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
            <h2 class="text-2xl font-bold mb-4 text-green-700">Shipping Index</h2>
            <router-link :to="{ name: 'shipping.create' }" class="btn-add-shipping">
                <i class="fas fa-plus mr-2"></i> Add Shipping
            </router-link>
        </div>
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white border border-green-300">
                <thead>
                    <tr>
                        <th class="py-3 px-6 text-left border-b text-green-700">No</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Shipping Name</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Price</th>
                        <th class="py-3 px-6 text-left border-b text-green-700">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(shipping, index) in services" :key="shipping.id">
                        <td class="py-4 px-6 border-b">{{ index + 1 }}</td>
                        <td class="py-4 px-6 border-b">{{ shipping.name }}</td>
                        <td class="py-4 px-6 border-b">{{ shipping.price }}</td>
                        <td class="py-4 px-6 border-b">
                            <div class="flex items-center">
                                <router-link :to="{ name: 'shipping.edit', params: { id: shipping.id } }"
                                    class="text-green-500 hover:underline mr-2">
                                    Edit
                                </router-link>
                                <button @click="removeShipping(shipping.id)"
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
.btn-add-shipping {
    padding: 8px 12px;
    background-color: #4caf50;
    /* Green color */
    color: #fff;
    text-decoration: none;
    border-radius: 4px;
    display: flex;
    align-items: center;
    transition: background-color 0.3s;
    border: 1px solid #4caf50;
    /* Solid border */
}

.btn-add-shipping:hover {
    background-color: #45a049;
    /* Darker green color on hover */
}

.btn-add-shipping i {
    margin-right: 6px;
}</style>