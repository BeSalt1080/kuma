
<script setup>

import { ref } from 'vue';
import { object, mixed, string } from 'yup';
import { authService } from '@/api';
import router from '@/router';

const image = ref(null);
const link = ref('');
const imageError = ref(null);
const linkError = ref(null);
const successMessage = ref('');
const errorMessage = ref('');


const validationSchema = object().shape({
    image: mixed().required('Image is required').test('fileType', 'Invalid file type', (value) => {
        if (!value) return false;
        const acceptedExtensions = ['png', 'webp', 'jpg', 'jpeg'];
        const extension = value.name.split('.').pop().toLowerCase();
        return acceptedExtensions.includes(extension);
    }),
    link: string().required('Link is required').min(3, 'Link must be at least 3 characters'),
});

const handleImageChange = (event) => {
    const file = event.target.files[0];
    image.value = file;
    imageError.value = null;
    validateField('image');
};

const validateField = async (fieldName) => {
    try {
        await validationSchema.validateAt(fieldName, { image: image.value, link: link.value });
        if (fieldName === 'image') {
            imageError.value = null;
        } else if (fieldName === 'link') {
            linkError.value = null;
        }
    } catch (error) {
        successMessage.value = '';
        if (fieldName === 'image') {
            imageError.value = error.message;
        } else if (fieldName === 'link') {
            linkError.value = error.message;
        }
    }
};

const submitForm = async () => {
    try {
        await validationSchema.validate({ image: image.value, link: link.value }, { abortEarly: false });

        const formData = new FormData();
        formData.append('image', image.value);
        formData.append('link', link.value);

        const response = await authService.post('/banner', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        successMessage.value = 'Form submitted successfully!';
        errorMessage.value = '';

        console.log('Response:', response.data);
    } catch (error) {
        successMessage.value = '';
        errorMessage.value = `Error: ${error.message || 'Unknown error'}`;
        console.error('Error:', error);
    }
};

const goBack = () => {
    router.back()
}

</script>

<template>
    <div class="flex justify-center items-center h-3/5 w-full">
        <div class="max-w-md mx-auto mt-8 p-6 bg-white shadow-md">
            <h2 class="text-2xl font-bold mb-4 text-green-700">Banner</h2>

            <!-- Image Link Form -->
            <form @submit.prevent="submitForm" class="space-y-4">
                <!-- Image Input -->
                <div class="mb-4">
                    <label for="image" class="block text-sm font-medium text-gray-700">Upload Image</label>
                    <input type="file" accept="image/*" id="image" name="image" @change="handleImageChange"
                        @blur="validateField('image')" class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                    <p v-if="imageError" class="text-red-500">{{ imageError }}</p>
                </div>

                <!-- Link Input -->
                <div class="mb-4">
                    <label for="link" class="block text-sm font-medium text-gray-700">Link URL</label>
                    <input v-model="link" type="text" id="link" name="link" @blur="validateField('link')"
                        class="mt-1 p-2 border border-gray-300 w-full rounded-md">
                    <p v-if="linkError" class="text-red-500">{{ linkError }}</p>
                </div>

                <!-- Submit Button -->
                <div class="flex items-center justify-center gap-10">
                    <button></button>
                    <button @click.prevent="goBack" class="text-gray-600 hover:text-gray-800">
                        <i class="fas fa-chevron-left mr-2"></i> Back
                    </button>
                    <button
                        class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="submit">
                        Submit
                    </button>
                </div>
                <div v-if="successMessage" class="mt-4 text-center text-green-700">
                    {{ successMessage }}
                </div>
                <div v-if="errorMessage" class="mt-4 text-center text-red-500">
                    {{ errorMessage }}
                </div>
            </form>
        </div>
    </div>
</template>
  