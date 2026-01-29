import { ref } from "vue"
import { useCart } from "@/services/CartService"

const token = ref(localStorage.getItem("access_token"))
const user = ref(
  JSON.parse(localStorage.getItem("user") || "null")
)

// login
const login = (data) => {
  localStorage.setItem("access_token", data.access_token)
  localStorage.setItem("user", JSON.stringify(data.user))

  token.value = data.access_token
  user.value = data.user

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
