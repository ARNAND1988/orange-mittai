<script setup>
import { useCart } from "@/services/CartService"
import { useRouter } from "vue-router"

const router = useRouter()

const {
  cartItems,
  updateQuantity,
  removeFromCart,
  totalPrice,
} = useCart()

// Price formatter → € with 2 decimals
const formatPrice = (value) => {
  return Number(value).toFixed(2)
}

// Quantity controls (1–5)
const increaseQty = (item) => {
  if (item.quantity < 5) {
    updateQuantity(item.id, item.quantity + 1)
  }
}

const decreaseQty = (item) => {
  if (item.quantity > 1) {
    updateQuantity(item.id, item.quantity - 1)
  }
}

const goToCheckout = () => {
  router.push("/checkout")
}
</script>

<template>
  <div class="max-w-5xl mx-auto py-8">
    <h1 class="text-2xl font-semibold text-gray-800 mb-6">
      My Cart
    </h1>

    <!-- Empty cart -->
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

    <!-- Cart items -->
    <div v-else class="space-y-4">
      <!-- Cart item -->
      <div
        v-for="item in cartItems"
        :key="item.id"
        class="flex items-center justify-between
               bg-white border border-orange-200
               rounded-xl p-4"
      >
        <!-- Product info -->
        <div>
          <h3 class="font-medium text-gray-800">
            {{ item.name }}
          </h3>
          <p class="text-sm text-gray-500">
            €{{ formatPrice(item.price) }} each
          </p>
        </div>

        <!-- Quantity -->
        <div class="flex items-center gap-2">
          <button
            @click="decreaseQty(item)"
            :disabled="item.quantity <= 1"
            class="px-2 py-1 rounded bg-gray-200
                   disabled:opacity-40 disabled:cursor-not-allowed"
          >
            −
          </button>

          <span class="w-6 text-center font-medium">
            {{ item.quantity }}
          </span>

          <button
            @click="increaseQty(item)"
            :disabled="item.quantity >= 5"
            class="px-2 py-1 rounded bg-gray-200
                   disabled:opacity-40 disabled:cursor-not-allowed"
          >
            +
          </button>
        </div>

        <!-- Line total -->
        <div class="text-right">
          <p class="font-medium text-gray-800">
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

      <!-- Total + Checkout -->
      <div
        class="flex justify-between items-center
               bg-orange-50 border border-orange-200
               rounded-xl p-4 mt-6"
      >
        <div>
          <span class="block font-semibold text-gray-800">
            Total
          </span>
          <span class="block text-sm text-gray-500">
            Taxes calculated at checkout
          </span>
        </div>

        <div class="text-right space-y-2">
          <p class="font-semibold text-orange-600 text-lg">
            €{{ formatPrice(totalPrice) }}
          </p>

          <button
            @click="goToCheckout"
            class="bg-orange-500 hover:bg-orange-600
                   text-white px-6 py-2 rounded-lg
                   font-medium transition"
          >
            Proceed to Checkout →
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
