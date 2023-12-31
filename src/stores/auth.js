import { defineStore } from "pinia";
import { authService } from "@/api";
import { ref } from "vue";

export const useAuthStore = defineStore("auth", () => {
  const user = ref({});
  const isLoggedIn = ref(false);

  async function registerUser(user) {
    const response = await authService.post("/register", user, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return response;
  }
  async function loginUser(user) {
    const response = await authService.post("/login", user, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    isLoggedIn.value = true
    return response;
  }
  async function logoutUser() {
    const response = await authService.post("/logout",'');
    if(response.status==200)
    {
      isLoggedIn.value = false
      user.value = {}
    }
  }
  async function fetchUser(){
    const response = await authService.post('/check','')
    if(response.status==200)
    {
      isLoggedIn.value = true
      user.value = response.data
    }
  }
  return { user, isLoggedIn, loginUser, registerUser, fetchUser, logoutUser };
});
