<script setup>
import { authService } from '@/api';
import { onMounted, ref } from 'vue';
import { object, number, string, mixed } from 'yup';

const formData = ref({
    name: '',
    description: '',
    image: null,
    price: '',
    sku: '',
    color: '',
    sale: 0,
    categories: 0,
    brands: 0,
    genders: 0,
});

const nameError = ref(null);
const descriptionError = ref(null);
const imageError = ref(null);
const priceError = ref(null);
const skuError = ref(null);
const colorError = ref(null);
const categoriesError = ref(null);
const brandsError = ref(null);
const gendersError = ref(null);
const loading = ref(false);
const successMessage = ref(null);
const errorMessage = ref(null);

const categories = ref([]);
const brands = ref([]);
const sizes = ref([]);
const genders = ref([]);

const userInput = ref('');
const suggestions = ref([]);
const selectedValues = ref([]);
const showSuggestions = ref('');


function updateSuggestions() {
    const inputLowerCase = userInput.value.toLowerCase();
    suggestions.value = sizes.value.filter(suggestion =>
        suggestion.toLowerCase().includes(inputLowerCase) &&
        !selectedValues.value.some(selected => selected.name === suggestion)
    );
}
function selectSuggestion(suggestion) {
    selectedValues.value.push({ name: suggestion, quantity: 1 });
    userInput.value = '';
    suggestions.value = [];
}
function removeSelectedValue(index) {
    selectedValues.value.splice(index, 1);
    updateSuggestions(); // Update suggestions after removing a selected value
}
function toggleShowSuggestions() {
    showSuggestions.value = true;
    updateSuggestions();
}
function hideSuggestions() {
    setTimeout(() => {
        showSuggestions.value = false;
    }, 200);
}

const fetchData = async () => {
    try {

        await authService.get('/category_get').then(response => {
            categories.value = response.data
        });
        await authService.get('/brand_get').then(response => {
            brands.value = response.data
        });
        await authService.get('/size_get').then(response => {
            response.data.forEach(size => {
                sizes.value.push(size.name);
            });
        });
        await authService.get('/gender_get').then(response => {
            genders.value = response.data
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

onMounted(() => {
    fetchData();
});

const validationSchema = object().shape({
    name: string().required('Name is required').min(3, 'Name must be at least 3 characters'),
    description: string().required('Description is required').min(8, 'Description must be at least 8 characters'),
    image: mixed().required('Image is required').test('fileType', 'Invalid file type', (value) => {
        if (!value) return false;
        const acceptedExtensions = ['png', 'jpg', 'jpeg', 'webp'];
        const extension = value.name.split('.').pop().toLowerCase();
        return acceptedExtensions.includes(extension);
    }),
    price: number().required('Price is required').positive('Price must be a positive number'),
    sku: string().required('SKU is required').min(8, 'SKU must be at least 8 characters').max(12, 'SKU cannot be more than 12 characters'),
    color: string().required('Color is required').min(3, 'Color must be at least 3 characters'),
    sale: number().default(0),
    categories: number().required('Category is required').min(1, 'Select a valid category'),
    brands: number().required('Brand is required').min(1, 'Select a valid brand'),
    genders: number().required('GefieldNamender is required').min(1, 'Select a valid gender'),
});

const handleImageChange = (event) => {
    formData.value.image = event.target.files[0];
    imageError.value = null;
    validateField('image');
};

const validateField = async (fieldName) => {
    try {
        await validationSchema.validateAt(fieldName, formData.value);
        switch (fieldName) {
            case 'name':
                nameError.value = null;
                break;
            case 'description':
                descriptionError.value = null;
                break;
            case 'image':
                imageError.value = null;
                break;
            case 'price':
                priceError.value = null;
                break;
            case 'sku':
                skuError.value = null;
                break;
            case 'color':
                colorError.value = null;
                break;
            case 'categories':
                categoriesError.value = null;
                break;
            case 'brands':
                brandsError.value = null;
                break;
            case 'genders':
                gendersError.value = null;
                break;
        }
    } catch (error) {
        switch (fieldName) {
            case 'name':
                nameError.value = error.message;
                break;
            case 'description':
                descriptionError.value = error.message;
                break;
            case 'image':
                imageError.value = error.message;
                break;
            case 'price':
                priceError.value = error.message;
                break;
            case 'sku':
                skuError.value = error.message;
                break;
            case 'color':
                colorError.value = error.message;
                break;
            case 'categories':
                categoriesError.value = error.message;
                break;
            case 'brands':
                brandsError.value = error.message;
                break;
            case 'genders':
                gendersError.value = error.message;
                break;
        }
    }
};

const submitForm = async () => {

    try {
        loading.value = true;
        successMessage.value = null;
        errorMessage.value = null;

        await validationSchema.validate(formData.value, { abortEarly: false });
        const data = new FormData()
        data.append("name", formData.value.name)
        data.append("description", formData.value.description)
        data.append("image", formData.value.image)
        data.append("price", formData.value.price)
        data.append("sale", formData.value.sale)
        data.append("sku", formData.value.sku)
        data.append("color", formData.value.color)
        data.append("categories_id", formData.value.categories)
        data.append("brands_id", formData.value.brands)
        data.append("genders_id", formData.value.genders)

        await authService.post('/product', data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
        setTimeout(() => {
            successMessage.value = 'Form submitted successfully!';
        }, 1000);
    } catch (error) {
        errorMessage.value = 'Error submitting the form. Please try again.';
    } finally {
        loading.value = false;
    }
};



</script>

  
  
<template>
    <div class="w-1/2 mx-auto mt-8 p-6 bg-white shadow-md">
        <h2 class="text-2xl font-bold mb-4 text-green-700">Product Form</h2>

        <!-- Product Form -->
        <form @submit.prevent="submitForm" class="space-y-4">

            <!-- Image Input -->
            <div class="mb-4">
                <label for="image" class="block text-sm font-medium text-gray-700">Upload Image</label>
                <input type="file" accept="image/*" id="image" name="image" @change="handleImageChange"
                    @blur="validateField('image')" class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                <p v-if="imageError" class="text-red-500">{{ imageError }}</p>
            </div>

            <!-- Name Input -->
            <div class="mb-4">
                <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                <input v-model="formData.name" type="text" id="name" name="name" @blur="validateField('name')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                <p v-if="nameError" class="text-red-500">{{ nameError }}</p>
            </div>

            <!-- Description Input -->
            <div class="mb-4">
                <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
                <textarea v-model="formData.description" id="description" name="description"
                    @blur="validateField('description')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md"></textarea>
                <p v-if="descriptionError" class="text-red-500">{{ descriptionError }}</p>
            </div>

            <!-- SKU Input -->
            <div class="mb-4">
                <label for="sku" class="block text-sm font-medium text-gray-700">SKU</label>
                <input v-model="formData.sku" type="text" id="sku" name="sku" @blur="validateField('sku')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md" />
                <p v-if="skuError" class="text-red-500">{{ skuError }}</p>
            </div>

            <!-- Color Input -->
            <div class="mb-4">
                <label for="color" class="block text-sm font-medium text-gray-700">Color</label>
                <input v-model="formData.color" type="text" id="color" name="color" @blur="validateField('color')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md" />
                <p v-if="colorError" class="text-red-500">{{ colorError }}</p>
            </div>

            <!-- Price Input -->
            <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2">Select sizes:</label>
                <div class="relative">
                    <input v-model="userInput" @input="updateSuggestions" @focus="toggleShowSuggestions"
                        @blur="hideSuggestions" type="text"
                        class="form-input border-2 border-green-500 px-4 py-2 rounded-md w-full"
                        placeholder="Type here..." />

                    <div v-if="showSuggestions && suggestions.length > 0" class="mt-2">
                        <ul class="bg-white border border-green-500 rounded-md shadow-md absolute left-0 w-full">
                            <li v-for="(suggestion, index) in suggestions" :key="index"
                                @click="selectSuggestion(suggestion)"
                                class="cursor-pointer px-4 py-2 hover:bg-green-500 hover:text-white">
                                {{ suggestion }}
                            </li>
                        </ul>
                    </div>
                </div>

                <div v-if="selectedValues.length > 0" class="mt-4">
                    <strong>Size Quantity:</strong>
                    <div v-for="(selectedValue, index) in selectedValues" :key="index" class="flex items-center mt-2">
                        <span class="bg-green-500 text-white px-2 py-1 rounded-md mr-2">{{ selectedValue.name }}</span>
                        <span></span>
                        <input v-model="selectedValue.quantity" type="number"
                            class="form-input border-2 border-green-500 px-4 py-2 rounded-md mr-2" placeholder="Quantity" />
                        <button @click="removeSelectedValue(index)" class="text-red-500">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
            <div class="mb-4">
                <label for="price" class="block text-sm font-medium text-gray-700">Price</label>
                <input v-model="formData.price" type="number" id="price" name="price" @blur="validateField('price')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                <p v-if="priceError" class="text-red-500">{{ priceError }}</p>
            </div>


            <!-- Sale Input -->
            <div class="mb-4">
                <label for="sale" class="block text-sm font-medium text-gray-700">Sale</label>
                <input v-model="formData.sale" type="number" id="sale" name="sale"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md">
            </div>

            <!-- Categories Dropdown -->
            <div class="mb-4">
                <label for="categories" class="block text-sm font-medium text-gray-700">Categories</label>
                <select v-model="formData.categories" id="categories" name="categories" @blur="validateField('categories')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                    <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}
                    </option>
                </select>
                <p v-if="categoriesError" class="text-red-500">{{ categoriesError }}</p>
            </div>

            <!-- Brands Dropdown -->
            <div class="mb-4">
                <label for="brands" class="block text-sm font-medium text-gray-700">Brands</label>
                <select v-model="formData.brands" id="brands" name="brands" @blur="validateField('brands')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                    <option v-for="brand in brands" :key="brand.id" :value="brand.id">{{ brand.name }}</option>
                </select>
                <p v-if="brandsError" class="text-red-500">{{ brandsError }}</p>
            </div>

            <!-- Genders Dropdown -->
            <div class="mb-4">
                <label for="genders" class="block text-sm font-medium text-gray-700">Genders</label>
                <select v-model="formData.genders" id="genders" name="genders" @blur="validateField('genders')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                    <option v-for="gender in genders" :key="gender.id" :value="gender.id">{{ gender.name }}</option>
                </select>
                <p v-if="gendersError" class="text-red-500">{{ gendersError }}</p>
            </div>

            <!-- Submit Button -->
            <div class="flex items-center justify-end">
                <button :disabled="loading" type="submit" class="bg-green-500 text-white px-4 py-2 rounded">
                    Submit
                </button>
            </div>

            <!-- Loading, Success, and Error Messages -->
            <div v-if="loading" class="text-blue-500">Submitting...</div>
            <div v-if="successMessage" class="text-green-500">{{ successMessage }}</div>
            <div v-if="errorMessage" class="text-red-500">{{ errorMessage }}</div>
        </form>
    </div>
</template>
  
  