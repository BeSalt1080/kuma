<script setup>
import { authService } from '../../api';
import ToggleList from '@/components/ToggleList.vue';
import Product from '../../components/Product.vue'
import { ref, defineProps, toRefs, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import PrimaryButton from '@/components/PrimaryButton.vue';

const router = useRouter().currentRoute.value
const route = useRoute()

const products = ref([])
const brands = ref([])
const categories = ref([])
const sizes = ref([])
const genders = ref([])

const gender = ref('')

const brandfilter = ref('')
const categoryfilter = ref('')
const genderfilter = ref('')
const sizefilter = ref('')
const pricefilter = ref({})

const query = ref('')

const props = defineProps({
    category: String
})
const { category } = toRefs(props)

const fetchProduct = async () => {
    try {
        const response = await authService.get('/product_get');
        products.value = response.data;
        switch (category.value) {
            case 'Men':
                gender.value = true
                products.value = products.value.filter((product) => { return product.gender == "Men" || product.gender == "Unisex" })
                if (route.params.categories == "footwear") {
                    products.value = products.value.filter((product) => { return product.category == "Footwear" })
                }
                else if (route.params.categories == "aparrel") {
                    products.value = products.value.filter((product) => { return product.category == "Aparrel" })
                }
                break;
            case 'Women':
                gender.value = true
                products.value = products.value.filter((product) => { return product.gender == "Women" || product.gender == "Unisex" })
                if (route.params.categories == "footwear") {
                    products.value = products.value.filter((product) => { return product.category == "Footwear" })
                }
                else if (route.params.categories == "aparrel") {
                    products.value = products.value.filter((product) => { return product.category == "Aparrel" })
                }
                break;
            case 'Kids':
                gender.value = true
                products.value = products.value.filter((product) => { return product.gender == "Kids" })
                if (route.params.categories == "footwear") {
                    products.value = products.value.filter((product) => { return product.category == "Footwear" })
                }
                else if (route.params.categories == "aparrel") {
                    products.value = products.value.filter((product) => { return product.category == "Aparrel" })
                }
                break;
            case 'Sale':
                products.value = products.value.filter((product) => { return product.sale > 0 })
                break;
            case 'Accessory':
                products.value = products.value.filter((product) => { return product.category == "Accessory" })
                break;
            case 'Search':
                const escapedQuery = query.value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
                const search = new RegExp(".*" + escapedQuery + ".*", 'i')
                products.value = products.value.filter((product) => { return search.test(product.name) })
                break;
            case 'Brand':
                break;
        }
        countData()
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

const fetchData = async () => {
    fetchProduct()
    try {
        const response = await authService.get('/brand_get');
        brands.value = response.data;

        console.log(brands.value);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
    try {
        const response = await authService.get('/category_get');
        categories.value = response.data;

    } catch (error) {
        console.error('Error fetching data:', error);
    }
    try {
        const response = await authService.get('/size_get');
        sizes.value = response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
    try {
        const response = await authService.get('/gender_get');
        genders.value = response.data;

    } catch (error) {
        console.error('Error fetching data:', error);
    }
    countData()
};

const productFilter = async (filter) => {
    await fetchProduct()
    switch (filter) {
        case "brand":

            products.value = products.value.filter((product) => { console.log(product.brands_id == brandfilter.value); return product.brands_id == brandfilter.value })
            categoryfilter.value = ''
            genderfilter.value = ''
            sizefilter.value = ''
            pricefilter.value = ''
            break;
        case "category":
            products.value = products.value.filter((product) => { return product.categories_id == categoryfilter.value })
            brandfilter.value = ''
            genderfilter.value = ''
            sizefilter.value = ''
            pricefilter.value = ''
            break;
        case "gender":
            products.value = products.value.filter((product) => { return product.genders_id == genderfilter.value })
            brandfilter.value = ''
            categoryfilter.value = ''
            sizefilter.value = ''
            pricefilter.value = ''
            break;
        case "size":
            products.value = products.value.filter((product) => {
                return product.sizes.some(size => { return size.id == sizefilter.value });
            })
            brandfilter.value = ''
            categoryfilter.value = ''
            genderfilter.value = ''
            pricefilter.value = ''
            break;
        case "price":
            products.value = products.value.filter((product) => {
                console.log(pricefilter, product.price);
                return product.price <= pricefilter.value.max && product.price >= pricefilter.value.min
            })
            brandfilter.value = ''
            categoryfilter.value = ''
            genderfilter.value = ''
            sizefilter.value = ''
            break;
        case "reset":
            brandfilter.value = ''
            categoryfilter.value = ''
            genderfilter.value = ''
            sizefilter.value = ''
            pricefilter.value = ''
            break;
        default:
            console.log("what");
            break;
    }
}

const countData = () => {
    brands.value.forEach(brand => {
        brand.count = products.value.filter((product) => { return product.brands_id == brand.id }).length
    });
    categories.value.forEach(category => {
        category.count = products.value.filter((product) => { return product.categories_id == category.id }).length
    });
    genders.value.forEach(gender => {
        gender.count = products.value.filter((product) => { return product.genders_id == gender.id }).length
    });
}

onMounted(() => {
    query.value = route.query.q
    fetchData()
})

watch(category, () => {
    fetchProduct()
    productFilter('reset')
})
watch(() => route.params.categories, () => {
    fetchProduct()
    productFilter('reset')
})
watch(() => route.query.q, () => {
    query.value = route.query.q
    fetchProduct()
    productFilter('reset')
})

</script>
<template>
    <div class="p-10 w-full">
        <h1 class="text-center text-xl font-bold" v-if="query">{{ "You Searched for " + query }}</h1>
        <h1 class="text-center text-xl font-bold" v-else>{{ category }} </h1>
        <div class="flex gap-5">
            <div class="w-1/6">
                <div class="border-b-black border-b">
                    <RouterLink class="cursor-pointer" :to="{name:'home'}">Home</RouterLink> / {{ category }} {{ route.params.categories === undefined ? null : '/ ' + route.params.categories
                    }}
                </div>
                <hr>
                <ToggleList title="Brand">
                    <div class="" v-for="brand in brands">
                        <div class="hover:text-green-600 w-fit cursor-pointer active:text-green-800"
                            :class="{ 'text-green-400': brandfilter == brand.id }" v-if="brand.count != 0" @click="() => {
                                if (brandfilter != brand.id) {
                                    brandfilter = brand.id
                                    productFilter('brand')
                                }
                                else {
                                    productFilter('reset')
                                }
                            }">
                            {{ brand.name }} ({{ brand.count }})
                        </div>
                    </div>
                    <hr class="mt-5">
                </ToggleList>
                <ToggleList title="Category">
                    <div class="" v-for="category in categories">
                        <div class="hover:text-green-600 w-fit cursor-pointer active:text-green-800"
                            :class="{ 'text-green-400': categoryfilter == category.id }" v-if="category.count != 0" @click="() => {
                                if (categoryfilter != category.id) {
                                    categoryfilter = category.id
                                    productFilter('category')
                                }
                                else {
                                    productFilter('reset')
                                }
                            }">
                            {{ category.name }} ({{ category.count }})
                        </div>
                    </div>
                    <hr class="mt-5">
                </ToggleList>
                <ToggleList title="Gender" v-if="!gender">
                    <div class="" v-for="gender in genders">
                        <div class="hover:text-green-600 w-fit cursor-pointer active:text-green-800"
                            :class="{ 'text-green-400': genderfilter == gender.id }" v-if="gender.count != 0" @click="() => {
                                if (genderfilter != gender.id) {
                                    genderfilter = gender.id
                                    productFilter('gender')
                                }
                                else {
                                    productFilter('reset')
                                }
                            }">
                            {{ gender.name }} ({{ gender.count }})
                        </div>
                    </div>
                    <hr class="mt-5">
                </ToggleList>
                <ToggleList title="Size">
                    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                        <div class="cursor-pointer w-full py-2 border text-center"
                            :class="{ 'border-green-300 bg-green-100': sizefilter == size.id }" v-for="size in sizes"
                            :key="size.id" @click="() => {
                                if (sizefilter != size.id) {
                                    sizefilter = size.id
                                    productFilter('size')
                                }
                                else {
                                    productFilter('reset')
                                }
                            }">
                            {{ size.name }}
                        </div>
                    </div>
                    <hr class="mt-5">
                </ToggleList>
                <ToggleList title="Price">
                    <div>
                        <div class="w-full">
                            <label for="price_min">Min</label>
                            <input type="text" class="w-full border-gray-400 rounded-md" v-model="pricefilter.min"
                                id="price_min">
                        </div>
                        <div class="w-full">
                            <label for="price_max">Max</label>
                            <input type="text" class="w-full border-gray-400 rounded-md" v-model="pricefilter.max"
                                id="price_max">
                        </div>
                        <PrimaryButton class="w-full mt-3 font-semibold" @click="() => {
                            productFilter('price')
                        }">Apply</PrimaryButton>
                    </div>
                    <hr class="mt-5">
                </ToggleList>
            </div>
            <div class="grid grid-cols-3 gap-20 mx-20 w-5/6">
                <Product v-for="product in products" :brand="product.brand" :name="product.name" :image="product.image"
                    :price=product.price :id=product.id :sale="product.sale" />
            </div>
        </div>
    </div>
</template>