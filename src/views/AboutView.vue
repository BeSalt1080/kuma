<script setup>
import { RouterLink } from "vue-router";
</script>

<template>
  <div class="flex flex-col gap-5 items-center px-12 py-10 text-white">
    <div
      class="w-full py-36 bg-[url('/images/banner1.webp')] flex items-center justify-center"
    >
      <div>
        <RouterLink to="/" class="select-none font-bold text-4xl"
          >Kuma</RouterLink
        >
        <Router to="/" class="text-3xl select-none">LATEST</Router>
      </div>
    </div>

    <div
      class="text-black flex flex-col gap-2 justify-start w-full font-semibold"
    >
      <h2 class="uppercase text-2xl tracking-tight font-bold">About Us</h2>
      <p>
        Welcome to KUMALatest, where shoes become more than a necessity—they
        become a statement. At KUMALatest, we're passionate about bringing you
        the latest and most stylish footwear options. From classic elegance to
        trendy kicks, our carefully curated collection ensures that stepping out
        is always a fashion-forward experience. With a commitment to quality,
        comfort, and affordability, KUMALatest invites you to step into a world
        where every pair tells a story and every step is taken in style.
      </p>
    </div>
  </div>
  <!-- <h1>This is an about page</h1> -->
</template>
