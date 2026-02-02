<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import {
  fetchProductsForAdmin,
  softDelete,
  restore
} from "@/services/productService"

const router = useRouter()
const products = ref([])

const fetchProducts = async () => {
  products.value = await fetchProductsForAdmin()
}

const toggleActive = async (product) => {
  if (product.is_active) {
    if (!confirm("Deactivate this product?")) return
    await softDelete(product.id)
    product.is_active = false
  } else {
    await restore(product.id)
    product.is_active = true
  }
}

onMounted(fetchProducts)
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
            ₹{{ product.price }}
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
            @click="toggleActive(product)"
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
  </div>
</template>
