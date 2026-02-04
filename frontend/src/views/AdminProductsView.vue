<script setup>
import { ref, onMounted, computed } from "vue"
import { useRouter } from "vue-router"
import {
  fetchProductsForAdmin,
  softDelete,
  restore
} from "@/services/productService"

const router = useRouter()
const products = ref([])

/* -----------------------
   MODAL STATE
------------------------ */
const showConfirm = ref(false)
const selectedProduct = ref(null)
const confirmLoading = ref(false)

/* 🔥 mode: 'activate' | 'deactivate' */
const actionMode = ref("deactivate")

/* -----------------------
   COMPUTED
------------------------ */
const modalTitle = computed(() =>
  actionMode.value === "deactivate"
    ? "Deactivate product?"
    : "Activate product?"
)

const modalMessage = computed(() =>
  actionMode.value === "deactivate"
    ? "will no longer be visible in the store."
    : "will become visible in the store."
)

const confirmButtonText = computed(() =>
  actionMode.value === "deactivate"
    ? "Deactivate"
    : "Activate"
)

const confirmButtonClass = computed(() =>
  actionMode.value === "deactivate"
    ? "bg-red-600 hover:bg-red-700"
    : "bg-green-600 hover:bg-green-700"
)

/* -----------------------
   FETCH
------------------------ */
const fetchProducts = async () => {
  products.value = await fetchProductsForAdmin()
}

onMounted(fetchProducts)

/* -----------------------
   ACTIONS
------------------------ */
const requestAction = (product) => {
  selectedProduct.value = product
  actionMode.value = product.is_active ? "deactivate" : "activate"
  showConfirm.value = true
}

const confirmAction = async () => {
  if (!selectedProduct.value) return
  confirmLoading.value = true

  try {
    if (actionMode.value === "deactivate") {
      await softDelete(selectedProduct.value.id)
      selectedProduct.value.is_active = false
    } else {
      await restore(selectedProduct.value.id)
      selectedProduct.value.is_active = true
    }
  } finally {
    confirmLoading.value = false
    showConfirm.value = false
    selectedProduct.value = null
  }
}
</script>

<template>
  <div class="max-w-7xl mx-auto py-8">

    <!-- HEADER -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-semibold text-gray-800">
        Products
      </h1>

      <button
        @click="router.push('/admin/products/add')"
        class="bg-orange-600 text-white px-4 py-2 rounded-lg
               hover:bg-orange-700 shadow-sm"
      >
        + Add Product
      </button>
    </div>

    <!-- PRODUCT GRID -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="product in products"
        :key="product.id"
        class="bg-white rounded-xl border shadow-sm
               hover:shadow-md transition p-4"
        :class="!product.is_active && 'opacity-60'"
      >
        <!-- IMAGE -->
        <img
          :src="product.image"
          class="w-full h-40 object-cover rounded-lg mb-3"
        />

        <!-- INFO -->
        <h3 class="font-medium text-gray-800 truncate">
          {{ product.name }}
        </h3>

        <p class="text-sm text-gray-500 line-clamp-2">
          {{ product.description }}
        </p>

        <!-- META -->
        <div class="flex justify-between items-center mt-3">
          <span class="font-semibold text-orange-600">
            €{{ product.price }}
          </span>

          <span
            class="text-xs px-2 py-1 rounded-full"
            :class="
              product.is_active
                ? 'bg-green-100 text-green-700'
                : 'bg-gray-200 text-gray-600'
            "
          >
            {{ product.is_active ? 'Active' : 'Inactive' }}
          </span>
        </div>

        <!-- ACTIONS -->
        <div class="flex justify-between items-center mt-4">
          <button
            @click="router.push(`/admin/products/${product.id}`)"
            class="text-sm font-medium text-orange-600 hover:underline"
          >
            Edit
          </button>

          <button
            @click="requestAction(product)"
            class="text-sm font-medium"
            :class="
              product.is_active
                ? 'text-red-600 hover:underline'
                : 'text-green-600 hover:underline'
            "
          >
            {{ product.is_active ? 'Deactivate' : 'Activate' }}
          </button>
        </div>
      </div>
    </div>

    <!-- CONFIRM MODAL -->
    <div
      v-if="showConfirm"
      class="fixed inset-0 z-50 flex items-center justify-center
             bg-black/40 backdrop-blur-sm"
    >
      <div
        class="bg-white rounded-xl shadow-xl max-w-sm w-full p-6
               animate-scale-in"
      >
        <h3 class="text-lg font-semibold text-gray-800 mb-2">
          {{ modalTitle }}
        </h3>

        <p class="text-sm text-gray-600 mb-4">
          <span class="font-medium text-gray-800">
            {{ selectedProduct?.name }}
          </span>
          {{ modalMessage }}
        </p>

        <div class="flex justify-end gap-3">
          <button
            @click="showConfirm = false"
            class="px-4 py-2 rounded-lg text-sm
                   border border-gray-300 text-gray-700
                   hover:bg-gray-100"
            :disabled="confirmLoading"
          >
            Cancel
          </button>

          <button
            @click="confirmAction"
            class="px-4 py-2 rounded-lg text-sm text-white
                   disabled:opacity-50"
            :class="confirmButtonClass"
            :disabled="confirmLoading"
          >
            {{ confirmLoading ? "Please wait..." : confirmButtonText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-scale-in {
  animation: scale-in 0.15s ease-out;
}
</style>
