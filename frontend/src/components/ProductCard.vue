<template>
  <div
    class="bg-white/90 backdrop-blur-[1px]
           rounded-xl shadow-sm hover:shadow-md
           transition w-52"
  >
    <!-- 🖼️ IMAGE -->
    <div
      class="h-28 flex items-center justify-center
             bg-gradient-to-b from-gray-50/80 to-transparent
             rounded-t-xl"
    >
      <img
        :src="product.image"
        class="max-h-24 max-w-[85%] object-contain"
        alt=""
      />
    </div>

    <!-- 📦 INFO -->
    <div class="px-3 py-2 space-y-1">
      <h3 class="text-sm font-medium text-gray-800 line-clamp-2">
        {{ product.name }}
      </h3>

      <p class="text-[11px] text-gray-400 uppercase tracking-wide">
        {{ subcategory }}
      </p>

      <!-- 🔖 BADGES (BELOW DESCRIPTION) -->
      <div
        v-if="visibleBadges.length"
        class="flex flex-wrap gap-1 pt-1"
      >
        <span
          v-for="tag in visibleBadges"
          :key="tag.id"
          :class="badgeClass(tag.type)"
          class="text-[10px] font-medium px-2 py-0.5 rounded-md"
        >
          {{ tag.name }}
        </span>

        <span
          v-if="extraBadgeCount"
          class="text-[10px] px-2 py-0.5 rounded-md
                 bg-gray-100/80 text-gray-600"
        >
          +{{ extraBadgeCount }}
        </span>
      </div>

<!-- 💰 PRICE + CART -->
<div class="flex items-center justify-between pt-2">
  <span class="font-semibold text-orange-600 text-sm">
    ₹{{ product.price }}
  </span>

  <button
    v-if="!isOutOfStock"
    @click="addToCart"
    class="text-[11px] px-3 py-1 rounded-md
           bg-orange-500/90 text-white
           hover:bg-orange-600
           transition"
  >
    Add
  </button>

  <span
    v-else
    class="text-[11px] text-red-500 font-medium"
  >
    Out
  </span>
</div>

    </div>
  </div>
</template>
<script setup>
import { computed } from "vue";

const props = defineProps({
  product: Object,
  subcategory: String,
  labels: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["add-to-cart"]);

const addToCart = () => {
  emit("add-to-cart", props.product);
};


const isOutOfStock = computed(() => props.product.stock <= 0);

const sortedLabels = computed(() =>
  [...props.labels].sort((a, b) =>
    a.type === "PROMOTION" ? -1 : 1
  )
);

const visibleBadges = computed(() =>
  sortedLabels.value.slice(0, 2)
);

const extraBadgeCount = computed(() =>
  Math.max(sortedLabels.value.length - 2, 0)
);

const badgeClass = (type) => {
  switch (type) {
    case "PROMOTION":
      return "bg-red-50/80 text-red-700";
    case "LABEL":
      return "bg-blue-50/80 text-blue-700";
    default:
      return "bg-gray-50/80 text-gray-700";
  }
};


</script>
