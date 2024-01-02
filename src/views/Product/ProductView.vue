<script setup>
import { authService } from '../../api';
import ToggleList from '@/components/ToggleList.vue';
import Product from '../../components/Product.vue'
import { ref,defineProps, toRefs, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import PrimaryButton from '@/components/PrimaryButton.vue';

const route = useRouter().currentRoute.value


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
const pricefilter = ref('')

const props = defineProps({
    category: String
})
const {category} = toRefs(props)

const fetchProduct = async () => {
    console.log(route)
    try {
        const response = await authService.get('/product_get');
        products.value = response.data;
        console.log(category.value)
        switch (category.value) {
            case 'Men':
                gender.value = true                
                products.value = products.value.filter((product) => { return product.gender == "Men" || product.gender == "Unisex"})
                if (route.params.categories == "footwear") {

                }
                else if (route.params.categories == "aparrel") {

                }
                break;
            case 'Women':
                gender.value = true
                products.value = products.value.filter((product) => { return product.gender == "Women" || product.gender == "Unisex" })
                if (route.params.categories == "footwear") {

                }
                else if (route.params.categories == "aparrel") {

                }
                break;
            case 'Kids':
                gender.value = true   
                products.value = products.value.filter((product) => { return product.gender == "Kids" })
                if (route.params.categories == "footwear") {

                }
                else if (route.params.categories == "aparrel") {

                }
                break;
            case 'Latest':

                break;
            case 'Sale':
                console.log("");
                break;
            case 'Accessory':

                break;
            case 'Brand':

                break;

            default:
                break;
        }
        console.log(gender.value);
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
            products.value = products.value.filter((product) => { return product.price <= pricefilter.max && product.price >= pricefilter.min })
            brandfilter.value = ''
            categoryfilter.value = ''
            genderfilter.value = ''
            sizefilter.value = ''
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
onMounted(()=>{
    fetchData();
    watch(props, () => {
        fetchData();
    });
})


</script>
<template>
    <div class="p-10 w-full">
        <h1 class="text-center text-xl font-bold ">{{ category }}</h1>
        <div class="flex gap-5">
            <div class="w-1/6">
                <div class="border-b-black border-b">
                    Home / {{ category }} {{ $route.params.categories === undefined ? null : '/' + $route.params.categories }}

                </div>
                <hr>
                <ToggleList title="Brand">
                    <div class="" v-for="brand in brands">
                        <div class="hover:text-green-600 w-fit cursor-pointer active:text-green-800" v-if="brand.count != 0"
                            @click="() => {
                                brandfilter = brand.id
                                console.log(brandfilter)
                                productFilter('brand')
                            }">
                            {{ brand.name }} ({{ brand.count }})
                        </div>
                    </div>
                    <hr class="mt-5">
                </ToggleList>
                <ToggleList title="Category">
                    <div class="" v-for="category in categories">
                        <div class="hover:text-green-600 w-fit cursor-pointer active:text-green-800"
                            v-if="category.count != 0" @click="() => {
                                categoryfilter = category.id
                                console.log(categoryfilter)
                                productFilter('category')
                            }">
                            {{ category.name }} ({{ category.count }})
                        </div>
                    </div>
                    <hr class="mt-5">
                </ToggleList>
                <ToggleList title="Gender" v-if="!gender">
                    <div class="" v-for="gender in genders">
                        <div class="hover:text-green-600 w-fit cursor-pointer active:text-green-800"
                            v-if="gender.count != 0" @click="() => {
                                genderfilter = gender.id
                                console.log(genderfilter)
                                productFilter('gender')
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
                                sizefilter = size.id
                                productFilter('size')
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
                    <input type="text" class="w-full border-gray-400 rounded-md" v-model="pricefilter.min" name="price_min" id="price_min">
                </div>          
                <div class="w-full">
                    <label for="price_max">Max</label>
                    <input type="text" class="w-full border-gray-400 rounded-md" v-model="pricefilter.max" name="password" id="price_max">
                </div>
                        <!-- <input class="w-full " type="text">
                        <input class="w-full " type="text"> -->
                        <!-- <button class="p-4 w-full bg-green-400">Apply</button> -->
                        <PrimaryButton class="w-full mt-3 font-semibold">Apply</PrimaryButton>
                    </div>
                    <hr class="mt-5">
                </ToggleList>
            </div>
            <div class="grid grid-cols-3 gap-20 mx-20 w-5/6">
                <Product v-for="product in products" :brand="product.brand" :name="product.name" :image="product.image"
                    :price=product.price :id=product.id />
            </div>
        </div>
    </div>
</template>