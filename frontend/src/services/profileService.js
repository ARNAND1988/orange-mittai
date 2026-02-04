import api from "./api";

export const getProfile = () => api.get("/profile");

export const getAddresses = () => api.get("/profile/addresses");

export const createAddress = (payload) =>
  api.post("/profile/addresses", payload);

export const updateAddress = (id, payload) =>
  api.put(`/profile/addresses/${id}`, payload);

export const updateProfile = (payload) =>
  api.put("/profile", payload);

export const deleteAddress = (id) =>
  api.delete(`/profile/addresses/${id}`);
