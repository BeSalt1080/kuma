<script setup>
import { authService } from '@/api';
import { ref, onMounted } from 'vue';

import { useAuthStore } from '@/stores/auth';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter()
const route = useRoute()

const msg = ref('')

const product = ref('')
const selectedSize = ref('')
const sizeArray = ref([])
const quantity = ref(1)

const fetchData = async () => {
    try {
        const response = await authService.get('/product_get',
            {
                params: { id: route.params.id },
                header: { "Content-Type": "application/x-www-form-urlencoded" }
            });
        product.value = response.data[0];
        sizeArray.value = product.value.sizes
        selectedSize.value = sizeArray.value[0].id
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};


const selectSize = (sizes) => {
    selectedSize.value = sizes
}
const store = useAuthStore()
const wishlist = async () => {
    if (Object.keys(store.user).length == 0) router.push({ name: 'login' });
    if (product.value.wishlist.length > 0) {
        try {
            await authService.delete('/wishlist', {
                data: { id: product.value.wishlist[0] },
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            });
            fetchData()
        } catch (error) {
            console.error('Error deletinng data:', error);
        }
    }
    else {
        await authService
            .post('/wishlist', { products_id: product.value.id, products_sizes_id: sizeArray.value.filter(size => { return size.id == selectedSize.value })[0].products_sizes_id[0] }, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            })
        fetchData()
    }
}

const addToCart = async () => {
    if (Object.keys(store.user).length == 0) router.push({ name: 'login' });
    const data = {
        products_id: product.value.id,
        quantity: quantity.value,
        sizes_id: selectedSize.value
    }
    await authService.post('/cart', data, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    }).then(response => {
        if (response.status == 201) {
            msg.value = "Items added to your cart successfully"
            setTimeout(()=>{msg.value=''},3000)
        }
    });
    fetchData()
}

onMounted(() => {
    fetchData();
});
</script>
<template>
    <div class="flex flex-1 justify-center mt-14">
        <div class="w-2/3">
            <p class="bg-green-400 text-white font-bold p-5" v-if="msg">{{ msg }}</p>
            <span>Home / {{ product.gender }} / {{ product.category }}</span>
            <div class="flex">
                <img :src="'/uploaded/' + product.image" :alt="product.image" />
                <div class="my-10">
                    <div class="font-bold">
                        {{ product.brand }}
                    </div>
                    <div class="font-bold text-3xl">
                        {{ product.name }}
                    </div>
                    <div class="" v-if="selectedSize">
                        Stocks:
                        {{ sizeArray.filter(size => { return size.id == selectedSize })[0].quantity }}
                    </div>
                    <div class="text-xl font-semibold" v-if="product.sale == 0">
                        {{ new Intl.NumberFormat('in-ID', { style: 'currency', currency: 'IDR' }).format(product.price) }}
                    </div>
                    <div class="text-xl font-semibold" v-else>
                        {{ new Intl.NumberFormat('in-ID', { style: 'currency', currency: 'IDR' }).format(product.price *
                            (product.sale / 100))
                        }}
                        <sup class="line-through text-sm">{{ new Intl.NumberFormat('in-ID', {
                            style: 'currency', currency: 'IDR'
                        }).format(product.price) }}</sup>
                    </div>
                    <div class="my-5">
                        Size:
                        <div class="flex gap-2">
                            <div class="cursor-pointer w-fit p-3 border"
                                :class="{ 'border-green-300 bg-green-100': selectedSize == size.id }"
                                v-for="size in sizeArray" :key="size.id" @click="selectSize(size.id)">
                                {{ size.name }}
                            </div>
                        </div>
                    </div>
                    <div class="my-5" v-if="selectedSize">
                        <label for="quantity">Quantity:</label>
                        <input v-model="quantity" class="block" min="1"
                            :max="sizeArray.filter(size => { return size.id == selectedSize })[0].quantity" type="number">
                    </div>
                    <div class="flex gap-5 items-center">
                        <button class="p-4 bg-green-400 hover:bg-green-300 rounded-lg" @click="addToCart">
                            <i class="fas fa-shopping-cart"></i> Add to Cart
                        </button>
                        <button class="border rounded-full w-14 h-14" @click="wishlist" v-if="product.wishlist">
                            <i class="fa-regular fa-heart text-2xl mt-1"
                                :class="{ 'text-red-600 fa-solid': product.wishlist.length }"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="flex border p-5 shadow-lg mb-10">
                <div class="w-1/2 p-5">
                    <h2 class="text-2xl font-bold text-green-800">Description</h2>
                    <span class="text-xs">{{ product.description }}</span>
                </div>
                <div class="w-1/2 p-5">
                    <h2 class="text-2xl font-bold text-green-800">Specification</h2>
                    <div class="flex">
                        <table>
                            <tr>
                                <td class="py-2 px-5 text-slate-700"><i
                                        class="fa-solid fa-square text-xs text-green-600"></i> Color</td>
                                <td class="px-5 text-slate-700">{{ product.color }}</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-5 text-slate-700"><i
                                        class="fa-solid fa-square text-xs text-green-600"></i> Category</td>
                                <td class="px-5 text-slate-700">{{ product.category }}</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-5 text-slate-700"><i
                                        class="fa-solid fa-square text-xs text-green-600"></i> Brand</td>
                                <td class="px-5 text-slate-700">{{ product.brand }}</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-5 text-slate-700"><i
                                        class="fa-solid fa-square text-xs text-green-600"></i> Gender</td>
                                <td class="px-5 text-slate-700">{{ product.gender }}</td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>