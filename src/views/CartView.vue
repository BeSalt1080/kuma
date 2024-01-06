<script setup>
import PrimaryButton from "@/components/PrimaryButton.vue";
import { authService } from "../api";
import { onMounted, ref } from "vue";
import Product from "@/components/Product.vue";
const carts = ref("");
const products = ref({})
const subtotal = ref(0);


const fetchData = async () => {
  try {
    const response = await authService.get("/cart");
    carts.value = response.data;
    priceTotal()
  } catch (error) {
    console.error("Error fetching data:", error);
  }
  try {
    const response = await authService.get('/product_get');
    products.value = response.data.filter(product => {
      return product.brands_id == carts.value[0].brands_id
    })
    carts.value.forEach(cart => {
      products.value = products.value.filter(product => {
        return product.id != cart.id
      })
    });
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

const priceTotal = () => {
  subtotal.value = 0;
  carts.value.forEach((cart) => {
    subtotal.value += cart.price * cart.quantity;
  });
}

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

const updateCart = async (cart_id, quantity) => {
  try {
    await authService.put("/cart", { id: cart_id, quantity: quantity }, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      }
    }
    );
    fetchData();
  } catch (error) {
    console.error("Error deletinng data:", error);
  }
}

onMounted(() => {
  fetchData();
});
</script>
<template>
  <div class="flex flex-1 justify-center">
    <div class="w-5/6 mt-10" v-if="carts.length != 0">
      <h1 class="text-center text-xl font-bold">Cart</h1>
      <div class="px-10">
        <div class="flex justify-between">
          <div class="w-1/2">
            <h1 class="text-2xl font-bold">Items</h1>
            <div class="flex w-full border-b my-2" v-for="cart in carts" :key="cart.id">
              <img class="w-44" :src="'/uploaded/' + cart.image" :alt="cart.image" />
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
                  <span class="me-5">Size: {{ cart.size }}</span> Quantity:
                  <button class="text-xl mx-1" @click="() => {
                    cart.quantity--
                    updateCart(cart.cart_id, cart.quantity);
                    priceTotal()
                  }">-</button>
                  <input class="w-10 h-5" type="text" :value="cart.quantity" />
                  <button class="text-xl mx-1" @click="() => {
                    cart.quantity++
                    updateCart(cart.cart_id, cart.quantity)
                    priceTotal()
                  }">+</button>
                </div>
                <div class="flex gap-5">
                  <button class="w-10 h-10" @click="wishlist(cart)">
                    <i class="fa-regular fa-heart text-2xl mt-1" :class="{ 'text-red-600 fa-solid': cart.wishlist }"></i>
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
            <router-link :to="{ name: 'order.checkout' }">
              <PrimaryButton class="mt-5 w-5/6 mx-10 font-bold">
                CHECKOUT
              </PrimaryButton>
            </router-link>
          </div>
        </div>
      </div>
      <div class="mt-20 mb-10 w-3/4">
                <h1 class="text-2xl font-bold">You Might Also Like</h1>
                <div class="grid grid-cols-4 gap-5 w-full ">
                  <Product v-for="product in products" :brand="product.brand" :name="product.name" :image="product.image"
                    :price=product.price :id=product.id :sale="product.sale" />
                </div>
              </div>
    </div>
    <div class="h-[calc(100vh-64px)] flex items-center justify-center" v-else>
      <div class="text-center">
        <svg class="mx-auto h-16 w-16 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8">
          </path>
        </svg>
        <h2 class="text-2xl font-semibold text-gray-800">Your Cart is Empty</h2>
        <p class="text-gray-500 mt-2">Looks like you haven't added any items to your cart yet.</p>
      </div>
    </div>
  </div>
  
</template>
