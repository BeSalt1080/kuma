<script setup>
import { authService } from '@/api';
import { onMounted, ref } from 'vue';
import { object, number, string } from 'yup';

const formData = ref({
    name: '',
    cost: '',
});

const nameError = ref(null);
const costError = ref(null);
const loading = ref(false);
const successMessage = ref(null);
const errorMessage = ref(null);


const validationSchema = object().shape({
    name: string().required('Name is required').min(3, 'Name must be at least 3 characters'),
    cost: number().required('Cost is required').positive('Cost must be a positive number'),
});

const validateField = async (fieldName) => {
    try {
        await validationSchema.validateAt(fieldName, formData.value);
        switch (fieldName) {
            case 'name':
                nameError.value = null;
                break;
            case 'cost':
                costError.value = null;
                break;
        }
    } catch (error) {
        switch (fieldName) {
            case 'name':
                nameError.value = error.message;
                break;
            case 'cost':
                costError.value = error.message;
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
        console.log(formData);
        await authService.post('/shipping', formData.value, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        }).then(() => { successMessage.value = 'Form submitted successfully!'; })

    } catch (error) {
        errorMessage.value = 'Error submitting the form. Please try again.';
    } finally {
        loading.value = false;
    }
};



</script>
  
<template>
    <div class="w-1/2 mx-auto mt-8 p-6 bg-white shadow-md">
        <h2 class="text-2xl font-bold mb-4 text-green-700">Shipping Form</h2>

        <!-- Product Form -->
        <form @submit.prevent="submitForm" class="space-y-4">
            <!-- Name Input -->
            <div class="mb-4">
                <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                <input v-model="formData.name" type="text" id="name" name="name" @blur="validateField('name')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                <p v-if="nameError" class="text-red-500">{{ nameError }}</p>
            </div>

            <!-- Cost Input -->
            <div class="mb-4">
                <label for="cost" class="block text-sm font-medium text-gray-700">Cost</label>
                <input v-model="formData.cost" type="number" id="cost" name="cost" @blur="validateField('cost')"
                    class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                <p v-if="costError" class="text-red-500">{{ costError }}</p>
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
  
  