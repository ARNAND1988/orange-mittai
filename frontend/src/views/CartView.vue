<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useCart } from "@/services/CartService"
import { useAuth } from "@/services/AuthService"

const router = useRouter()
const { isAuthenticated } = useAuth()

const {
  cartItems,
  updateQuantity,
  removeFromCart,
  totalPrice,
} = useCart()

const showGuestPrompt = ref(false)

const formatPrice = (v) => Number(v).toFixed(2)

const increaseQty = (item) => {
  if (item.quantity < 5) updateQuantity(item.id, item.quantity + 1)
}
const decreaseQty = (item) => {
  if (item.quantity > 1) updateQuantity(item.id, item.quantity - 1)
}

const isLoggedIn = () => !!localStorage.getItem("user")

const goToCheckout = () => {
  if (isLoggedIn()) {
    router.push("/checkout")
  } else {
    showGuestPrompt.value = true
  }
}

const continueAsGuest = () => {
  router.push("/checkout?guest=true")
}
</script>

<template>
  <div class="max-w-5xl mx-auto py-8">
    <h1 class="text-2xl font-semibold mb-6">My Cart</h1>

    <!-- EMPTY -->
    <div
      v-if="cartItems.length === 0"
      class="bg-white border border-orange-200 rounded-xl shadow-sm p-6"
    >
      <p class="text-gray-600">
        Your cart is empty 🍊
      </p>

      <RouterLink
        to="/"
        class="inline-block mt-4 text-orange-600 font-medium hover:underline"
      >
        Browse products →
      </RouterLink>
    </div>
    <!-- CART ITEMS -->
    <div v-else class="space-y-4">
      <div
        v-for="item in cartItems"
        :key="item.id"
        class="flex gap-4 bg-white border rounded-xl p-4"
      >
        <!-- IMAGE -->
        <img
          :src="item.image"
          class="w-24 h-24 object-cover rounded-lg"
        />

        <!-- INFO -->
        <div class="flex-1">
          <h3 class="font-medium">{{ item.name }}</h3>
          <p class="text-sm text-gray-500">
            €{{ formatPrice(item.price) }} each
          </p>

          <!-- QTY -->
          <div class="flex items-center gap-2 mt-2">
            <button @click="decreaseQty(item)" class="px-2 bg-gray-200 rounded">−</button>
            <span>{{ item.quantity }}</span>
            <button @click="increaseQty(item)" class="px-2 bg-gray-200 rounded">+</button>
          </div>
        </div>

        <!-- TOTAL -->
        <div class="text-right">
          <p class="font-semibold">
            €{{ formatPrice(item.price * item.quantity) }}
          </p>
          <button
            @click="removeFromCart(item.id)"
            class="text-sm text-red-500 hover:underline"
          >
            Remove
          </button>
        </div>
      </div>

      <!-- TOTAL -->
      <div class="flex justify-between items-center bg-orange-50 p-4 rounded-xl">
        <span class="font-semibold">Total</span>
        <div class="text-right">
          <p class="text-lg font-semibold text-orange-600">
            €{{ formatPrice(totalPrice) }}
          </p>
          <button
            @click="goToCheckout"
            class="mt-2 bg-orange-500 text-white px-6 py-2 rounded-lg"
          >
            Proceed to Checkout →
          </button>
        </div>
      </div>
    </div>

    <!-- GUEST PROMPT MODAL -->
    <div
      v-if="showGuestPrompt"
      class="fixed inset-0 bg-black/40 flex items-center justify-center"
    >
      <div class="bg-white rounded-xl p-6 max-w-sm w-full">
        <h3 class="text-lg font-semibold mb-2">Continue Checkout</h3>
        <p class="text-sm text-gray-600 mb-4">
          Login to save your details, or continue as a guest.
        </p>

        <div class="space-y-3">
          <button
            @click="router.push('/auth')"
            class="w-full border px-4 py-2 rounded-lg"
          >
            Login
          </button>

          <button
            @click="continueAsGuest"
            class="w-full bg-orange-600 text-white px-4 py-2 rounded-lg"
          >
            Continue as Guest
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
