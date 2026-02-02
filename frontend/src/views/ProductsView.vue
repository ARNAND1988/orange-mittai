<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { getProducts } from "@/services/productService"
import { useCart } from "@/services/CartService"
import { useSearch } from "@/services/SearchService"
import ProductCard from "@/components/ProductCard.vue"

const route = useRoute()
const router = useRouter()
const { searchQuery } = useSearch()
const { addToCart } = useCart()

const products = ref([])
const loading = ref(true)

/* LOAD ONCE */
onMounted(async () => {
  if (products.value.length) return
  const res = await getProducts()
  products.value = Array.isArray(res) ? res : res?.data ?? []
  loading.value = false
})

/* FILTER */
const filteredProducts = computed(() => {
  const tag = route.query.tag || null
  const query = (searchQuery.value || "").toLowerCase()

  return products.value.filter(p => {
    if (!p.is_active || p.stock <= 0) return false

    if (tag) {
      const hasTag = p.tags?.some(t =>
        t.is_active &&
        (t.type === "PROMOTION" || t.type === "LABEL") &&
        t.slug === tag
      )
      if (!hasTag) return false
    }

    if (query && !p.name.toLowerCase().includes(query)) return false

    return true
  })
})

/* PROMOTIONS */
const promotionSections = computed(() => {
  const map = {}
  filteredProducts.value.forEach(p => {
    p.tags?.filter(t => t.type === "PROMOTION").forEach(t => {
      map[t.slug] ??= { name: t.name, slug: t.slug, products: [] }
      map[t.slug].products.push(p)
    })
  })
  return Object.values(map)
})

/* CATEGORIES */
const categorySections = computed(() => {
  const map = {}
  filteredProducts.value.forEach(p => {
    const c = p.tags?.find(t => t.type === "CATEGORY")
    if (!c) return
    map[c.slug] ??= { name: c.name, slug: c.slug, products: [] }
    map[c.slug].products.push(p)
  })
  return Object.values(map)
})

/* HELPERS */
const getSubcategory = p =>
  p.tags?.find(t => t.type === "SUBCATEGORY")?.name || null

const getLabels = p =>
  p.tags?.filter(t => t.type === "LABEL" || t.type === "PROMOTION") || []

const clearFilter = () => {
  router.replace({ path: route.path, query: {} })
}
</script>

<template>
  <div class="bg-white py-8">
    <div class="max-w-7xl mx-auto space-y-14 px-4">

      <!-- CLEAR FILTER -->
      <button
        v-if="route.query.tag"
        @click="clearFilter"
        class="text-sm text-orange-600"
      >
        Clear filter ✕
      </button>

      <!-- LOADING -->
      <div v-if="loading" class="text-center py-20 text-gray-400">
        Loading products…
      </div>

      <!-- PROMOTIONS -->
      <section v-for="promo in promotionSections" :key="promo.slug">
        <h2 class="text-lg font-semibold">🔥 {{ promo.name }}</h2>
        <div class="flex gap-4 overflow-x-auto">
          <ProductCard
            v-for="p in promo.products"
            :key="p.id"
            :product="p"
            :subcategory="getSubcategory(p)"
            :labels="getLabels(p)"
            @add-to-cart="addToCart"
            class="flex-shrink-0"
          />
        </div>
      </section>

      <!-- CATEGORIES -->
      <section v-for="cat in categorySections" :key="cat.slug">
        <h2 class="text-xl font-semibold">{{ cat.name }}</h2>
        <div class="flex gap-4 overflow-x-auto">
          <ProductCard
            v-for="p in cat.products"
            :key="p.id"
            :product="p"
            :subcategory="getSubcategory(p)"
            :labels="getLabels(p)"
            @add-to-cart="addToCart"
            class="w-56 flex-shrink-0"
          />
        </div>
      </section>

    </div>
  </div>
</template>
