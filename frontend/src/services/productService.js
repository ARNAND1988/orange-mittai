import api from "./api";

// productService.js
export const getProducts = async () => {
  const res = await api.get("/products"); // or public products endpoint
  console.log(res)
  return res;
};


export const getProductById = (id) => {
  return api.get(`/products/${id}`);
};

export const createProduct = (data) => {
  return api.post(`/products`, data);
};


// Admin API Calls
export const fetchProductsForAdmin = async () => {
    const res =  await api.get(`/admin/products`)
    return res.data ?? res
}

export const softDelete = (id) => {
  return api.patch(`/admin/products/${id}/soft-delete`)
}

export const restore = (id) => {
  return api.patch(`/admin/products/${id}/restore`)
}

export const updateProduct = ( id, name, price, stock ) => {
  console.log({ id, name, price, stock })
  return api.patch(`/admin/products/${id}`, { name: name, price: price, stock:stock, });
};
