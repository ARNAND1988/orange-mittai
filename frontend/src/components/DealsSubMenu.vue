<template>
  <!-- DESKTOP SUB MENU (UNCHANGED) -->
  <div class="hidden md:flex bg-white border-b border-neutral-200">
    <div class="max-w-7xl mx-auto flex gap-6 px-6 py-3">
      <RouterLink
        v-for="item in menu"
        :key="item.name"
        :to="item.to"
        class="flex items-center gap-2 text-sm font-medium
               text-neutral-700 hover:text-orange-600"
      >
        <component :is="item.icon" class="w-4 h-4" />
        {{ item.label }}
      </RouterLink>
    </div>
  </div>

<!-- MOBILE TOP BAR (MENU + SEARCH) -->
<div class="md:hidden bg-white border-b border-neutral-200">
  <div class="flex items-center gap-3 px-4 py-3">

    <!-- Hamburger -->
    <button
      @click="open = true"
      class="p-2 text-neutral-700"
    >
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M4 6h16M4 12h16M4 18h16"
        />
      </svg>
    </button>

    <!-- Search -->
    <div class="relative flex-1">
      <input
        type="text"
        placeholder="Find a product…"
        class="w-full pl-9 pr-3 py-2 text-sm
               rounded-full border border-neutral-300
               focus:outline-none focus:ring-2 focus:ring-orange-400"
      />
      <svg
        class="absolute left-3 top-1/2 -translate-y-1/2
               w-4 h-4 text-neutral-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 1110.5 3a7.5 7.5 0 016.15 12.65z"
        />
      </svg>
    </div>

  </div>
</div>

  <!-- MOBILE DRAWER -->
  <div
    v-if="open"
    class="fixed inset-0 z-50"
  >
    <!-- Overlay -->
    <div
      class="absolute inset-0 bg-black/40"
      @click="open = false"
    ></div>

    <!-- Drawer -->
    <aside
      class="absolute left-0 top-0 h-full w-[85%] max-w-sm
             bg-white shadow-xl flex flex-col"
    >
      <!-- HEADER -->
      <div class="flex items-center justify-between px-4 py-4 border-b">
        <h3 class="text-sm font-semibold tracking-wide">MENU</h3>
        <button
          @click="open = false"
          class="p-1 rounded-full hover:bg-neutral-100"
        >
          ✕
        </button>
      </div>

      <!-- MENU ITEMS -->
      <nav class="flex-1 overflow-y-auto py-2">
        <RouterLink
          v-for="item in menu"
          :key="item.name"
          :to="item.to"
          @click="open = false"
          class="flex items-center gap-3
                 px-4 py-3 text-sm
                 hover:bg-neutral-100"
        >
          <component
            :is="item.icon"
            class="w-5 h-5 text-orange-500"
          />
          {{ item.label }}
        </RouterLink>
      </nav>
    </aside>
  </div>
</template>

<script setup>
import { ref } from "vue";
import {
  FireIcon,
  StarIcon,
  MapIcon,
  MapPinIcon,
} from "@heroicons/vue/24/solid";

const open = ref(false);

const menu = [
  {
    name: "spice-steals",
    label: "Spice Steals",
    icon: FireIcon,
    to: "/deals/spice-steals",
  },
  {
    name: "southern-crunch",
    label: "Southern Crunch",
    icon: MapIcon,
    to: "/deals/southern-crunch",
  },
  {
    name: "northern-delights",
    label: "Northern Delights",
    icon: MapPinIcon,
    to: "/deals/northern-delights",
  },
  {
    name: "favourites",
    label: "Customer Favourites",
    icon: StarIcon,
    to: "/deals/favourites",
  },
];
</script>
