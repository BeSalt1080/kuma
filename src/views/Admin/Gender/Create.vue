
<script setup>
import { ref, reactive } from 'vue';
import { object, string } from 'yup';
import { authService } from '@/api';
import router from '@/router';

const name = ref('');
const loading = ref(false);
const errors = reactive({
    name: '',
});
const successMessage = ref('');
const errorMessage = ref('');

const isValidForm = () => {
    return !Object.values(errors).some(Boolean);
};

const validateForm = () => {
    const schema = object().shape({
        name: string().required('Name is required').min(3, 'Name must be at least 3 characters'),
    });

    schema
        .validate({ name: name.value }, { abortEarly: false })
        .then(() => {
            errors.name = '';
        })
        .catch(validationErrors => {
            validationErrors.inner.forEach(error => {
                errors[error.path] = error.message;
            });
            successMessage.value = '';
        });
};

const submitForm = () => {
    validateForm();

    if (isValidForm()) {
        loading.value = true;
        authService
            .post('/gender', { name: name.value }, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            })
            .then(() => {
                successMessage.value = 'Form submitted successfully!';
                errorMessage.value = '';
                name.value = '';
            })
            .catch(error => {
                successMessage.value = '';
                errorMessage.value = `Error: ${error.message || 'Unknown error'}`;
            })
            .finally(() => {
                loading.value = false;
            });
    }
};

const goBack = () => {
    router.back()
}

</script>

<template>
    <div class="flex justify-center items-center h-3/5 w-full">
        <form @submit.prevent="submitForm" class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-3/12">
            <div class="mb-4">
                <h2 class="text-2xl font-bold mb-4 text-center text-green-700">Gender</h2>
                <label class="block text-gray-700 text-sm font-bold mb-2" for="name">
                    Name
                </label>
                <input v-model="name" @input="validateForm" :class="{ 'border-red-500': errors.name }"
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="name" type="text" placeholder="Enter your name" />
                <div v-if="errors.name" class="text-red-500 text-xs mt-1">{{ errors.name }}</div>
            </div>
            <div class="flex items-center justify-center gap-10">
                <button></button>
                <button @click.prevent="goBack" class="text-gray-600 hover:text-gray-800">
                    <i class="fas fa-chevron-left mr-2"></i> Back
                </button>
                <button
                    class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    type="submit" :disabled="loading || !isValidForm">
                    {{ loading ? 'Loading...' : 'Submit' }}
                </button>
            </div>
            <div v-if="loading" class="mt-4 text-center text-green-700">
                Loading...
            </div>
            <div v-if="successMessage" class="mt-4 text-center text-green-700">
                {{ successMessage }}
            </div>
            <div v-if="errorMessage" class="mt-4 text-center text-red-500">
                {{ errorMessage }}
            </div>
        </form>
    </div>
</template>