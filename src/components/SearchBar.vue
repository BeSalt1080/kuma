<script setup>
import SearchIcon from './icons/SearchIcon.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const search = ref('')
const router = useRouter();
const Search = ()=>{
    router.push({ name:'search', query:{q:search.value} })
}

</script>
    
<template>
    <div class="flex items-center gap-1">
        <SearchIcon height="24px" />
        <form @submit.prevent="Search">
            <input class=" p-4 rounded-2xl h-8 appearance-none focus:border-green-500" v-model="search" type="text" placeholder="Search">
        </form>
    </div>
</template>