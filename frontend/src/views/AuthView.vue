<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/api";
import { useAuth } from "@/services/AuthService";

const mode = ref("login"); // 'login' | 'register'

const first_name = ref("");
const last_name = ref("");

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const error = ref("");
const submitting = ref(false);

const router = useRouter();
const { login } = useAuth();

const resetForm = () => {
  first_name.value = "";
  last_name.value = "";
  email.value = "";
  password.value = "";
  confirmPassword.value = "";
};

const switchMode = () => {
  mode.value = mode.value === "login" ? "register" : "login";
  error.value = "";
  resetForm();
};

const handleSubmit = async () => {
  error.value = "";
  submitting.value = true;

  try {
    if (mode.value === "login") {
      console.log("=== LOGIN START ===");
      console.log("Email:", email.value);

      const formData = new URLSearchParams();
      formData.append("username", email.value);
      formData.append("password", password.value);

      console.log("FormData payload:", formData.toString());

      const response = await api.post(
        "/auth/login",
        formData,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );

      console.log("RAW AXIOS RESPONSE:", response);
      console.log("RESPONSE TYPE:", typeof response);

      // Try both possibilities explicitly
      console.log("response.data:", response?.data);
      console.log("response.access_token:", response?.access_token);

      // Decide what data actually is
      const payload = response?.data ?? response;

      console.log("FINAL PAYLOAD PASSED TO login():", payload);
      console.log("payload.access_token:", payload?.access_token);
      console.log("payload.user:", payload?.user);

      login(payload);
      router.push("/");
    } else {
      if (password.value !== confirmPassword.value) {
        error.value = "Passwords do not match";
        submitting.value = false;
        return;
      }

      await api.post("/auth/register", {
        first_name: first_name.value,
        last_name: last_name.value,
        email: email.value,
        password: password.value,
      });

      mode.value = "login";
      resetForm();
    }
  } catch (err) {
    console.error("LOGIN ERROR:", err);
    console.error("ERROR RESPONSE:", err?.response);
    console.error("ERROR RESPONSE DATA:", err?.response?.data);

    error.value =
      err?.response?.data?.detail ||
      err?.message ||
      "Something went wrong";
  } finally {
    submitting.value = false;
    console.log("=== LOGIN END ===");
  }
};
</script>


<template>
  <div class="min-h-full flex items-center justify-center px-4 ">
    <div class="w-full max-w-sm bg-white p-6 border border-orange-200 rounded-xl shadow-lg">

      <h5 class="text-2xl font-semibold text-gray-800 mb-2 text-center">
        {{ mode === "login" ? "Welcome back 🍊" : "Create your account" }}
      </h5>

      <p class="text-sm text-gray-600 text-center mb-6">
        {{ mode === "login"
          ? "Sign in to continue"
          : "Join Orange Mittai today"
        }}
      </p>

      <!-- Error -->
      <p v-if="error" class="mb-4 text-sm text-red-600 text-center">
        {{ error }}
      </p>

      <form @submit.prevent="handleSubmit">

        <!-- First Name -->
        <div v-if="mode === 'register'" class="mb-4">
          <label class="block mb-2 text-sm font-medium text-gray-700">
            First Name
          </label>
          <input
            v-model="first_name"
            type="text"
            required
            class="w-full px-3 py-2.5 text-sm rounded-lg
                   border border-gray-300
                   focus:ring-2 focus:ring-orange-400"
          />
        </div>

        <!-- Last Name -->
        <div v-if="mode === 'register'" class="mb-4">
          <label class="block mb-2 text-sm font-medium text-gray-700">
            Last Name
          </label>
          <input
            v-model="last_name"
            type="text"
            required
            class="w-full px-3 py-2.5 text-sm rounded-lg
                   border border-gray-300
                   focus:ring-2 focus:ring-orange-400"
          />
        </div>

        <!-- Email -->
        <div class="mb-4">
          <label class="block mb-2 text-sm font-medium text-gray-700">
            Email
          </label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full px-3 py-2.5 text-sm rounded-lg
                   border border-gray-300
                   focus:ring-2 focus:ring-orange-400"
          />
        </div>

        <!-- Password -->
        <div class="mb-4">
          <label class="block mb-2 text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full px-3 py-2.5 text-sm rounded-lg
                   border border-gray-300
                   focus:ring-2 focus:ring-orange-400"
          />
        </div>

        <!-- Confirm password (register only) -->
        <div v-if="mode === 'register'" class="mb-5">
          <label class="block mb-2 text-sm font-medium text-gray-700">
            Confirm Password
          </label>
          <input
            v-model="confirmPassword"
            type="password"
            required
            class="w-full px-3 py-2.5 text-sm rounded-lg
                   border border-gray-300
                   focus:ring-2 focus:ring-orange-400"
          />
        </div>

        <!-- Submit -->
        <button
          type="submit"
          :disabled="submitting"
          class="w-full text-white bg-orange-600 hover:bg-orange-700
                 font-medium rounded-lg text-sm px-4 py-2.5
                 focus:ring-4 focus:ring-orange-300
                 disabled:opacity-50"
        >
          {{ submitting
            ? "Please wait…"
            : mode === "login"
              ? "Sign in"
              : "Create account"
          }}
        </button>
      </form>

      <!-- Switch -->
      <p class="text-sm text-center text-gray-600 mt-4">
        {{ mode === "login"
          ? "New to Orange Mittai?"
          : "Already have an account?"
        }}
        <button
          type="button"
          class="text-orange-600 font-medium hover:underline ml-1"
          @click="switchMode"
        >
          {{ mode === "login" ? "Create one" : "Sign in" }}
        </button>
      </p>

    </div>
  </div>
</template>
