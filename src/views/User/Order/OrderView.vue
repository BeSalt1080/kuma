<script setup>
import { authService } from '@/api';
import UserLayout from '@/views/layouts/UserLayout.vue'
import { onMounted, ref } from 'vue';

const orders = ref([])

const fetchData = async () => {
    try {
        const response = await authService.get('/order')
        if(response.status==200) 
        {
            response.data.forEach(order => {
                orders.value[order.order_id]=[]
            });
            response.data.forEach(order => {
                orders.value[order.order_id].push(order)
            });
            console.log(orders.value);

        }
    } catch (error) {
        console.error("Error Fetching Data: "+ error);
    }

}

onMounted(()=>{
    fetchData();
})

</script>
<template>
    <UserLayout title="My Orders">
        <div class="p-5">
            <table class="w-full text-xl">
                <tr class="bg-green-300">
                    <th class="py-3">Order#</th>
                    <th class="py-3">Date</th>
                    <th class="py-3">Order Total</th>
                    <th class="py-3">Status</th>
                    <th class="py-3">Action</th>
                </tr>
                <tr>
                    <td></td>
                </tr>
            </table>
        </div>
    </UserLayout>
</template>