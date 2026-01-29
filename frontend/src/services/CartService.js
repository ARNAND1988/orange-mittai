import { ref, computed } from "vue";

const cartItems = ref([]);
const showAddedToast = ref(false);
const lastAddedProduct = ref(""); // ✅ THIS WAS MISSING

// Restore cart on refresh
const storedCart = localStorage.getItem("cart");
if (storedCart) {
  cartItems.value = JSON.parse(storedCart);
}

const saveCart = () => {
  localStorage.setItem("cart", JSON.stringify(cartItems.value));
};

const clearCart = () => {
  cartItems.value = []
  localStorage.removeItem("cart")
}

// Add to cart
const addToCart = (product, qty = 1) => {
  const existing = cartItems.value.find(
    (item) => item.id === product.id
  );

  if (existing) {
    existing.quantity += qty;
  } else {
    cartItems.value.push({
      ...product,
      quantity: qty,
    });
  }

  lastAddedProduct.value = product.name;
  showAddedToast.value = true;

  setTimeout(() => {
    showAddedToast.value = false;
  }, 2000);

  saveCart();
};


// Update quantity
const updateQuantity = (id, qty) => {
  const item = cartItems.value.find((i) => i.id === id);
  if (!item) return;

  item.quantity = qty;

  if (item.quantity <= 0) {
    removeFromCart(id);
  }

  saveCart();
};

// Remove item
const removeFromCart = (id) => {
  cartItems.value = cartItems.value.filter(
    (item) => item.id !== id
  );
  saveCart();
};

// Totals
const totalItems = computed(() =>
  cartItems.value.reduce((sum, i) => sum + i.quantity, 0)
);

const totalPrice = computed(() =>
  cartItems.value.reduce(
    (sum, i) => sum + i.price * i.quantity,
    0
  )
);

export function useCart() {
  return {
    cartItems,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    totalItems,
    totalPrice,
    showAddedToast,
    lastAddedProduct,
  };
}
