<template>
  <div
    id="default-carousel"
    class="relative w-full z-0"
    data-carousel="slide"
  >
    <!-- FRAME (controls size) -->
    <div
      class="relative h-48 sm:h-64 md:h-80 lg:h-96
             overflow-hidden rounded-xl"
    >

      <!-- Slide 1 (ACTIVE) -->
      <div
        class="absolute inset-0 duration-700 ease-in-out"
        data-carousel-item="active"
      >
        <img
          src="../assets/images/banner1.png"
          class="w-full h-full object-cover"
          alt="Orange Mittai Offers"
        />
      </div>

      <!-- Slide 2 -->
      <div
        class="absolute inset-0 hidden duration-700 ease-in-out"
        data-carousel-item
      >
        <img
          src="../assets/images/banner2.png"
          class="w-full h-full object-cover"
          alt="Festival Deals"
        />
      </div>

      <!-- Slide 3 -->
      <div
        class="absolute inset-0 hidden duration-700 ease-in-out"
        data-carousel-item
      >
        <img
          src="../assets/images/banner3.png"
          class="w-full h-full object-cover"
          alt="Sweet Promotions"
        />
      </div>

      <!-- Slide 4 -->
      <div
        class="absolute inset-0 hidden duration-700 ease-in-out"
        data-carousel-item
      >
        <img
          src="../assets/images/banner4.png"
          class="w-full h-full object-cover"
          alt="Snack Combos"
        />
      </div>
    </div>

    <!-- Indicators -->
    <div
      class="absolute z-30 flex -translate-x-1/2 bottom-4 left-1/2 space-x-3"
    >
      <button class="w-3 h-3 rounded-full bg-white/60" data-carousel-slide-to="0"></button>
      <button class="w-3 h-3 rounded-full bg-white/60" data-carousel-slide-to="1"></button>
      <button class="w-3 h-3 rounded-full bg-white/60" data-carousel-slide-to="2"></button>
      <button class="w-3 h-3 rounded-full bg-white/60" data-carousel-slide-to="3"></button>
    </div>

    <!-- Prev -->
    <button
      type="button"
      class="absolute top-0 left-0 z-30
             flex items-center justify-center h-full px-4"
      data-carousel-prev
    >
      <span
        class="w-10 h-10 flex items-center justify-center
               rounded-full bg-black/30 text-white"
      >
        ‹
      </span>
    </button>

    <!-- Next -->
    <button
      type="button"
      class="absolute top-0 right-0 z-30
             flex items-center justify-center h-full px-4"
      data-carousel-next
    >
      <span
        class="w-10 h-10 flex items-center justify-center
               rounded-full bg-black/30 text-white"
      >
        ›
      </span>
    </button>
  </div>
</template>

<script setup>
import { onMounted, nextTick } from "vue";
import { initFlowbite } from "flowbite";

onMounted(async () => {
  await nextTick();
  initFlowbite();
});
</script>
