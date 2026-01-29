<template>
  <div class="max-w-4xl mx-auto p-6 space-y-6">
    <h1 class="text-2xl font-semibold">
      Checkout
    </h1>

    <div
      v-if="cartItems.length === 0"
      class="p-6 text-center text-gray-500 bg-white rounded-lg shadow"
    >
      Your cart is empty
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="item in cartItems"
        :key="item.productId"
        class="flex justify-between border-b pb-2"
      >
        <span>
          {{ item.name }} × {{ item.quantity }}
        </span>
        <span>
          €{{ formatPrice(item.price * item.quantity) }}
        </span>
      </div>

      <div class="flex justify-between text-lg font-semibold">
        <span>Total</span>
        <span>
          €{{ formatPrice(cartTotal) }}
        </span>
      </div>

      <button
        @click="placeOrder"
        class="w-full bg-orange-500 hover:bg-orange-600
               text-white py-3 rounded-lg transition"
      >
        Place Order
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import api from "@/services/api"
import { useCart } from "@/services/CartService"
import { createOrder } from "@/services/OrderService"

const { clearCart } = useCart()

// Cart items (from localStorage)
const cartItems = ref(
  JSON.parse(localStorage.getItem("cart") || "[]")
)

// Total calculation
const cartTotal = computed(() =>
  cartItems.value.reduce(
    (sum, i) => sum + i.price * i.quantity,
    0
  )
)

// Price formatter → 2 decimals
const formatPrice = (value) => {
  return Number(value).toFixed(2)
}

const router = useRouter()

const placeOrder = async () => {
  const payload = {
    items: cartItems.value.map(i => ({
      product_id: i.productId ?? i.id, // 🔥 fallback
      quantity: Number(i.quantity),
    })),
    payment_method: "COD",
  };

  console.log("ORDER PAYLOAD:", payload); // 👈 debug

  createOrder(payload)

  clearCart()
  router.push("/orders");
};
</script>
