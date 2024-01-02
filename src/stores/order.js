import { defineStore } from "pinia";
import { ref } from "vue";

export const useOrderStore = defineStore("order", () => {
  const expedition = ref(0);
  const persist = true;

  return { expedition }
},{persist:true});
