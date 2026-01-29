<script setup>
import { computed, ref, onMounted } from "vue"
import api from "@/services/api"
import { getAdminOrders, patchAdminOrderStatus } from "@/services/orderService";

const orders = ref([])
const loading = ref(true)
const selectedStatus = ref("ALL")

const dateRange = ref({
  from: "",
  to: "",
})

const statuses = [
  "PAYMENT_PENDING",
  "PROCESSING",
  "COMPLETED",
  "CANCELLED",
  "REFUNDED",
  "FAILED",
]

const filteredOrders = computed(() => {
  return orders.value.filter((order) => {
    // STATUS FILTER
    if (
      selectedStatus.value !== "ALL" &&
      order.status !== selectedStatus.value
    ) {
      return false
    }

    // DATE FILTER
    const orderDate = new Date(order.created_at)

    if (dateRange.value.from) {
      const fromDate = new Date(dateRange.value.from)
      if (orderDate < fromDate) return false
    }

    if (dateRange.value.to) {
      const toDate = new Date(dateRange.value.to)
      // include entire day
      toDate.setHours(23, 59, 59, 999)
      if (orderDate > toDate) return false
    }

    return true
  })
})



const fetchOrders = async () => {
  loading.value = true;

  try {
    console.log("🔥 fetchOrders called");
    const data = await getAdminOrders();

    orders.value = data.map((o) => ({
      ...o,
      _originalStatus: o.status,
    }));
  } catch (err) {
    showToast(err?.detail || "Failed to load admin orders", "error");
  } finally {
    loading.value = false;
  }
};

const saveStatus = async (order) => {
  if (order.status === order._originalStatus) return;

  try {
    await patchAdminOrderStatus(order.order_id, order.status);
    order._originalStatus = order.status;
    showToast("Order status updated successfully");
  } catch (err) {
    showToast(err?.detail || "Failed to update status", "error");
    order.status = order._originalStatus;
  }
};


const toast = ref({
  show: false,
  message: "",
  type: "success", // success | error
})

const showToast = (message, type = "success") => {
  toast.value = { show: true, message, type }

  setTimeout(() => {
    toast.value.show = false
  }, 3000)
}

onMounted(fetchOrders)

const exportOrdersPdf = async () => {
  try {
    const pdfMakeModule = await import("pdfmake/build/pdfmake")
    const pdfFonts = await import("pdfmake/build/vfs_fonts")

    const pdfMake =
      pdfMakeModule.default ?? pdfMakeModule

    pdfMake.vfs = pdfFonts.default.vfs

    // TABLE BODY
    const tableBody = [
      [
        { text: "Order ID", bold: true },
        { text: "Total (€)", bold: true },
        { text: "Status", bold: true },
        { text: "Created At", bold: true },
      ],
      ...filteredOrders.value.map((order) => [
        order.order_id,
        Number(order.total_amount).toFixed(2),
        order.status.replaceAll("_", " "),
        new Date(order.created_at).toLocaleString(),
      ]),
    ]

    // 📦 AGGREGATE PRODUCTS ACROSS ORDERS
    const productMap = {}

    filteredOrders.value.forEach(order => {
      order.items.forEach(item => {
        const productId = item.product_id

        if (!productMap[productId]) {
          productMap[productId] = {
            name: item.product.name,
            totalQuantity: 0,
          }
        }

        productMap[productId].totalQuantity += item.quantity
      })
    })

    const productSummary = Object.values(productMap).sort(
      (a, b) => b.totalQuantity - a.totalQuantity
    )

    const productTableBody = [
      [
        { text: "Product Name", bold: true },
        { text: "Total Quantity", bold: true, alignment: "right" },
      ],
    ]

    productSummary.forEach(p => {
      productTableBody.push([
        p.name,
        { text: p.totalQuantity.toString(), alignment: "right" },
      ])
    })
    const totalProductCount = productSummary.length
    const totalQuantity = productSummary.reduce(
      (sum, p) => sum + p.totalQuantity,
      0
    )

    const docDefinition = {
      pageSize: "A4",
      pageOrientation: "landscape",
      pageMargins: [40, 40, 40, 40],

    content: [
      // ================= PAGE 1 =================
      { text: "Admin Orders Report", style: "title" },
      {
        text: `Generated on: ${new Date().toLocaleString()}`,
        margin: [0, 0, 0, 15],
        fontSize: 10,
      },

      {
        table: {
          headerRows: 1,
          widths: ["*", "auto", "auto", "*"],
          body: tableBody,
        },
        layout: "lightHorizontalLines",
      },

      // ================= PAGE 2 =================
      {
        text: "Product-wise Order Summary",
        style: "title",
        pageBreak: "before",
      },
      {
        text: `Status: ${selectedStatus.value}`,
        margin: [0, 0, 0, 15],
        fontSize: 10,
      },

      {
        table: {
          headerRows: 1,
          widths: ["*", "auto"],
          body: productTableBody,
        },
        layout: "lightHorizontalLines",
      },
      {
        columns: [
          {
            text: `Total Products: ${totalProductCount}`,
            bold: true,
          },
          {
            text: `Total Quantity: ${totalQuantity}`,
            alignment: "right",
            bold: true,
          },
        ],
        margin: [0, 15, 0, 0],
      },

    ],


      styles: {
        title: {
          fontSize: 18,
          bold: true,
          margin: [0, 0, 0, 10],
        },
      },
    }

    pdfMake.createPdf(docDefinition).download(
      `admin-orders-${Date.now()}.pdf`
    )

    showToast("Orders report exported successfully")
  } catch (err) {
    console.error("Failed to export orders PDF", err)
    showToast("Failed to export orders report", "error")
  }
}


</script>

<template>
  <div class="max-w-6xl mx-auto py-8">
<div class="flex justify-between items-center mb-4">
  <h1 class="text-2xl font-semibold">
    Admin – Orders
  </h1>

<button
  @click="exportOrdersPdf"
  :disabled="filteredOrders.length === 0"
  class="px-4 py-2 rounded-lg text-sm font-medium
         bg-black text-white
         disabled:bg-gray-300 disabled:cursor-not-allowed"
>
  Export PDF
</button>
</div>
<!-- FILTER BAR -->
<div class="bg-white border rounded-lg p-4 mb-4">
  <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">

    <!-- STATUS FILTER -->
    <div>
      <label class="block text-sm font-medium mb-1">
        Status
      </label>
      <select
        v-model="selectedStatus"
        class="w-full border rounded px-3 py-2 text-sm"
      >
        <option value="ALL">All statuses</option>
        <option
          v-for="s in statuses"
          :key="s"
          :value="s"
        >
          {{ s.replaceAll("_", " ") }}
        </option>
      </select>
    </div>

    <!-- FROM DATE -->
    <div>
      <label class="block text-sm font-medium mb-1">
        From date
      </label>
      <input
        type="date"
        v-model="dateRange.from"
        class="w-full border rounded px-3 py-2 text-sm"
      />
    </div>

    <!-- TO DATE -->
    <div>
      <label class="block text-sm font-medium mb-1">
        To date
      </label>
      <input
        type="date"
        v-model="dateRange.to"
        class="w-full border rounded px-3 py-2 text-sm"
      />
    </div>
  </div>

  <!-- RESET -->
  <div class="mt-3 flex justify-end">
    <button
      @click="() => {
        selectedStatus = 'ALL'
        dateRange.from = ''
        dateRange.to = ''
      }"
      class="text-sm text-gray-600 hover:underline"
    >
      Reset filters
    </button>
  </div>
</div>

    <div v-if="loading" class="bg-white p-6 rounded shadow">
      Loading orders...
    </div>

    <table
      v-else
      class="w-full bg-white border rounded-lg shadow"
    >
      <thead class="bg-gray-100 text-sm text-gray-700">
        <tr>
          <th class="p-3 text-left">Order ID</th>
          <th class="p-3 text-left">Total (€)</th>
          <th class="p-3 text-left">Status</th>
          <th class="p-3 text-left">Action</th>
          <th class="p-3 text-left">Created</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="order in filteredOrders"
          :key="order.order_id"
          class="border-t"
        >
          <td class="p-3 font-medium">
            {{ order.order_id }}
          </td>

          <td class="p-3">
            €{{ Number(order.total_amount).toFixed(2) }}
          </td>

          <!-- Status dropdown -->
          <td class="p-3">
            <select
              v-model="order.status"
              class="border rounded px-2 py-1 text-sm"
            >
              <option
                v-for="s in statuses"
                :key="s"
                :value="s"
              >
                {{ s.replaceAll("_", " ") }}
              </option>
            </select>
          </td>

          <!-- Update button -->
          <td class="p-3">
            <button
              @click="saveStatus(order)"
              :disabled="order.status === order._originalStatus"
              class="px-3 py-1 rounded text-sm font-medium transition"
              :class="order.status === order._originalStatus
                ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                : 'bg-orange-500 hover:bg-orange-600 text-white'"
            >
              Update
            </button>
          </td>

          <td class="p-3 text-sm text-gray-500">
            {{ new Date(order.created_at).toLocaleString() }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
