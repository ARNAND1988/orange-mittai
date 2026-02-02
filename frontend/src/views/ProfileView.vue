<script setup>
import { ref, onMounted } from "vue";
import {
  getProfile,
  getAddresses,
  createAddress,
  updateAddress,
  updateProfile,
  deleteAddress,
} from "@/services/profileService";

/* =====================
   STATE
===================== */

const profile = ref(null);
const addresses = ref([]);

const profileForm = ref({
  first_name: "",
  last_name: "",
  phone: "",
});

const showPasswordChange = ref(false);
const passwordForm = ref({
  current_password: "",
  new_password: "",
  confirm_password: "",
});

const addressForm = ref({
  label: "Home",
  name: "",
  phone: "",
  house_number: "",
  line1: "",
  line2: "", // optional
  city: "",
  state: "",
  postal_code: "",
  country: "",
  is_default: false,
});

const editingAddressId = ref(null);
const loading = ref(false);
const success = ref("");
const addressError = ref("");

/* =====================
   LIFECYCLE
===================== */

onMounted(async () => {
  profile.value = await getProfile();
  addresses.value = await getAddresses();

  profileForm.value.first_name = profile.value.first_name || "";
  profileForm.value.last_name = profile.value.last_name || "";
  profileForm.value.phone = profile.value.phone || "";
});

/* =====================
   PROFILE
===================== */

const saveProfile = async () => {
  // Password validation
  if (showPasswordChange.value) {
    if (
      !passwordForm.value.current_password ||
      !passwordForm.value.new_password
    ) {
      alert("Please fill all password fields");
      return;
    }

    if (
      passwordForm.value.new_password !==
      passwordForm.value.confirm_password
    ) {
      alert("New passwords do not match");
      return;
    }
  }

  const payload = {
    ...profileForm.value,
    ...(showPasswordChange.value
      ? {
          current_password: passwordForm.value.current_password,
          new_password: passwordForm.value.new_password,
        }
      : {}),
  };

  await updateProfile(payload);
  profile.value = await getProfile();

  showPasswordChange.value = false;
  passwordForm.value = {
    current_password: "",
    new_password: "",
    confirm_password: "",
  };

  success.value = "Profile updated successfully";
};

/* =====================
   ADDRESS VALIDATION
===================== */

const validateAddress = () => {
  addressError.value = "";

  const requiredFields = [
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

  for (const field of requiredFields) {
    if (!addressForm.value[field]?.trim()) {
      addressError.value = "Please fill all required address fields.";
      return false;
    }
  }

  return true;
};

/* =====================
   ADDRESS
===================== */

const editAddress = (addr) => {
  editingAddressId.value = addr.id;
  addressForm.value = { ...addr };
  addressError.value = "";
};

const resetAddressForm = () => {
  editingAddressId.value = null;
  addressForm.value = {
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
  };
  addressError.value = "";
};

const removeAddress = async (addr) => {
  const ok = confirm(
    `Delete ${addr.label} address?\nThis action cannot be undone.`
  );
  if (!ok) return;

  await deleteAddress(addr.id);
  addresses.value = await getAddresses();
  success.value = "Address deleted successfully";
};

const saveAddress = async () => {
  if (!validateAddress()) return;

  loading.value = true;

  if (editingAddressId.value) {
    await updateAddress(editingAddressId.value, addressForm.value);
  } else {
    await createAddress(addressForm.value);
  }

  addresses.value = await getAddresses();
  resetAddressForm();
  success.value = "Address saved successfully";
  loading.value = false;
};
</script>

<template>
  <div class="max-w-4xl mx-auto py-8 space-y-8">

    <!-- ================= PROFILE ================= -->
    <div class="bg-white border border-orange-200 rounded-xl p-6">
      <h2 class="text-xl font-semibold mb-4">My Profile</h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">
            First Name
          </label>
          <input v-model="profileForm.first_name" class="border rounded-lg px-3 py-2 w-full" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">
            Last Name
          </label>
          <input v-model="profileForm.last_name" class="border rounded-lg px-3 py-2 w-full" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">
            Phone Number
          </label>
          <input v-model="profileForm.phone" class="border rounded-lg px-3 py-2 w-full" />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-600 mb-1">
            Password
          </label>
          <div class="flex items-center gap-3">
            <input
              value="********"
              disabled
              class="border rounded-lg px-3 py-2 w-full bg-gray-100"
            />
            <button
              type="button"
              class="text-sm text-orange-600 hover:underline"
              @click="showPasswordChange = !showPasswordChange"
            >
              {{ showPasswordChange ? "Cancel" : "Change" }}
            </button>
          </div>
        </div>
      </div>

      <!-- Change Password -->
      <div v-if="showPasswordChange" class="mt-6 border-t pt-4">
        <h3 class="text-lg font-medium mb-3">Change Password</h3>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            v-model="passwordForm.current_password"
            type="password"
            placeholder="Current Password"
            class="border rounded-lg px-3 py-2"
          />
          <input
            v-model="passwordForm.new_password"
            type="password"
            placeholder="New Password"
            class="border rounded-lg px-3 py-2"
          />
          <input
            v-model="passwordForm.confirm_password"
            type="password"
            placeholder="Confirm New Password"
            class="border rounded-lg px-3 py-2"
          />
        </div>
      </div>

      <button
        @click="saveProfile"
        class="mt-6 bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700"
      >
        Save Profile
      </button>
    </div>

    <!-- ================= SAVED ADDRESSES ================= -->
    <div class="bg-white border border-orange-200 rounded-xl p-6">
      <h2 class="text-xl font-semibold mb-4">Saved Addresses</h2>

      <div v-for="addr in addresses" :key="addr.id" class="border rounded-lg p-4 mb-3">
        <div class="flex justify-between items-start">
          <div>
            <p class="font-medium">
              {{ addr.label }} {{ addr.is_default ? "(Default)" : "" }}
            </p>
            <p>{{ addr.name }} · {{ addr.phone }}</p>
            <p>
              {{ addr.house_number }},
              {{ addr.line1 }},
              {{ addr.city }} – {{ addr.postal_code }}
            </p>
          </div>

          <div class="flex gap-3">
            <button
              v-if="editingAddressId !== addr.id"
              class="text-orange-600 text-sm hover:underline"
              @click="editAddress(addr)"
            >
              Edit
            </button>

            <button
              v-if="editingAddressId === addr.id"
              class="text-gray-600 text-sm hover:underline"
              @click="resetAddressForm"
            >
              Cancel
            </button>

            <button
              v-if="editingAddressId !== addr.id"
              class="text-red-600 text-sm hover:underline"
              :disabled="addresses.length === 1"
              @click="removeAddress(addr)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>

      <p v-if="addresses.length === 1" class="text-xs text-gray-500 mt-2">
        You must keep at least one address.
      </p>
    </div>

    <!-- ================= ADD / EDIT ADDRESS ================= -->
    <div class="bg-white border border-orange-200 rounded-xl p-6">
      <h2 class="text-xl font-semibold mb-4">
        {{ editingAddressId ? "Edit Address" : "Add Address" }}
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input v-model="addressForm.label" placeholder="Label (Home / Office)" class="border rounded-lg px-3 py-2" />
        <input v-model="addressForm.name" placeholder="Full Name" class="border rounded-lg px-3 py-2" />
        <input v-model="addressForm.phone" placeholder="Phone" class="border rounded-lg px-3 py-2" />
        <input v-model="addressForm.house_number" placeholder="House Number" class="border rounded-lg px-3 py-2" />
        <input v-model="addressForm.line1" placeholder="Street" class="border rounded-lg px-3 py-2" />
        <input v-model="addressForm.line2" placeholder="Address Line 2 (optional)" class="border rounded-lg px-3 py-2" />
        <input v-model="addressForm.city" placeholder="City" class="border rounded-lg px-3 py-2" />
        <input v-model="addressForm.state" placeholder="State" class="border rounded-lg px-3 py-2" />
        <input v-model="addressForm.postal_code" placeholder="Postal Code" class="border rounded-lg px-3 py-2" />
        <input v-model="addressForm.country" placeholder="Country" class="border rounded-lg px-3 py-2" />
      </div>

      <p v-if="addressError" class="text-red-600 text-sm mt-3">
        {{ addressError }}
      </p>

      <label class="flex items-center mt-4 text-sm">
        <input type="checkbox" v-model="addressForm.is_default" class="mr-2" />
        Set as default
      </label>

      <div class="flex gap-3 mt-4">
        <button
          @click="saveAddress"
          :disabled="loading"
          class="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700"
        >
          {{ loading ? "Saving..." : "Save Address" }}
        </button>

        <button
          v-if="editingAddressId"
          @click="resetAddressForm"
          class="border px-4 py-2 rounded-lg"
        >
          Cancel
        </button>
      </div>

      <p v-if="success" class="text-green-600 text-sm mt-2">
        {{ success }}
      </p>
    </div>

  </div>
</template>

<style scoped>
/* Tailwind only */
</style>
