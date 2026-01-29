import api from "./api";

/* ========= CUSTOMER ========= */
export const getOrders = () => {
  return api.get("/orders");
};

export const getOrderById = (id) => {
  return api.get(`/orders/${id}`);
};

export const cancelOrder = (orderId) => {
  return api.patch(`/orders/${orderId}/cancel`);
};
/* ========= ADMIN ========= */
export const getAdminOrders = () => {
  console.log("🔥 getAdminOrders CALLED → /admin/orders");
  return api.get("/admin/orders");   // ✅ FIXED
};

export const patchAdminOrderStatus = (id, status) => {
  return api.patch(`/admin/orders/${id}/status`, {
    status,
  });
};

export const createOrder = (order_payload) => {
    return api.post("/orders", order_payload)
}