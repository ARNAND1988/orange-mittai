<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import { FireIcon, StarIcon } from "@heroicons/vue/24/solid"
import { useTagMenu } from "@/services/TagMenuService"
import { useSearch } from "@/services/SearchService"

const router = useRouter()
const route = useRoute()
const open = ref(false)
const { searchQuery } = useSearch()

/* TAGS */
const { groupedTags, fetchTags } = useTagMenu()
onMounted(fetchTags)

/* ICONS */
const iconMap = {
  PROMOTION: FireIcon,
  LABEL: StarIcon,
}

/* MENU */
const menu = computed(() => {
  const items = []
  const tags = groupedTags.value || {}

  tags.PROMOTION?.forEach(tag => {
    items.push({
      key: tag.id,
      label: tag.name,
      slug: tag.slug,
      icon: iconMap.PROMOTION,
    })
  })

  tags.LABEL?.forEach(tag => {
    items.push({
      key: tag.id,
      label: tag.name,
      slug: tag.slug,
      icon: iconMap.LABEL,
    })
  })

  return items
})

/* APPLY FILTER (FIXED: MOBILE SAFE, NO REMOUNT) */
const applyTag = (slug) => {
  // ✅ close drawer immediately to avoid overlay blocking UI
  open.value = false

  // ✅ prevent redundant route updates
  if (route.query.tag === slug) return

  router.replace({
    path: route.path,
    query: { ...route.query, tag: slug }
  })
}
</script>

<template>
  <!-- ================= DESKTOP ================= -->
  <div class="hidden md:block bg-white border-b">
    <div class="max-w-7xl mx-auto px-6 py-3">
      <div class="flex justify-center gap-8">
        <button
          v-for="item in menu"
          :key="item.key"
          @click="applyTag(item.slug)"
          class="flex items-center gap-2 text-sm font-medium
                 text-neutral-700 hover:text-orange-600"
        >
          <component :is="item.icon" class="w-4 h-4" />
          {{ item.label }}
        </button>
      </div>
    </div>
  </div>

  <!-- ================= MOBILE SEARCH ================= -->
  <div class="md:hidden bg-white border-b">
    <div class="flex items-center gap-3 px-4 py-3">
      <button @click="open = true" class="p-2">☰</button>

      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search products…"
        class="flex-1 rounded-full border px-4 py-2 text-sm"
      />
    </div>
  </div>

  <!-- ================= MOBILE DRAWER ================= -->
  <div v-if="open" class="fixed inset-0 z-50 md:hidden">
    <div
      class="absolute inset-0 bg-black/40"
      @click="open = false"
    ></div>

    <aside class="absolute left-0 top-0 h-full w-[80%] bg-white shadow">
      <div class="flex justify-between p-4 border-b">
        <span class="font-semibold">Deals</span>
        <button @click="open = false">✕</button>
      </div>

      <nav>
        <button
          v-for="item in menu"
          :key="item.key"
          @click="applyTag(item.slug)"
          class="flex items-center gap-3 px-4 py-3 text-sm
                 hover:bg-gray-100 w-full text-left"
        >
          <component
            :is="item.icon"
            class="w-5 h-5 text-orange-500"
          />
          {{ item.label }}
        </button>
      </nav>
    </aside>
  </div>
</template>
