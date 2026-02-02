import api from "./api";

/* =======================
   PUBLIC APIs
======================= */

export const getProducts = async () => {
  const res = await api.get("/products");
  console.log("data ", res)
  return res;
};

export const getProductById = (id) => {
  return api.get(`/products/${id}`);
};

/* =======================
   ADMIN APIs
======================= */

// Fetch products for admin
export const fetchProductsForAdmin = async () => {
  const res = await api.get(`/admin/products`);
  console.log("products", res)
  return res;
};

export const createProductWithImage = async ({
  name,
  description,
  price,
  stock,
  is_active = true,
  tag_ids = [],
  imageFile = null
}) => {
  const formData = new FormData()

  // ✅ Only append image if selected
  if (imageFile instanceof File) {
    formData.append("image", imageFile)
  }

  formData.append("name", name)
  formData.append("description", description)
  formData.append("price", price)
  formData.append("stock", stock)
  formData.append("is_active", is_active)

  if (tag_ids.length > 0) {
    formData.append("tag_ids", tag_ids.join(","))
  }

  const res = await api.post(
    "/admin/products/add",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    }
  )

  return res.data
}


// Update product (basic fields)
export const updateProduct = (id, name, price, stock) => {
  return api.patch(`/admin/products/${id}`, {
    name,
    price,
    stock
  });
};

// Soft delete product
export const softDelete = (id) => {
  return api.patch(`/admin/products/${id}/soft-delete`);
};

// Restore product
export const restore = (id) => {
  return api.patch(`/admin/products/${id}/restore`);
};

// productService.js
export const updateProductImage = (id, imageUrl) => {
  console.log(imageUrl)
  return api.patch(`/admin/products/${id}/image`, {
    image: imageUrl
  })
}
