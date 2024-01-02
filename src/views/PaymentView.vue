<script setup>
import { onMounted, ref } from 'vue';
import { useOrderStore } from '../stores/order.js'
import { authService } from '@/api';

const address = ref('')
const shipping = ref('')
const payment = ref('')
const carts = ref('')
const store = useOrderStore()
const paymentOption = ref('')
const subtotal = ref(0);


const fetchData = async () => {
    try {
        let response = await authService.get('/shipping_get');
        shipping.value = response.data.filter((expedition) => { return expedition.id == store.expedition })[0];
        console.log(shipping.value);
        response = await authService.get('/cart');
        carts.value = response.data;
        subtotal.value = 0
        carts.value.forEach(cart => {
            subtotal.value += cart.price * cart.quantity
        });
        response = await authService.get('/address');
        address.value = response.data;
        response = await authService.get('/payment_get');
        payment.value = response.data
        paymentOption.value = payment.value[0].id
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

const proceed = async () => {
    let products = []
    carts.value.forEach(product => {
        products.push({
            products_id: product.id,
            quantity: product.quantity,
            sizes_id: product.sizes_id
        })
    });
    const data = JSON.stringify({
        products: products
    })
    console.log(data);
    await authService.post('/order', data, { headers: { 'Content-Type': 'application/JSON' } })
}

onMounted(() => {
    fetchData();
});

</script>
<template>
    <div class="flex flex-1 justify-center my-10">
        <div class="w-5/6">
            <h1 class="text-center text-xl font-bold">Order Detail</h1>
            <div class="px-10 grid grid-cols-2 gap-20">
                <div class="col">
                    <div class="flex justify-between">
                        <h1 class="text-xl font-bold">Payment Method:</h1>
                    </div>
                    <div class="grid grid-cols-2 gap-5">
                        <div class="border w-full" v-for="p in payment">
                            <label class="p-4 block cursor-pointer items-center" :for="p.name">
                                {{ p.name }}
                                <input class="float-end" type="radio" :id="p.name" v-model="paymentOption" :value="p.id">
                            </label>
                        </div>
                    </div>
                    <button @click="proceed"
                        class="block text-center mt-5 p-4 bg-green-400 hover:bg-green-300 w-2/3 mx-auto">Confirm</button>
                </div>
                <div class="">
                    <h1 class="text-2xl font-bold mx-10">Summary</h1>
                    <table class="mx-10 w-5/6 my-3">
                        <tr>
                            <td class="w-1/2 py-1">Subtotal</td>
                            <td class="text-right">{{ new Intl.NumberFormat('in-ID', {
                                style: 'currency', currency: 'IDR'
                            }).format(subtotal)
                            }}</td>
                        </tr>
                        <tr>
                            <td class="w-1/2 py-1">Delivery & Handling</td>
                            <td class="text-right">{{ new Intl.NumberFormat('in-ID', {
                                style: 'currency', currency: 'IDR'
                            }).format(shipping.price)
                            }}</td>
                        </tr>
                        <tr>
                            <td class="w-1/2 py-1">Estimated Duty & Taxes </td>
                            <td class="text-right">{{ new Intl.NumberFormat('in-ID', {
                                style: 'currency', currency: 'IDR'
                            }).format(subtotal * 11 / 100)
                            }}</td>
                        </tr>
                    </table>
                    <hr>
                    <table class="mx-10 w-5/6 my-3">
                        <tr>
                            <td class="w-1/2">Total</td>
                            <td class="text-right">{{ new Intl.NumberFormat('in-ID', {
                                style: 'currency', currency: 'IDR'
                            }).format(subtotal + (subtotal * 11 / 100) + shipping.price)
                            }}</td>
                        </tr>
                    </table>
                    <hr>
                    <div class="my-3 mx-10">
                        <h1 class="text-2xl font-bold">Items Summary</h1>
                        <div class="border overflow-y-scroll max-h-32 shadow-sm">
                            <div class="flex w-11/12 mx-auto my-2 " v-for="(cart) in carts" :key="cart.id">
                                <img class="w-20" :src="'/uploaded/' + cart.image" :alt="cart.image" />
                                <div class="w-full">
                                    <div class="w-full flex justify-between items-center">
                                        <div>
                                            <div class="font-bold text-xs">
                                                {{ cart.name }}
                                            </div>
                                            <div class="text-xs">
                                                <div>Category: {{ cart.category }}</div>
                                                <div>Color: {{ cart.color }}</div>
                                                <div>Size: {{ cart.size }} Quantity: {{ cart.quantity }}</div>
                                            </div>
                                        </div>
                                        <div class="font-bold text-sm w-fit">
                                            {{ new Intl.NumberFormat('in-ID', {
                                                style: 'currency', currency: 'IDR'
                                            }).format((cart.price - (cart.sale * cart.price / 100)) * cart.quantity) }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr>
                    <div class="my-3 mx-10">
                        <h1 class="text-2xl font-bold">Address Detail</h1>
                        <div class="text-xs">
                            <div class="font-bold">{{ address.name }}</div>
                            <div>Address: {{ address.address }}</div>
                            <div>Phone Number: {{ address.phone }}</div>
                            <div>{{ shipping.name }}</div>
                            <div>{{ address.city }}</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>