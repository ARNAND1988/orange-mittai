<script setup>
import Navbar from './components/NavBar.vue'
import AnnouncementBar from './components/AnnouncementBar.vue'
import DealsSubMenu from "./components/DealsSubMenu.vue"
import { toast } from "@/utils/toast"
</script>

<template>
  <!-- FULL HEIGHT APP -->
  <div class="h-screen flex flex-col">

    <!-- FIXED TOP SECTION -->
    <AnnouncementBar />
    <Navbar />
    <DealsSubMenu />
    <!-- SCROLLABLE CONTENT ONLY -->
    <main class="flex-1 overflow-y-auto">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <RouterView />
      </div>
    </main>
<!-- Global Toast -->
  <div
    v-if="toast.show"
    class="fixed top-20 right-6 z-50"
  >
    <div
      class="px-4 py-3 rounded-lg shadow text-sm"
      :class="toast.type === 'error'
        ? 'bg-red-100 text-red-800'
        : 'bg-green-100 text-green-800'"
    >
      {{ toast.message }}
    </div>
  </div>
  </div>
</template>
