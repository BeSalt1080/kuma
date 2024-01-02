<script setup>
import { authService } from "../api";
import { onMounted, ref } from "vue";

const carts = ref("");
const subtotal = ref(0);

const fetchData = async () => {
  try {
    const response = await authService.get("/cart");
    carts.value = response.data;
    subtotal.value = 0;
    carts.value.forEach((cart) => {
      subtotal.value += cart.price * cart.quantity;
    });
    console.log(carts.value);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

const wishlist = async (cart) => {
  if (cart.wishlist) {
    try {
      await authService.delete("/wishlist", {
        data: { id: cart.wishlist[0] },
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });
      fetchData();
    } catch (error) {
      console.error("Error deletinng data:", error);
    }
  } else {
    await authService.post(
      "/wishlist",
      { products_id: cart.id },
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );
    fetchData();
  }
};
const deleteCart = async (cart_id) => {
  try {
    await authService.delete("/cart", {
      data: { id: cart_id },
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
  <div class="flex flex-1 justify-center mt-10">
    <div class="w-5/6">
      <h1 class="text-center text-xl font-bold">Cart</h1>
      <div class="px-10">
        <div class="flex justify-between">
          <div class="w-1/2">
            <h1 class="text-2xl font-bold">Items</h1>
            <div
              class="flex w-full border-b my-2"
              v-for="cart in carts"
              :key="cart.id"
            >
              <img
                class="w-44"
                :src="'/uploaded/' + cart.image"
                :alt="cart.image"
              />
              <div class="w-full">
                <div class="w-full flex justify-between">
                  <div class="font-bold text-lg">
                    {{ cart.name }}
                  </div>
                  <div class="font-bold text-lg">
                    {{
                      new Intl.NumberFormat("in-ID", {
                        style: "currency",
                        currency: "IDR",
                      }).format(cart.price - (cart.sale * cart.price) / 100)
                    }}
                  </div>
                </div>
                <div>
                  {{ cart.category }}
                </div>
                <div>
                  {{ cart.color }}
                </div>
                <div>
                  Size: {{ cart.size }} Quantity: <button>-</button>
                  <input class="w-10" type="text" :value="cart.quantity" />
                  <button>+</button>
                </div>
                <div class="flex gap-5">
                  <button class="w-10 h-10" @click="wishlist(cart)">
                    <i
                      class="fa-regular fa-heart text-2xl mt-1"
                      :class="{ 'text-red-600 fa-solid': cart.wishlist }"
                    ></i>
                  </button>
                  <button @click="deleteCart(cart.cart_id)">
                    <i class="fa-solid fa-trash-can text-2xl"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="w-1/3">
            <h1 class="text-2xl font-bold mx-10">Summary</h1>
            <table class="mx-10 w-5/6 my-3">
              <tr>
                <td class="w-1/2 py-1">Subtotal</td>
                <td class="text-right">
                  {{
                    new Intl.NumberFormat("in-ID", {
                      style: "currency",
                      currency: "IDR",
                    }).format(subtotal)
                  }}
                </td>
              </tr>
              <tr>
                <td class="w-1/2 py-1">Estimated Duty & Taxes</td>
                <td class="text-right">
                  {{
                    new Intl.NumberFormat("in-ID", {
                      style: "currency",
                      currency: "IDR",
                    }).format((subtotal * 11) / 100)
                  }}
                </td>
              </tr>
            </table>
            <hr />
            <table class="mx-10 w-5/6 my-3">
              <tr>
                <td class="w-1/2">Total</td>
                <td class="text-right">
                  {{
                    new Intl.NumberFormat("in-ID", {
                      style: "currency",
                      currency: "IDR",
                    }).format(subtotal + (subtotal * 11) / 100)
                  }}
                </td>
              </tr>
            </table>
            <hr />
            <router-link
              :to="{ name: 'order.checkout' }"
              class="block text-center mt-5 p-4 bg-green-400 hover:bg-green-300 w-5/6 mx-10"
              >Checkout</router-link
            >
          </div>
        </div>
        <div class="mt-20 mb-10">
          <h1 class="text-2xl font-bold">You Might Also Like</h1>
        </div>
      </div>
    </div>
  </div>
</template>
