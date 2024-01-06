<script setup>
import { authService } from '@/api';
import { useOrderStore } from '@/stores/order';
import UserLayout from '@/views/layouts/UserLayout.vue'
import { onMounted, ref } from 'vue';

const order = ref()
const total = ref()

const store = useOrderStore()

const fetchData = async () => {
    try {
        const response = await authService.get('/order')
        if (response.status == 200) {
            order.value = response.data.filter(product => {
                return product.order_id == store.order_id
            })
            order.value.forEach(product => {
                if (product.sale)
                    orderTotal += (product.price * product.quantity) * product.sale / 100;
                else
                    orderTotal += product.price * product.quantity;
            });
        }
    } catch (error) {
        console.error("Error Fetching Data: " + error);
    }
}
onMounted(() => {
    fetchData();
})
</script>
<template>
    <UserLayout>
        <table class="w-full text-xl text-center">
            <tr class="bg-green-300">
                <th class="py-3">Products</th>
                <th class="py-3">SKU</th>
                <th class="py-3">Price</th>
                <th class="py-3">Quantity</th>
                <th class="py-3">Subtotal</th>
            </tr>
            <tr v-for="(product) in order" :key="product.id">
                <td class="py-4 px-6 border-b flex">
                    <img class="h-32" :src="'/uploaded/' + product.image" :alt="product.image" />
                    <div class="flex flex-col text-left self-center">
                        <div class="text-sm font-bold">{{ product.name }}</div>
                        <div class="text-base">Brand Name : {{ product.brand }}</div>
                        <div class="text-base">Size : {{ product.size }}</div>
                    </div>
                </td>
                <td class="py-4 px-6 border-b">{{ product.sku }}</td>
                <td class="py-4 px-6 border-b">{{ new Intl.NumberFormat("in-ID", {
                    style: "currency", currency:
                        "IDR",
                }).format(product.price - (product.sale * product.price) / 100) }}</td>
                <td class="py-4 px-6 border-b">{{ product.quantity }}</td>
                <td class="py-4 px-6 border-b">{{ new Intl.NumberFormat("in-ID", { style: "currency", currency: "IDR",}).format((product.price - (product.sale * product.price) / 100) * product.quantity) }}</td>
            </tr>
        </table>
        <hr>
        <div class="w-full flex justify-end text-xl">
            <table>
                <tr>
                    <td>SubTotal</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Discount</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Shipping</td>
                    <td></td>
                </tr>
                <tr>
                    <td>Order Total</td>
                </tr>
            </table>
        </div>
    </UserLayout>
</template>