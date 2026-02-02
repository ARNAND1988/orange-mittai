import { createRouter, createWebHistory } from 'vue-router'

// Page views (NOT components)
import HomeView from '@/views/HomeView.vue'
import AuthView from '@/views/AuthView.vue'
import OrdersView from "@/views/OrdersView.vue";
import ProfileView from "@/views/ProfileView.vue";
import CartView from "@/views/CartView.vue";
import CheckoutView from "@/views/CheckoutView.vue"
import OrderDetailsView from "@/views/OrderDetailsView.vue"

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
{
  path: "/auth",
  name: "Auth",
  component: AuthView,
},

  { path: "/orders", name: "Orders", component: OrdersView },
  { path: "/profile", name: "Profile", component: ProfileView },
  { path: "/cart", name: "Cart", component: CartView },
  {
    path: "/checkout",
    component: CheckoutView,
  },
  {
    path: "/orders",
    component: OrdersView,
  },
  {
    path: "/admin/orders",
    component: () => import("@/views/AdminOrdersView.vue"),
  },
  {
    path: "/admin/products",
    component: () => import("@/views/AdminProductsView.vue"),
  },


{
  path: "/orders/:orderId",
  component: OrderDetailsView,
},
{
  path: "/admin/products/add",
  component: () => import("@/views/AdminProductAddEdit.vue")
}
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
