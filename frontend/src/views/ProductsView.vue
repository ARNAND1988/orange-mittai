<template>
  <div class="bg-orange-50 py-8">
    <div class="max-w-7xl mx-auto space-y-14 px-4">

<!-- 🔥 PROMOTION SECTIONS -->
<section
  v-for="promo in promotionSections"
  :key="promo.slug"
  class="space-y-6"
>
  <!-- PROMO HEADER -->
  <div class="flex items-center justify-between">
    <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
      <span class="text-orange-500">🔥</span>
      {{ promo.name }}
    </h2>

    <span
      class="hidden sm:inline text-sm font-medium text-orange-600"
    >
      View all →
    </span>
  </div>

  <!-- PRODUCTS -->
  <div
    class="flex gap-4 overflow-x-auto scroll-smooth
           no-scrollbar pb-2 snap-x snap-mandatory"
  >
    <ProductCard
      v-for="product in promo.products"
      :key="`${promo.slug}-${product.id}`"
      :product="product"
      :subcategory="getSubcategory(product)"
      :labels="getLabels(product)"
      @add-to-cart="handleAddToCart"
      class="flex-shrink-0 snap-start"
    />
  </div>
</section>



      <section
        v-for="category in categorySections"
        :key="category.slug"
        class="space-y-6"
      >
        <!-- CATEGORY HEADER -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div
              class="w-16 h-16 rounded-lg bg-orange-100
                     flex items-center justify-center
                     text-orange-700 font-semibold"
            >
              {{ category.name[0] }}
            </div>

            <div>
              <h2 class="text-xl font-semibold text-gray-800">
                {{ category.name }}
              </h2>
              <p class="text-sm text-gray-500">
                {{ category.products.length }} products
              </p>
            </div>
          </div>

          <span
            class="hidden sm:inline text-sm font-medium
                   text-orange-600"
          >
            View all →
          </span>
        </div>

        <!-- HORIZONTAL PRODUCT LIST -->
        <div
          class="flex gap-4 overflow-x-auto scroll-smooth
                 no-scrollbar pb-2 snap-x snap-mandatory"
        >
          <ProductCard
            v-for="product in category.products"
            :key="product.id"
            :product="product"
            :subcategory="getSubcategory(product)"
            :labels="getLabels(product)"
            @add-to-cart="handleAddToCart"
            class="w-56 flex-shrink-0 snap-start"
          />
        </div>

      </section>

    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from "vue";
import { getProducts } from "@/services/productService";
import ProductCard from "../components/ProductCard.vue";
import { useCart } from "@/services/CartService";

const { addToCart } = useCart();

const products = ref([]);
const handleAddToCart = (product) => {
  addToCart(product);
};

onMounted(async () => {
  try {
    const res = await getProducts();
    console.log("Products API response:", res);
    products.value = Array.isArray(res) ? res : res?.data ?? [];
  } catch (e) {
    products.value = [];
  }
});


const categorySections = computed(() => {
  const map = {};

  products.value
    .filter(p => p.is_active && p.stock > 0)
    .forEach(product => {
      const categoryTag = product.tags.find(
        t => t.type === "CATEGORY" && t.is_active
      );

      if (!categoryTag) return;

      if (!map[categoryTag.slug]) {
        map[categoryTag.slug] = {
          name: categoryTag.name,
          slug: categoryTag.slug,
          products: [],
        };
      }

      map[categoryTag.slug].products.push(product);
    });

  return Object.values(map);
});

const promotionSections = computed(() => {
  const map = {};

  products.value
    ?.filter(p => p.is_active && p.stock > 0)
    .forEach(product => {
      product.tags
        .filter(tag => tag.type === "PROMOTION")
        .forEach(tag => {
          if (!map[tag.slug]) {
            map[tag.slug] = {
              name: tag.name,
              slug: tag.slug,
              products: [],
            };
          }

          map[tag.slug].products.push(product);
        });
    });

  return Object.values(map);
});


const getSubcategory = (product) => {
  const sub = product.tags.find(t => t.type === "SUBCATEGORY");
  return sub ? sub.name : null;
};

const getLabels = (product) => {
  return product.tags.filter(
    t => t.type === "LABEL" || t.type === "PROMOTION"
  );
};


const availableProducts = computed(() => {
  if (!Array.isArray(products.value)) return [];
  return products.value.filter(p => p.is_active && p.stock > 0);
});



</script>
