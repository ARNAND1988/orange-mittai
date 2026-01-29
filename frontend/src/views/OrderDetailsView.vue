<template>
  <div class="max-w-4xl mx-auto py-8 space-y-6">
    <RouterLink
      to="/orders"
      class="text-orange-600 hover:underline"
    >
      ← Back to orders
    </RouterLink>
    <div v-if="loading" class="bg-white p-6 rounded-xl shadow">
      Loading order...
    </div>

    <div v-else-if="!order" class="bg-white p-6 rounded-xl shadow">
      Order not found
    </div>

    <div v-else class="bg-white border rounded-xl shadow p-6 space-y-4">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <div>
          <h1 class="text-xl font-semibold">
            {{ order.order_id }}
          </h1>
          <p class="text-sm text-gray-500">
            {{ formatDate(order.created_at) }}
          </p>
        </div>

        <span
          class="px-3 py-1 text-sm rounded-full font-medium"
          :class="statusClass(order.status)"
        >
          {{ order.status.replaceAll("_", " ") }}
        </span>
      </div>

      <!-- Items -->
      <div class="border-t pt-4 space-y-2">
        <div
          v-for="item in order.items"
          :key="item.product_id"
          class="flex justify-between text-sm"
        >
          <span>
            {{ item.product_name }} × {{ item.quantity }}
          </span>
          <span>
            €{{ formatPrice(item.price * item.quantity) }}
          </span>
        </div>
      </div>

      <!-- Total -->
      <div class="border-t pt-4 flex justify-between font-semibold">
        <span>Total</span>
        <span>
          €{{ formatPrice(order.total_amount) }}
        </span>
      </div>

      <!-- Cancel button (CUSTOMER ONLY) -->
      <div
        v-if="order.status === 'PAYMENT_PENDING'"
        class="border-t pt-4"
      >
        <button
          @click="openCancelModal"
          class="bg-red-500 hover:bg-red-600
                 text-white px-4 py-2 rounded-lg
                 text-sm font-medium transition"
        >
          Cancel Order
        </button>
      </div>
    </div>

    <!-- Cancel Confirmation Modal (Flowbite style) -->
    <div
      v-if="showCancelModal"
      class="fixed inset-0 z-50 flex items-center justify-center
             bg-black bg-opacity-50"
    >
      <div class="bg-white rounded-lg shadow-lg max-w-md w-full p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-3">
          Cancel Order?
        </h3>

        <p class="text-sm text-gray-600 mb-6">
          Are you sure you want to cancel
          <span class="font-medium">
            {{ order?.order_id }}
          </span
          >?
          <br />
          This action cannot be undone.
        </p>

        <div class="flex justify-end gap-3">
          <button
            @click="closeCancelModal"
            class="px-4 py-2 text-sm rounded-lg
                   bg-gray-200 hover:bg-gray-300"
          >
            No, keep order
          </button>

          <button
            @click="confirmCancelOrder"
            class="px-4 py-2 text-sm rounded-lg
                   bg-red-600 hover:bg-red-700
                   text-white font-medium"
          >
            Yes, cancel order
          </button>
        </div>
      </div>
    </div>

    <!-- Flowbite Toast -->
    <div
      v-if="toast.show"
      class="fixed top-20 right-6 z-[60]"
    >
      <div
        class="flex items-center max-w-xs p-4 rounded-lg shadow text-sm"
        :class="toast.type === 'success'
          ? 'bg-green-100 text-green-800'
          : 'bg-red-100 text-red-800'"
      >
        <span class="font-medium">
          {{ toast.message }}
        </span>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted, nextTick } from "vue"
import { useRoute } from "vue-router"
import api from "@/services/api"
import { getOrders, cancelOrder } from "@/services/orderService";

const invoiceRef = ref(null)
const selectedOrder = ref(null)

const route = useRoute()
const order = ref(null)
const loading = ref(true)


// Modal state
const showCancelModal = ref(false)

// Toast state
const toast = ref({
  show: false,
  message: "",
  type: "success",
})

const showToast = (message, type = "success") => {
  toast.value = { show: true, message, type }

  setTimeout(() => {
    toast.value.show = false
  }, 3000)
}

onMounted(async () => {
  const orders = await getOrders()
  order.value = orders.find(
    o => o.order_id === route.params.orderId
  )
  loading.value = false
})

const openCancelModal = () => {
  showCancelModal.value = true
}

const closeCancelModal = () => {
  showCancelModal.value = false
}

const confirmCancelOrder = async () => {
  try {
    await cancelOrder(order.value.order_id)

    order.value.status = "CANCELLED"
    showToast("Order cancelled successfully")
  } catch (err) {
    showToast(err?.detail || "Failed to cancel order", "error")
  } finally {
    closeCancelModal()
  }
}

// ✅ Price formatter → Euro, 2 decimals
const formatPrice = (value) => {
  return Number(value).toFixed(2)
}

const formatDate = (date) =>
  new Date(date).toLocaleString()

const statusClass = (status) => ({
  PAYMENT_PENDING: "bg-yellow-100 text-yellow-800",
  PROCESSING: "bg-blue-100 text-blue-800",
  COMPLETED: "bg-green-100 text-green-800",
  CANCELLED: "bg-gray-100 text-gray-800",
  FAILED: "bg-red-100 text-red-800",
  REFUNDED: "bg-purple-100 text-purple-800",
}[status])
</script>
