<template>
  <div class="max-w-4xl mx-auto py-8 space-y-6">
    <h1 class="text-2xl font-semibold text-gray-800">
      My Orders
    </h1>

    <!-- Loading -->
    <div
      v-if="loading"
      class="bg-white border border-gray-200 rounded-xl shadow-sm p-6 text-gray-600"
    >
      Loading your orders...
    </div>

    <!-- Empty -->
    <div
      v-else-if="!orders.length"
      class="bg-white border border-orange-200 rounded-xl shadow-sm p-6"
    >
      <p class="text-gray-600">
        You haven’t placed any orders yet.
      </p>

      <RouterLink
        to="/"
        class="inline-block mt-4 text-orange-600 font-medium hover:underline"
      >
        Start shopping →
      </RouterLink>
    </div>

    <!-- Orders -->
    <div v-else class="space-y-4">
      <div
        v-for="order in orders"
        :key="order.order_id"
        class="bg-white border border-gray-200 rounded-xl shadow-sm
               p-6 space-y-4 hover:shadow-md hover:border-orange-300
               transition cursor-pointer"
        @click="goToOrder(order.order_id)"
      >
        <!-- ================= HEADER ================= -->
        <div class="flex justify-between items-center gap-4">
          <div>
            <h1 class="text-xl font-semibold">
              {{ order.order_id }}
            </h1>
            <p class="text-sm text-gray-500">
              {{ formatDate(order.created_at) }}
            </p>
          </div>

          <div class="flex items-center gap-3">
            <span
              class="px-3 py-1 text-sm rounded-full font-medium"
              :class="statusClass(order.status)"
            >
              {{ order.status.replaceAll("_", " ") }}
            </span>

            <button
              v-if="order.status === 'COMPLETED'"
              @click.stop="downloadInvoice(order.order_id)"
              class="text-sm px-3 py-1 rounded-lg
                     border border-gray-300
                     hover:bg-gray-100 transition"
            >
              Invoice
            </button>
          </div>
        </div>

        <!-- ================= SUMMARY ================= -->
        <div class="text-sm text-gray-700">
          {{ order.items.length }} items ·
          <span class="font-medium">
            ₹{{ order.total_amount }}
          </span>
        </div>

        <!-- ================= ADDRESS ================= -->
        <div
          v-if="order.address"
          class="border-t pt-3 text-sm text-gray-700"
        >
          <p class="font-medium text-gray-800 mb-1">
            Delivery Address
          </p>

          <p>
            {{ order.address.name }} · {{ order.address.phone }}
          </p>

          <p>
            {{ order.address.house_number }},
            {{ order.address.line1 }}
            <span v-if="order.address.line2">
              , {{ order.address.line2 }}
            </span>
          </p>

          <p>
            {{ order.address.city }},
            {{ order.address.state }}
            – {{ order.address.postal_code }}
          </p>

          <p>{{ order.address.country }}</p>
        </div>

        <!-- ================= ITEMS PREVIEW ================= -->
        <div class="border-t pt-3 space-y-1">
          <div
            v-for="item in order.items.slice(0, 2)"
            :key="item.product_id"
            class="text-sm text-gray-600 flex justify-between"
          >
            <span>
              {{ item.product_name }} × {{ item.quantity }}
            </span>
            <span>
              ₹{{ item.price * item.quantity }}
            </span>
          </div>

          <p
            v-if="order.items.length > 2"
            class="text-xs text-orange-600 font-medium mt-1"
          >
            View all items →
          </p>
        </div>
      </div>
    </div>

    <!-- Invoice PDF -->
    <InvoicePdf
      v-if="selectedOrder"
      ref="invoiceRef"
      :order="selectedOrder"
    />
  </div>
</template>

<script setup>
import { nextTick, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import InvoicePdf from "@/components/InvoicePdf.vue";
import { getOrders, getOrderById } from "@/services/orderService";

const router = useRouter();

const orders = ref([]);
const loading = ref(true);
const selectedOrder = ref(null);
const invoiceRef = ref(null);

const downloadInvoice = async (orderId) => {
  try {
    const res = await getOrderById(orderId);
    const fullOrder = res?.data ?? res;

    selectedOrder.value = fullOrder;
    await nextTick();
    invoiceRef.value.generate();
  } catch (err) {
    console.error("Invoice generation failed:", err);
  }
};

onMounted(async () => {
  const res = await getOrders();
  orders.value = Array.isArray(res) ? res : [];
  console.log(orders)
  loading.value = false;
});

const goToOrder = (id) => {
  router.push(`/orders/${id}`);
};

const formatDate = (date) =>
  new Date(date).toLocaleString();

const statusClass = (status) => ({
  PAYMENT_PENDING: "bg-yellow-100 text-yellow-800",
  PROCESSING: "bg-blue-100 text-blue-800",
  COMPLETED: "bg-green-100 text-green-800",
  CANCELLED: "bg-gray-100 text-gray-800",
  FAILED: "bg-red-100 text-red-800",
  REFUNDED: "bg-purple-100 text-purple-800",
}[status]);
</script>
