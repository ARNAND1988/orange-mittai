<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const messages = [
  '🇮🇳 Shipping from India',
  '🚚 Delivered in 15 days worldwide',
  '🍊 Authentic Orange Mittai – Freshly packed'
]

const currentIndex = ref(0)
let interval = null

onMounted(() => {
  interval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % messages.length
  }, 3000)
})

onUnmounted(() => {
  clearInterval(interval)
})
</script>

<template>
  <div class="bg-orangeMittai-600 text-white text-sm font-medium overflow-hidden">
    <div class="h-10 flex items-center justify-center relative">
      <transition-group
        name="slide"
        tag="div"
        class="absolute"
      >
        <span
          :key="currentIndex"
          class="whitespace-nowrap text-black"
        >
          {{ messages[currentIndex] }}
        </span>
      </transition-group>
    </div>
  </div>
</template>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: all 0.4s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(100%);
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}
</style>
