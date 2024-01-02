<script setup>
import UserLayout from '@/views/layouts/UserLayout.vue'

import { onMounted, ref } from 'vue';
import { authService } from '@/api';

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
    <UserLayout>
        <div class="p-5">
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
            <button @click="proceed">Update</button>
        </div>
    </UserLayout>
</template>