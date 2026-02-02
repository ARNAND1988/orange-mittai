<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useCart } from "@/services/CartService";
import { createOrder } from "@/services/orderService";
import { getAddresses, createAddress } from "@/services/profileService";

/* =====================
   STATE
===================== */

const router = useRouter();
const { clearCart } = useCart();

const cartItems = ref(
  JSON.parse(localStorage.getItem("cart") || "[]")
);

const addresses = ref([]);
const selectedAddressId = ref(null);

const showNewAddress = ref(false);
const addressError = ref("");
const loading = ref(false);

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
});

/* =====================
   LIFECYCLE
===================== */

onMounted(async () => {
  addresses.value = await getAddresses();

  // auto-select default address
  const defaultAddr = addresses.value.find(a => a.is_default);
  if (defaultAddr) {
    selectedAddressId.value = defaultAddr.id;
  }
});

/* =====================
   COMPUTED
===================== */

const cartTotal = computed(() =>
  cartItems.value.reduce(
    (sum, i) => sum + i.price * i.quantity,
    0
  )
);

const formatPrice = (value) =>
  Number(value).toFixed(2);

/* =====================
   ADDRESS
===================== */

const validateNewAddress = () => {
  addressError.value = "";

  const required = [
    "label",
    "name",
    "phone",
    "house_number",
    "line1",
    "city",
    "state",
    "postal_code",
    "country",
  ];

  for (const field of required) {
    if (!newAddress.value[field]?.trim()) {
      addressError.value = "Please fill all required address fields.";
      return false;
    }
  }
  return true;
};

const saveNewAddress = async () => {
  if (!validateNewAddress()) return;

  const created = await createAddress(newAddress.value);
  addresses.value = await getAddresses();

  selectedAddressId.value = created.id;
  showNewAddress.value = false;
};

/* =====================
   ORDER
===================== */

const placeOrder = async () => {
  if (!selectedAddressId.value) {
    alert("Please select or add a delivery address");
    return;
  }

  loading.value = true;

  const payload = {
    items: cartItems.value.map(i => ({
      product_id: i.productId ?? i.id,
      quantity: Number(i.quantity),
    })),
    address_id: selectedAddressId.value,
    payment_method: "COD",
  };

  await createOrder(payload);

  clearCart();
  router.push("/orders");

  loading.value = false;
};
</script>

<template>
  <div class="max-w-4xl mx-auto p-6 space-y-8">

    <h1 class="text-2xl font-semibold">Checkout</h1>

    <!-- EMPTY CART -->
    <div
      v-if="cartItems.length === 0"
      class="p-6 text-center text-gray-500 bg-white rounded-lg"
    >
      Your cart is empty
    </div>

    <div v-else class="space-y-6">

      <!-- ================= ADDRESSES ================= -->
      <div class="bg-white p-6 rounded-xl border border-orange-200">
        <h2 class="text-lg font-semibold mb-4">
          Delivery Address
        </h2>

        <div v-if="addresses.length">
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
        </div>

        <button
          class="mt-2 text-orange-600 text-sm hover:underline"
          @click="showNewAddress = !showNewAddress"
        >
          {{ showNewAddress ? "Cancel" : "+ Add new address" }}
        </button>

        <!-- ================= ADD NEW ADDRESS ================= -->
        <div v-if="showNewAddress" class="mt-4 border-t pt-4">
          <h3 class="font-medium mb-3">New Address</h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input v-model="newAddress.label" placeholder="Label" class="border rounded-lg px-3 py-2" />
            <input v-model="newAddress.name" placeholder="Full Name" class="border rounded-lg px-3 py-2" />
            <input v-model="newAddress.phone" placeholder="Phone" class="border rounded-lg px-3 py-2" />
            <input v-model="newAddress.house_number" placeholder="House Number" class="border rounded-lg px-3 py-2" />
            <input v-model="newAddress.line1" placeholder="Street" class="border rounded-lg px-3 py-2" />
            <input v-model="newAddress.line2" placeholder="Address Line 2 (optional)" class="border rounded-lg px-3 py-2" />
            <input v-model="newAddress.city" placeholder="City" class="border rounded-lg px-3 py-2" />
            <input v-model="newAddress.state" placeholder="State" class="border rounded-lg px-3 py-2" />
            <input v-model="newAddress.postal_code" placeholder="Postal Code" class="border rounded-lg px-3 py-2" />
            <input v-model="newAddress.country" placeholder="Country" class="border rounded-lg px-3 py-2" />
          </div>

          <p v-if="addressError" class="text-red-600 text-sm mt-2">
            {{ addressError }}
          </p>

          <button
            @click="saveNewAddress"
            class="mt-4 bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700"
          >
            Save Address
          </button>
        </div>
      </div>

      <!-- ================= CART SUMMARY ================= -->
      <div class="bg-white p-6 rounded-xl border border-orange-200">
        <h2 class="text-lg font-semibold mb-4">Order Summary</h2>

        <div
          v-for="item in cartItems"
          :key="item.productId"
          class="flex justify-between border-b pb-2 mb-2"
        >
          <span>{{ item.name }} × {{ item.quantity }}</span>
          <span>€{{ formatPrice(item.price * item.quantity) }}</span>
        </div>

        <div class="flex justify-between text-lg font-semibold mt-4">
          <span>Total</span>
          <span>€{{ formatPrice(cartTotal) }}</span>
        </div>
      </div>

      <!-- ================= PLACE ORDER ================= -->
      <button
        @click="placeOrder"
        :disabled="loading"
        class="w-full bg-orange-500 hover:bg-orange-600
               text-white py-3 rounded-lg transition"
      >
        {{ loading ? "Placing Order..." : "Place Order" }}
      </button>

    </div>
  </div>
</template>

<style scoped>
/* Tailwind only */
</style>
