<script setup>
import { ref, onMounted, computed } from "vue"
import { useRouter, useRoute } from "vue-router"
import api from "@/services/api"
import {
  createProductWithImage,
  updateProductWithImage
} from "@/services/productService"

const router = useRouter()
const route = useRoute()

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)

/* -----------------------
   FORM STATE
------------------------ */
const form = ref({
  name: "",
  description: "",
  price: 0,
  stock: 0,
  is_active: true
})

const imageFile = ref(null)
const imagePreview = ref(null)

/* -----------------------
   TAGS
------------------------ */
const tags = ref([])
const selectedTagIds = ref([])

const activeTags = computed(() =>
  Array.isArray(tags.value)
    ? tags.value.filter(t => t.is_active !== false)
    : []
)

const tagsByType = computed(() =>
  activeTags.value.reduce((acc, tag) => {
    const type = tag.type || "Other"
    acc[type] = acc[type] || []
    acc[type].push(tag)
    return acc
  }, {})
)

/* -----------------------
   FETCH TAGS
------------------------ */
const fetchTags = async () => {
  try {
    const res = await api.get("/tags")
    tags.value = Array.isArray(res) ? res : res.data || []
  } catch (e) {
    console.error("Failed to fetch tags", e)
    tags.value = []
  }
}

/* -----------------------
   FETCH PRODUCT (EDIT)
------------------------ */
const fetchProduct = async () => {
  if (!isEdit.value) return

  try {
    const res = await api.get(`/admin/products/${route.params.id}`)
    const product = res
    if (!product) return

    form.value = {
      name: product.name ?? "",
      description: product.description ?? "",
      price: product.price ?? 0,
      stock: product.stock ?? 0,
      is_active: product.is_active ?? true
    }

    selectedTagIds.value = Array.isArray(product.tags)
      ? product.tags.map(t => t.id)
      : []

    imagePreview.value = product.image ?? null
  } catch (err) {
    console.error("Failed to load product", err)
    alert("Failed to load product for editing")
    router.push("/admin/products")
  }
}

/* -----------------------
   IMAGE SELECT
------------------------ */
const onImageSelect = (e) => {
  const file = e.target.files[0]
  if (!file) return
  imageFile.value = file
  imagePreview.value = URL.createObjectURL(file)
}

/* -----------------------
   SUBMIT
------------------------ */
const submit = async () => {
  if (!form.value.name) {
    alert("Product name is required")
    return
  }

  if (!isEdit.value && !imageFile.value) {
    alert("Image is required")
    return
  }

  loading.value = true

  try {
    const payload = {
      ...form.value,
      tag_ids: selectedTagIds.value,
      imageFile: imageFile.value || null
    }

    if (isEdit.value) {
      await updateProductWithImage(route.params.id, payload)
    } else {
      await createProductWithImage(payload)
    }

    router.push("/admin/products")
  } catch (err) {
    console.error(err)
    alert("Failed to save product")
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchTags()
  await fetchProduct()
})
</script>

<template>
  <div class="max-w-2xl mx-auto py-8">
    <h1 class="text-2xl font-semibold mb-6">
      {{ isEdit ? "Edit Product" : "Add Product" }}
    </h1>

    <div class="space-y-5 bg-white p-6 border rounded-xl shadow">

      <!-- STATUS -->
      <div
        class="flex justify-between items-center
               bg-orange-50 border border-orange-200
               rounded-lg px-4 py-3"
      >
        <div>
          <p class="text-sm font-medium">Product Status</p>
          <p class="text-xs text-gray-500">Visible in store</p>
        </div>

        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="form.is_active" class="sr-only peer">
          <div
            class="w-11 h-6 bg-gray-300 rounded-full
                   peer-checked:bg-orange-600 transition
                   after:absolute after:top-0.5 after:left-1
                   after:w-5 after:h-5 after:bg-white after:rounded-full
                   peer-checked:after:translate-x-5"
          ></div>
        </label>
      </div>

      <!-- NAME -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Product Name
        </label>
        <input
          v-model="form.name"
          placeholder="Product name"
          class="border px-3 py-2 w-full rounded"
        />
      </div>

      <!-- DESCRIPTION -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          v-model="form.description"
          placeholder="Description"
          rows="3"
          class="border px-3 py-2 w-full rounded"
        />
      </div>

      <!-- PRICE + STOCK -->
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Price
          </label>
          <div class="relative">
            <span
              class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500"
            >
              €
            </span>
            <input
              v-model.number="form.price"
              type="number"
              placeholder="0.00"
              class="border pl-7 pr-3 py-2 w-full rounded"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Stock
          </label>
          <input
            v-model.number="form.stock"
            type="number"
            placeholder="Stock"
            class="border px-3 py-2 w-full rounded"
          />
        </div>
      </div>

      <!-- TAGS -->
      <div v-if="Object.keys(tagsByType).length">
        <div v-for="(group, type) in tagsByType" :key="type" class="mb-4">
          <p class="text-xs font-semibold text-orange-600 mb-2">
            {{ type }}
          </p>

          <div class="flex flex-wrap gap-2">
            <label
              v-for="tag in group"
              :key="tag.id"
              class="cursor-pointer"
            >
              <input
                type="checkbox"
                :value="tag.id"
                v-model="selectedTagIds"
                class="hidden peer"
              />
              <span
                class="px-3 py-1.5 rounded-full text-xs font-medium border
                       bg-orange-50 text-orange-700 border-orange-200
                       peer-checked:bg-orange-600 peer-checked:text-white"
              >
                {{ tag.name }}
              </span>
            </label>
          </div>
        </div>
      </div>

      <!-- NO TAGS -->
      <p v-else class="text-sm text-gray-400 italic">
        No tags available
      </p>

      <!-- IMAGE -->
      <div>
        <label
          class="inline-flex items-center gap-2 cursor-pointer
                 bg-orange-500 text-white px-4 py-2 rounded-lg"
        >
          📷 {{ imageFile || imagePreview ? "Change Image" : "Browse Image" }}
          <input type="file" class="hidden" @change="onImageSelect" />
        </label>

        <img
          v-if="imagePreview"
          :src="imagePreview"
          class="mt-4 w-32 h-32 object-cover rounded-xl border"
        />
      </div>

      <!-- SUBMIT -->
      <button
        @click="submit"
        :disabled="loading"
        class="bg-orange-600 text-white px-4 py-2 rounded-lg
               hover:bg-orange-700 disabled:opacity-50"
      >
        <span v-if="loading">
          {{ isEdit ? "Updating..." : "Saving..." }}
        </span>
        <span v-else>
          {{ isEdit ? "Update Product" : "Save Product" }}
        </span>
      </button>
    </div>
  </div>
</template>
