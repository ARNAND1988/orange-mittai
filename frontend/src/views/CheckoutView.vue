<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useCart } from "@/services/CartService"
import { createOrder } from "@/services/orderService"
import { getAddresses, createAddress } from "@/services/profileService"
import { useAuth } from "@/services/AuthService"
const { isAuthenticated } = useAuth()

/* =====================
   ROUTER / AUTH
===================== */
const router = useRouter()
const route = useRoute()
console.log(route.query.guest)
const isGuest = computed(() => route.query.guest === "true")

/* =====================
   CART
===================== */
const { clearCart } = useCart()
const cartItems = ref(
  JSON.parse(localStorage.getItem("cart") || "[]")
)

/* =====================
   ADDRESS (LOGGED IN)
===================== */
const addresses = ref([])
const selectedAddressId = ref(null)
const showNewAddress = ref(false)
const addressError = ref("")

const newAddress = ref({
  label: "Home",
  name: "",
  phone: "",
  house_number: "",
  line1: "",
  line2: "",
  city: "",
  state: "",
  postal_code: "",
  country: "",
  is_default: false,
})

/* =====================
   GUEST INFO
===================== */
const guestInfo = ref({
  name: "",
  email: "",
  phone: "",
})

/* =====================
   UI STATE
===================== */
const loading = ref(false)

/* =====================
   LIFECYCLE
===================== */
onMounted(async () => {
  console.log("Guest",!isGuest.value, isAuthenticated )
  if (!isGuest.value && isAuthenticated) {
    addresses.value = await getAddresses()
    const defaultAddr = addresses.value.find(a => a.is_default)
    if (defaultAddr) selectedAddressId.value = defaultAddr.id
  }
})

/* =====================
   COMPUTED
===================== */
const cartTotal = computed(() =>
  cartItems.value.reduce(
    (sum, i) => sum + i.price * i.quantity,
    0
  )
)

const formatPrice = (v) => Number(v).toFixed(2)

/* =====================
   VALIDATION
===================== */
const validateGuest = () => {
  if (!guestInfo.value.name || !guestInfo.value.email || !guestInfo.value.phone) {
    alert("Please fill guest name, email, and phone")
    return false
  }
  return validateAddress()
}

const validateAddress = () => {
  const required = [
    "name",
    "phone",
    "house_number",
    "line1",
    "city",
    "state",
    "postal_code",
    "country",
  ]
  for (const f of required) {
    if (!newAddress.value[f]?.trim()) {
      addressError.value = "Please fill all required address fields."
      return false
    }
  }
  addressError.value = ""
  return true
}

/* =====================
   ADDRESS SAVE (USER)
===================== */
const saveNewAddress = async () => {
  if (!validateAddress()) return

  const created = await createAddress(newAddress.value)
  addresses.value = await getAddresses()
  selectedAddressId.value = created.id
  showNewAddress.value = false
}

/* =====================
   PLACE ORDER
===================== */
const placeOrder = async () => {
  if (cartItems.value.length === 0) return

  if (isGuest.value) {
    if (!validateGuest()) return
  } else {
    if (!selectedAddressId.value) {
      alert("Please select or add an address")
      return
    }
  }

  loading.value = true

  const payload = {
    items: cartItems.value.map(i => ({
      product_id: i.productId ?? i.id,
      quantity: Number(i.quantity),
    })),
    payment_method: "COD",
    guest: isGuest.value,
    guest_info: isGuest.value ? guestInfo.value : undefined,
    address: isGuest.value ? newAddress.value : undefined,
    address_id: !isGuest.value ? selectedAddressId.value : undefined,
  }

  try {
    await createOrder(payload)
    clearCart()
    router.push("/orders")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8">

    <h1 class="text-2xl font-semibold">Checkout</h1>

    <!-- EMPTY -->
    <div
      v-if="cartItems.length === 0"
      class="p-6 text-center text-gray-500 bg-white rounded-lg"
    >
      Your cart is empty
    </div>

    <div v-else class="space-y-6">

      <!-- ================= GUEST DETAILS ================= -->
      <div
        v-if="isGuest"
        class="bg-white p-6 rounded-xl border border-orange-200"
      >
        <h2 class="text-lg font-semibold mb-4">Guest Details</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input v-model="guestInfo.name" placeholder="Full Name" class="border rounded-lg px-3 py-2" />
          <input v-model="guestInfo.email" placeholder="Email" class="border rounded-lg px-3 py-2" />
          <input v-model="guestInfo.phone" placeholder="Phone" class="border rounded-lg px-3 py-2" />
        </div>
      </div>

      <!-- ================= ADDRESS ================= -->
      <div class="bg-white p-6 rounded-xl border border-orange-200">
        <h2 class="text-lg font-semibold mb-4">Delivery Address</h2>

        <!-- LOGGED IN ADDRESS LIST -->
        <div v-if="!isGuest && addresses.length">
          <label
            v-for="addr in addresses"
            :key="addr.id"
            class="block border rounded-lg p-4 mb-3 cursor-pointer"
            :class="{
              'border-orange-500 bg-orange-50':
                selectedAddressId === addr.id
            }"
          >
            <input
              type="radio"
              class="mr-2"
              :value="addr.id"
              v-model="selectedAddressId"
            />
            <span class="font-medium">
              {{ addr.label }} {{ addr.is_default ? "(Default)" : "" }}
            </span>
            <p class="text-sm text-gray-600">
              {{ addr.name }} · {{ addr.phone }}
            </p>
            <p class="text-sm">
              {{ addr.house_number }},
              {{ addr.line1 }},
              {{ addr.city }} – {{ addr.postal_code }}
            </p>
          </label>

          <button
            class="mt-2 text-orange-600 text-sm hover:underline"
            @click="showNewAddress = !showNewAddress"
          >
            {{ showNewAddress ? "Cancel" : "+ Add new address" }}
          </button>
        </div>

        <!-- ADDRESS FORM (GUEST OR NEW) -->
        <div v-if="isGuest || showNewAddress" class="mt-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input v-model="newAddress.name" placeholder="Full Name" class="border rounded px-3 py-2" />
            <input v-model="newAddress.phone" placeholder="Phone" class="border rounded px-3 py-2" />
            <input v-model="newAddress.house_number" placeholder="House Number" class="border rounded px-3 py-2" />
            <input v-model="newAddress.line1" placeholder="Street" class="border rounded px-3 py-2" />
            <input v-model="newAddress.line2" placeholder="Address Line 2 (optional)" class="border rounded px-3 py-2" />
            <input v-model="newAddress.city" placeholder="City" class="border rounded px-3 py-2" />
            <input v-model="newAddress.state" placeholder="State" class="border rounded px-3 py-2" />
            <input v-model="newAddress.postal_code" placeholder="Postal Code" class="border rounded px-3 py-2" />
            <input v-model="newAddress.country" placeholder="Country" class="border rounded px-3 py-2" />
          </div>

          <p v-if="addressError" class="text-red-600 text-sm mt-2">
            {{ addressError }}
          </p>

          <button
            v-if="!isGuest"
            @click="saveNewAddress"
            class="mt-4 bg-orange-600 text-white px-4 py-2 rounded-lg"
          >
            Save Address
          </button>
        </div>
      </div>

      <!-- ================= SUMMARY ================= -->
      <div class="bg-white p-6 rounded-xl border border-orange-200">
        <h2 class="text-lg font-semibold mb-4">Order Summary</h2>

        <div
          v-for="item in cartItems"
          :key="item.id"
          class="flex justify-between mb-2"
        >
          <span>{{ item.name }} × {{ item.quantity }}</span>
          <span>€{{ formatPrice(item.price * item.quantity) }}</span>
        </div>

        <div class="flex justify-between font-semibold text-lg mt-4">
          <span>Total</span>
          <span>€{{ formatPrice(cartTotal) }}</span>
        </div>
      </div>

      <!-- ================= PLACE ORDER ================= -->
      <button
        @click="placeOrder"
        :disabled="loading"
        class="w-full bg-orange-500 hover:bg-orange-600
               text-white py-3 rounded-lg"
      >
        {{ loading ? "Placing Order..." : "Place Order" }}
      </button>

    </div>
  </div>
</template>

<style scoped>
/* Tailwind only */
</style>
