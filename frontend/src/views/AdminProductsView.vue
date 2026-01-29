<script setup>
import { ref, onMounted } from "vue"
import api from "@/services/api"
import { fetchProductsForAdmin, softDelete, restore, updateProduct  } from "@/services/productService";

const products = ref([])

const fetchProducts = async () => {
  products.value = await fetchProductsForAdmin()
  console.log(products.value)
}

const softDeleteFn = async (product) => {
  if (!confirm("Deactivate this product?")) return

  await softDelete(product.id)
  product.is_active = false
}

const restoreFn = async (product) => {
  await restore(product.id)
  product.is_active = true
}


const saveProduct = async (product) => {
  await updateProduct(
    product.id,
    product.name,
    product.price,
    product.stock,)
}

onMounted(fetchProducts)
</script>

<template>
  <div class="max-w-6xl mx-auto py-8">
    <h1 class="text-2xl font-semibold mb-6">
      Admin – Products
    </h1>

    <table class="w-full bg-white border rounded shadow">
      <thead class="bg-gray-100">
        <tr>
          <th class="p-3 text-left">Name</th>
          <th class="p-3 text-left">Price (€)</th>
          <th class="p-3 text-left">Stock</th>
          <th class="p-3"></th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="product in products"
          :key="product.id"
          class="border-t"
          :class="!product.is_active ? 'opacity-50 bg-gray-50' : ''"
        >
          <td class="p-3">
            <input v-model="product.name" class="border px-2 py-1 w-full" />
          </td>

          <td class="p-3">
            <input
              v-model.number="product.price"
              type="number"
              step="0.01"
              class="border px-2 py-1 w-full"
            />
          </td>

          <td class="p-3">
            <input
              v-model.number="product.stock"
              type="number"
              class="border px-2 py-1 w-full"
            />
          </td>

<td class="p-3 space-x-2">
  <button
    @click="saveProduct(product)"
    class="text-orange-600 hover:underline text-sm"
  >
    Save
  </button>

  <button
    v-if="product.is_active"
    @click="softDeleteFn(product)"
    class="text-red-600 hover:underline text-sm"
  >
    Deactivate
  </button>

  <button
    v-else
    @click="restoreFn(product)"
    class="text-green-600 hover:underline text-sm"
  >
    Restore
  </button>
</td>

        </tr>
      </tbody>
    </table>
  </div>
</template>
