import { ref } from "vue"
import { useCart } from "@/services/CartService"

// ✅ SAFE READ helpers
const safeParse = (value) => {
  if (!value || value === "undefined") return null
  try {
    return JSON.parse(value)
  } catch {
    return null
  }
}

const token = ref(localStorage.getItem("access_token"))
const user = ref(
  safeParse(localStorage.getItem("user"))
)

// login
const login = (data) => {
  console.log("AuthService.login received:", data)

  // 🔒 Guard (prevents poisoning localStorage again)
  if (!data?.access_token) {
    throw new Error("Login failed: access_token missing")
  }

  localStorage.setItem("access_token", data.access_token)

  if (data.user) {
    localStorage.setItem("user", JSON.stringify(data.user))
  } else {
    localStorage.removeItem("user")
  }

  token.value = data.access_token
  user.value = data.user ?? null

  const { clearCart } = useCart()
  clearCart()
}

// logout
const logout = () => {
  const { clearCart } = useCart()
  clearCart()

  localStorage.removeItem("access_token")
  localStorage.removeItem("user")

  token.value = null
  user.value = null
}

export function useAuth() {
  return {
    token,
    user,
    login,
    logout,
  }
}
