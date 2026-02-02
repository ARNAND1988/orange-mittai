<script setup>
import { ref, computed, watch, onMounted } from "vue"
import { useRouter, useRoute, RouterLink } from "vue-router"
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { useAuth } from "@/services/AuthService"
import { useCart } from "@/services/CartService"
import { useTagMenu } from "@/services/TagMenuService"

/* ================= SERVICES ================= */
const auth = useAuth()
const router = useRouter()
const route = useRoute()
const { totalItems, showAddedToast, lastAddedProduct } = useCart()

const { groupedTags, fetchTags } = useTagMenu()
onMounted(fetchTags)

/* ================= UI STATE ================= */
const mobileMenuOpen = ref(false)
const mobileAccountOpen = ref(false)
const mobileAdminOpen = ref(false)
const desktopDropdownOpen = ref(false)
const showLogoutMessage = ref(false)

/* ================= AUTH ================= */
const isLoggedIn = computed(() => !!auth.token.value)
const isAdmin = computed(() => auth.user.value?.is_admin === true)

const userFullName = computed(() =>
  auth.user.value
    ? `${auth.user.value.first_name} ${auth.user.value.last_name}`
    : ""
)

/* ================= ACTIONS ================= */
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
  mobileAccountOpen.value = false
  mobileAdminOpen.value = false
}

const toggleMobileAccount = () => {
  if (!isLoggedIn.value) {
    router.push("/auth")
    return
  }
  mobileAccountOpen.value = !mobileAccountOpen.value
  mobileMenuOpen.value = false
  mobileAdminOpen.value = false
}

const toggleMobileAdmin = () => {
  mobileAdminOpen.value = !mobileAdminOpen.value
  mobileMenuOpen.value = false
  mobileAccountOpen.value = false
}

const toggleDesktopDropdown = () => {
  desktopDropdownOpen.value = !desktopDropdownOpen.value
}

const handleLogout = async () => {
  await auth.logout()
  showLogoutMessage.value = true
  setTimeout(() => (showLogoutMessage.value = false), 2500)
  router.push("/")
}

/* AUTO CLOSE */
watch(() => route.fullPath, () => {
  mobileMenuOpen.value = false
  mobileAccountOpen.value = false
  mobileAdminOpen.value = false
  desktopDropdownOpen.value = false
})
</script>

<template>
  <!-- ================= MOBILE LOGO ================= -->
  <nav class="md:hidden fixed top-0 inset-x-0 z-50 bg-white border-b">
    <div class="flex justify-center py-3">
      <RouterLink to="/">
        <img src="../assets/images/logo.png" class="h-8" />
      </RouterLink>
    </div>
  </nav>

  <!-- ================= MOBILE SEARCH + HAMBURGER ================= -->
  <nav class="md:hidden fixed top-[52px] inset-x-0 z-40 bg-white border-b">
    <div class="relative flex items-center gap-3 px-4 py-3">
      <button
        @click="toggleMobileMenu"
        class="menu-item text-gray-800"
        aria-label="Open menu"
      >
        <font-awesome-icon icon="bars" size="lg" />
      </button>

      <input
        type="text"
        placeholder="Search sweets, snacks…"
        class="flex-1 rounded-full border px-4 py-2 text-sm
               focus:ring-2 focus:ring-orange-400"
      />

      <div
        v-if="mobileMenuOpen"
        class="absolute left-4 top-full mt-2 w-64
               bg-white border rounded-xl shadow-lg z-50 overflow-hidden"
      >
        <template v-if="groupedTags.PROMOTION?.length">
          <div class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase">
            🔥 Promotions
          </div>
          <RouterLink
            v-for="tag in groupedTags.PROMOTION"
            :key="tag.id"
            :to="`/tag/${tag.slug}`"
            class="menu-item block"
          >
            {{ tag.name }}
          </RouterLink>
        </template>

        <template v-if="groupedTags.LABEL?.length">
          <div class="border-t my-1"></div>
          <div class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase">
            🏷 Labels
          </div>
          <RouterLink
            v-for="tag in groupedTags.LABEL"
            :key="tag.id"
            :to="`/tag/${tag.slug}`"
            class="menu-item block"
          >
            {{ tag.name }}
          </RouterLink>
        </template>
      </div>
    </div>
  </nav>

  <!-- ================= DESKTOP NAVBAR ================= -->
  <nav class="hidden md:block bg-white border-b shadow-sm">
    <div class="max-w-7xl mx-auto flex justify-between items-center px-6 py-4">
      <RouterLink to="/">
        <img src="../assets/images/logo.png" class="h-20" />
      </RouterLink>

      <div v-if="isAdmin" class="flex gap-6">
        <RouterLink to="/admin/products" class="menu-item text-base font-semibold">
          Admin Products
        </RouterLink>
        <RouterLink to="/admin/orders" class="menu-item text-base font-semibold">
          Admin Orders
        </RouterLink>
      </div>

      <div class="flex items-center gap-4 relative">
        <div v-if="isLoggedIn" class="relative">
          <button @click="toggleDesktopDropdown" class="menu-item">
            <font-awesome-icon icon="user" size="lg" />
          </button>

          <div
            v-if="desktopDropdownOpen"
            class="absolute right-0 mt-2 w-44
                   bg-white border rounded-xl shadow-lg z-50 overflow-hidden"
          >
            <div class="px-4 py-2 font-semibold border-b">
              {{ userFullName }}
            </div>

            <RouterLink to="/profile" class="menu-item block">
              Profile
            </RouterLink>

            <RouterLink
              v-if="!isAdmin"
              to="/orders"
              class="menu-item block"
            >
              Orders
            </RouterLink>

            <button
              @click="handleLogout"
              class="menu-item block text-red-600 w-full text-left"
            >
              Logout
            </button>
          </div>
        </div>

        <RouterLink v-else to="/auth" class="menu-item">
          <font-awesome-icon icon="user" size="lg" />
        </RouterLink>
      </div>
    </div>
  </nav>

  <!-- ================= MOBILE BOTTOM NAV ================= -->
  <nav
    class="md:hidden fixed bottom-2 left-2 right-2 z-50
           bg-white/80 backdrop-blur-lg
           border rounded-2xl shadow-lg"
  >
    <div class="relative flex justify-around py-2 text-xs text-gray-800">

      <RouterLink to="/" class="menu-item flex flex-col items-center">
        <font-awesome-icon icon="house" size="lg" />
        Home
      </RouterLink>

      <button
        v-if="isAdmin"
        @click="toggleMobileAdmin"
        class="menu-item flex flex-col items-center"
      >
        <font-awesome-icon icon="user-shield" size="lg" />
        Admin
      </button>

      <button
        @click="toggleMobileAccount"
        class="menu-item flex flex-col items-center"
      >
        <font-awesome-icon icon="user" size="lg" />
        {{ isLoggedIn ? "Account" : "Login" }}
      </button>

      <div
        v-if="mobileAdminOpen"
        class="absolute bottom-14 left-1/2 -translate-x-1/2
               w-44 bg-white border rounded-xl shadow-lg z-50 overflow-hidden"
      >
        <RouterLink to="/admin/products" class="menu-item block">
          Admin Products
        </RouterLink>
        <RouterLink to="/admin/orders" class="menu-item block">
          Admin Orders
        </RouterLink>
      </div>

      <div
        v-if="mobileAccountOpen && isLoggedIn"
        class="absolute right-4 bottom-14 w-44
               bg-white border rounded-xl shadow-lg z-50 overflow-hidden"
      >
        <div class="px-4 py-2 font-semibold border-b">
          {{ userFullName }}
        </div>

        <RouterLink to="/profile" class="menu-item block">
          Profile
        </RouterLink>

        <RouterLink
          v-if="!isAdmin"
          to="/orders"
          class="menu-item block"
        >
          Orders
        </RouterLink>

        <button
          @click="handleLogout"
          class="menu-item block text-red-600 w-full text-left"
        >
          Logout
        </button>
      </div>
    </div>
  </nav>

  <!-- ================= TOASTS ================= -->
  <div
    v-if="showAddedToast"
    class="fixed top-24 left-1/2 -translate-x-1/2 z-[60]
           bg-green-100 text-green-800 px-4 py-2 rounded-xl text-sm"
  >
    ✅ {{ lastAddedProduct }} added to cart
  </div>

  <div
    v-if="showLogoutMessage"
    class="fixed top-24 left-1/2 -translate-x-1/2 z-[60]
           bg-green-100 text-green-800 px-4 py-2 rounded-xl text-sm"
  >
    You’ve logged out successfully 👋
  </div>
</template>
