<script setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { useAuth } from "@/services/AuthService"
import { useCart } from "@/services/CartService"

const auth = useAuth()
const router = useRouter()
const { totalItems, showAddedToast, lastAddedProduct } = useCart()

const dropdownOpen = ref(false)
const showLogoutMessage = ref(false)

const isLoggedIn = computed(() => !!auth.token.value)
const isAdmin = computed(() => auth.user.value?.is_admin === true)
const userFullName = computed(() =>
  auth.user.value
    ? `${auth.user.value.first_name} ${auth.user.value.last_name}`
    : ""
)

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

// --------------------
// CART HANDLER (✅ FIX)
// --------------------
const handleAddToCart = (product) => {
  addToCart(product);
};

const handleLogout = () => {
  auth.logout()
  dropdownOpen.value = false

  showLogoutMessage.value = true
  setTimeout(() => (showLogoutMessage.value = false), 2500)

  router.push("/")
}
</script>


<template>
  <nav class="w-full z-50 bg-white border-b border-gray-200 shadow-sm relative">
    <div class="max-w-7xl mx-auto flex items-center justify-between px-4 py-3">

      <!-- Brand -->
      <router-link to="/" class="flex items-center">
        <img
          src="../assets/images/menu_logo.png"
          class="h-12 w-auto max-w-[220px] object-contain"
          alt="Orange Mittai"
        />
      </router-link>

      <!-- Icons -->
      <div class="flex items-center gap-6 text-gray-800 relative">

        <!-- Admin links -->
        <div
          v-if="isAdmin"
          class="flex items-center gap-4 ml-6 text-gray-800"
        >
          <RouterLink
            to="/admin/products"
            class="text-sm font-medium hover:text-orange-500 transition"
          >
            Admin Products
          </RouterLink>

          <RouterLink
            to="/admin/orders"
            class="text-sm font-medium hover:text-orange-500 transition"
          >
            Admin Orders
          </RouterLink>
        </div>

        <!-- Logged OUT -->
        <RouterLink
          v-if="!isLoggedIn"
          to="/auth"
          class="hover:text-orange-500 transition"
        >
          <font-awesome-icon icon="user" size="lg" />
        </RouterLink>

        <!-- Logged IN -->
        <div v-else class="relative flex items-center gap-2">
          <span class="text-sm text-gray-600 hidden sm:block">
            Welcome {{ userFullName }}
          </span>

          <button
            @click="toggleDropdown"
            class="hover:text-orange-500 transition focus:outline-none"
          >
            <font-awesome-icon icon="user" size="lg" />
          </button>

          <!-- Dropdown -->
          <div
            v-if="dropdownOpen"
            class="absolute right-0 mt-2 w-40 bg-white
                   text-gray-800 rounded-lg shadow-lg z-50 border"
          >
            <!-- Orders: CUSTOMER ONLY -->
            <RouterLink
              v-if="!isAdmin"
              to="/orders"
              class="block px-4 py-2 hover:bg-gray-100"
              @click="dropdownOpen = false"
            >
              Orders
            </RouterLink>

            <RouterLink
              to="/profile"
              class="block px-4 py-2 hover:bg-gray-100"
              @click="dropdownOpen = false"
            >
              Profile
            </RouterLink>

            <button
              @click="handleLogout"
              class="w-full text-left px-4 py-2 hover:bg-gray-100"
            >
              Logout
            </button>
          </div>
        </div>

        <!-- Cart (CUSTOMER ONLY) -->
        <RouterLink
          v-if="!isAdmin"
          to="/cart"
          class="relative hover:text-orange-500 transition"
        >
          <font-awesome-icon icon="cart-shopping" size="lg" />

          <!-- Cart badge -->
          <span
            v-if="totalItems > 0"
            class="absolute -top-2 -right-2
                   bg-orange-500 text-white
                   text-[10px] font-bold
                   rounded-full px-1.5 py-0.5
                   min-w-[18px] text-center"
          >
            {{ totalItems }}
          </span>
        </RouterLink>

      </div>
    </div>
  </nav>

  <!-- Logout confirmation -->
  <div
    v-if="showLogoutMessage"
    class="fixed top-20 left-1/2 -translate-x-1/2 z-[60]
           bg-green-100 text-green-800
           px-4 py-2 rounded-lg shadow-md
           text-sm font-medium"
  >
    You’ve logged out successfully 👋
  </div>

  <!-- ADD-TO-CART TOAST -->
  <div
    v-if="showAddedToast"
    class="fixed top-20 left-1/2 -translate-x-1/2 z-[60]
           bg-green-100 text-green-800
           px-4 py-2 rounded-lg shadow-md
           text-sm font-medium"
  >
    ✅ {{ lastAddedProduct }} added to cart
  </div>
</template>

