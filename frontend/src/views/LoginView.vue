<template>
  <div class="min-h-full flex items-center justify-center px-4">

    <!-- Login Card -->
    <div class="w-full max-w-sm bg-white p-6 border border-orange-200 rounded-xl shadow-lg">
      <form>

        <!-- Heading -->
        <h5 class="text-2xl font-semibold text-gray-800 mb-6 text-center">
          Welcome back 🍊
        </h5>

        <!-- Email -->
        <div class="mb-4">
          <label for="email" class="block mb-2 text-sm font-medium text-gray-700">
            Email
          </label>
          <input
            type="email"
            id="email"
            class="w-full px-3 py-2.5 text-sm rounded-lg
                   border border-gray-300
                   focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400"
            placeholder="example@orangemittai.com"
            required
          />
        </div>

        <!-- Password -->
        <div class="mb-5">
          <label for="password" class="block mb-2 text-sm font-medium text-gray-700">
            Password
          </label>
          <input
            type="password"
            id="password"
            class="w-full px-3 py-2.5 text-sm rounded-lg
                   border border-gray-300
                   focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400"
            placeholder="••••••••"
            required
          />
        </div>

        <!-- Remember + Forgot -->
        <div class="flex items-center justify-between mb-6">
          <label class="flex items-center text-sm text-gray-600">
            <input
              type="checkbox"
              class="w-4 h-4 mr-2 rounded border-gray-300
                     text-orange-600 focus:ring-orange-500"
            />
            Remember me
          </label>

          <a href="#" class="text-sm font-medium text-orange-600 hover:underline">
            Forgot password?
          </a>
        </div>

        <!-- Submit -->
        <button
          type="submit"
          class="w-full text-white bg-orange-600 hover:bg-orange-700
                 font-medium rounded-lg text-sm px-4 py-2.5
                 focus:outline-none focus:ring-4 focus:ring-orange-300"
        >
          Sign in
        </button>

        <!-- Footer -->
        <p class="text-sm text-center text-gray-600 mt-4">
          New to Orange Mittai?
          <a href="#" class="text-orange-600 font-medium hover:underline">
            Create an account
          </a>
        </p>

      </form>
    </div>
  </div>
</template>

<script setup>
</script>