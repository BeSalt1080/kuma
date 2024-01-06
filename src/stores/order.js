import { defineStore } from "pinia";
import { ref } from "vue";

export const useOrderStore = defineStore("order", () => {
  const expedition = ref(0);
  const order_id = ref(0);

  return { expedition, order_id }
},{persist:true});
