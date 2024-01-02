<script setup>
import { ref, onMounted } from "vue";
import { authService } from "@/api";

const payments = ref([]);

const fetchData = async () => {
  try {
    const response = await authService.get("/payment_get");
    payments.value = response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

const removePayment = async (paymentId) => {
  try {
    console.log(paymentId);
    await authService.delete("/payment", {
      data: { id: paymentId },
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    fetchData();
  } catch (error) {
    console.error("Error deletinng data:", error);
  }
};

onMounted(() => {
  fetchData();
});
</script>

<template>
  <div class="container mx-auto">
    <div class="container mx-auto flex justify-between items-center">
      <h2 class="text-2xl font-bold mb-4 text-green-700">Payment Index</h2>
      <router-link :to="{ name: 'payment.create' }" class="btn-add-payment">
        <i class="fas fa-plus mr-2"></i> Add Payment
      </router-link>
    </div>
    <div class="overflow-x-auto">
      <table class="min-w-full bg-white border border-green-300">
        <thead>
          <tr>
            <th class="py-3 px-6 text-left border-b text-green-700 w-1">No</th>
            <th class="py-3 px-6 text-left border-b text-green-700 w-1/2">
              Image
            </th>
            <th class="py-3 px-6 text-left border-b text-green-700 w-1/2">
              Payment Name
            </th>
            <th class="py-3 px-6 text-left border-b text-green-700 w-1">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(payment, index) in payments" :key="payment.id">
            <td class="py-4 px-6 border-b">{{ index + 1 }}</td>
            <td class="py-4 px-6 border-b">
              <img :src="'/uploaded/' + payment.image" :alt="payment.image" />
            </td>
            <td class="py-4 px-6 border-b">{{ payment.name }}</td>
            <td class="py-4 px-6 border-b">
              <div class="flex items-center">
                <router-link
                  :to="{ name: 'payment.edit', params: { id: payment.id } }"
                  class="text-green-500 hover:underline mr-2"
                >
                  Edit
                </router-link>
                <button
                  @click="removePayment(payment.id)"
                  class="text-red-500 hover:underline focus:outline-none"
                >
                  Remove
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style>
.btn-add-payment {
  padding: 8px 12px;
  background-color: #4caf50; /* Green color */
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
  display: flex;
  align-items: center;
  transition: background-color 0.3s;
  border: 1px solid #4caf50; /* Solid border */
}

.btn-add-payment:hover {
  background-color: #45a049; /* Darker green color on hover */
}

.btn-add-payment i {
  margin-right: 6px;
}
</style>
