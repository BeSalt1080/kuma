<script setup>
import { authService } from '@/api';
import { useOrderStore } from '@/stores/order';
import UserLayout from '@/views/layouts/UserLayout.vue'
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const orders = ref({})
const total = ref({})

const fetchData = async () => {
    try {
        const response = await authService.get('/order')
        if (response.status == 200) {
            response.data.forEach(order => {
                orders.value[order.order_id] = []
            });
            response.data.forEach(order => {
                orders.value[order.order_id].push(order)
            });
            Object.entries(orders.value).map((key) => {
                let orderTotal = 0;
                key[1].forEach(product => {
                    if (product.sale)
                        orderTotal += (product.price * product.quantity) * product.sale / 100;
                    else
                        orderTotal += product.price * product.quantity;
                });
                total.value[key[0]] = orderTotal;
            })
        }
    } catch (error) {
        console.error("Error Fetching Data: " + error);
    }
}

const dateFormat = (date) => {
    const temp = new Date(date); 
    return temp.getMonth()+1 + "/" + temp.getDate() + "/" + temp.getFullYear()
}

const detail = (id) => {
    const store = useOrderStore()
    store.order_id = id
    router.push({name:'order.detail'})
}

onMounted(() => {
    fetchData();
})

</script>
<template>
    <user-layout title="My Orders">
        <div class="p-5">
            <table class="w-full text-xl text-center">
                <tr class="bg-green-300">
                    <th class="py-3">Order#</th>
                    <th class="py-3">Date</th>
                    <th class="py-3">Order Total</th>
                    <th class="py-3">Status</th>
                    <th class="py-3">Action</th>
                </tr>
                <tr v-for="(order, index) in orders" :key="index">
                    <td class="py-2 border-b">{{ index }}</td>
                    <td class="py-2 border-b">{{ dateFormat(order[0].date) }}</td>
                    <td class="py-2 border-b">{{ new Intl.NumberFormat('in-ID', { style: 'currency', currency: 'IDR' }).format(total[index]) }}
                    </td>
                    <td class="py-2 border-b" v-if="order[0].status == 0">Processing</td>
                    <td class="py-2 border-b">
                        <div class="underline" @click="detail(index)">View Order</div>
                    </td>
                </tr>
            </table>
        </div>
    </user-layout>
</template>