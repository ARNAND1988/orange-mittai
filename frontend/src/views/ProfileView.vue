<script setup>
import { useAuth } from "@/services/AuthService";

const { user } = useAuth();
</script>

<template>
  <div class="max-w-4xl mx-auto py-8">
    <h1 class="text-2xl font-semibold text-gray-800 mb-6">
      My Profile
    </h1>

    <div class="bg-white border border-orange-200 rounded-xl shadow-sm p-6 space-y-4">
      <div>
        <p class="text-sm text-gray-500">Email</p>
        <p class="text-gray-800 font-medium">
          {{ user?.email }}
        </p>
      </div>

      <div>
        <p class="text-sm text-gray-500">Account Type</p>
        <p class="text-gray-800 font-medium">
          {{ user?.is_admin ? "Admin" : "Customer" }}
        </p>
      </div>

      <button
        class="mt-4 text-sm text-orange-600 font-medium hover:underline"
      >
        Edit profile (coming soon)
      </button>
    </div>
  </div>
</template>
