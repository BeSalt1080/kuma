<script setup>
import { onMounted, ref } from 'vue';
import { authService } from '../api';
import router from '../router';
import { useOrderStore } from '@/stores/order';
import PrimaryButton from '@/components/PrimaryButton.vue';

const name = ref('')
const province = ref('')
const city = ref('')
const subdistrict = ref('')
const postcode = ref('')
const phone = ref('')
const address = ref('')
const carts = ref('');
const subtotal = ref(0);
const expedition = ref('')
const shipping = ref([])
const haveAddress = ref('')


const fetchData = async () => {
    try {
        let response = await authService.get('/shipping_get');
        shipping.value = response.data;
        expedition.value = shipping.value[0].id
        response = await authService.get('/cart');
        carts.value = response.data;
        subtotal.value = 0
        carts.value.forEach(cart => {
            subtotal.value += cart.price * cart.quantity
        });
        response = await authService.get('/address');
        if (response.status == 200) {
            name.value = response.data.name
            province.value = response.data.province
            city.value = response.data.city
            subdistrict.value = response.data.subdistrict
            postcode.value = response.data.postcode
            phone.value = response.data.phone
            address.value = response.data.address
            haveAddress.value = true
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

onMounted(() => {
    fetchData();
});

const proceed = async () => {
    const data = {
        name: name.value,
        province: province.value,
        city: city.value,
        subdistrict: subdistrict.value,
        postcode: postcode.value,
        phone: phone.value,
        address: address.value
    }

    if (!haveAddress.value) {
        const response = await authService.post('/address', data, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
        if (response.status == 201) {
            const store = useOrderStore()
            store.expedition = expedition.value
            router.push({ name: "order.payment" })
        }
    }
    else {
        const response = await authService.put('/address', data, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });
        if (response.status == 200) {
            const store = useOrderStore()
            store.expedition = expedition.value
            router.push({ name: "order.payment" })
        }
    }
}

</script>
<template>
    <div class="flex flex-1 justify-center my-10">
        <div class="w-5/6 flex flex-col">
            <h1 class="text-center text-xl font-bold">Order Detail</h1>
            <div class="px-10 grid grid-cols-3 gap-20">
                <div class="">
                    <span class="text-sm">Please enter your delivery below:</span>
                    <table class="w-full">
                        <tr>
                            <label class="font-bold" for="name">Full Name</label>
                            <input class="block w-full" type="text" id="name" v-model="name">
                        </tr>
                        <tr>
                            <label class="font-bold" for="province">Province</label>
                            <input class="block w-full" type="text" id="province" v-model="province">
                        </tr>
                        <tr>
                            <label class="font-bold" for="city">City</label>
                            <input class="block w-full" type="text" id="city" v-model="city">
                        </tr>
                        <tr>
                            <label class="font-bold" for="subdistrict">Subdistrict</label>
                            <input class="block w-full" type="text" id="subdistrict" v-model="subdistrict">
                        </tr>
                        <tr>
                            <label class="font-bold" for="postcode">Postcode</label>
                            <input class="block w-full" type="text" id="postcode" v-model="postcode">
                        </tr>
                        <tr>
                            <label class="font-bold" for="phone">Phone Number</label>
                            <input class="block w-full" type="text" id="phone" v-model="phone">
                        </tr>
                        <tr>
                            <label class="font-bold" for="address">Address</label>
                            <input class="block w-full" type="text" id="address" v-model="address">
                        </tr>
                    </table>
                </div>
                <div class="col">
                    <div class="flex justify-between">
                        <h1>Shipping Method</h1>
                        <div v-if="expedition">
                            {{ new Intl.NumberFormat('in-ID', {
                                style: 'currency', currency: 'IDR'
                            }).format(shipping.filter((ship) => { return ship.id == expedition })[0].price) }}
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-5">
                        <div class="border w-full" v-for="service in shipping">
                            <label class="p-4 block cursor-pointer items-center" :for="service.name">
                                {{ service.name }}
                                <input class="float-end" type="radio" :id="service.name" v-model="expedition"
                                    :value="service.id">
                            </label>
                        </div>
                    </div>
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
                        <tr v-if="expedition">
                            <td class="w-1/2 py-1">Delivery & Handling</td>
                            <td class="text-right">{{ new Intl.NumberFormat('in-ID', {
                                style: 'currency', currency: 'IDR'
                            }).format(shipping.filter((ship) => { return ship.id == expedition })[0].price)
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
                            <td class="text-right" v-if="expedition">{{ new Intl.NumberFormat('in-ID', {
                                style: 'currency', currency: 'IDR'
                            }).format(subtotal + (subtotal * 11 / 100) + shipping.filter((ship) => {
                                return ship.id ==
                                    expedition
                            })[0].price)
                            }}</td>
                        </tr>
                    </table>
                    <hr>
                    <div class="my-3">
                        <h1 class="text-2xl font-bold mx-10">Items Summary</h1>
                        <div class="border overflow-y-scroll max-h-52 shadow-sm">
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
                </div>
            </div>
            <PrimaryButton class="mt-6 w-1/2 mx-auto" @click="proceed">Proceed To Payment</PrimaryButton>
        </div>
    </div>
</template>