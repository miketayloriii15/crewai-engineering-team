let cart = {};

document.addEventListener("DOMContentLoaded", () => {
  loadProducts();
  document
    .getElementById("search-button")
    .addEventListener("click", loadProducts);
  document
    .getElementById("category-filter")
    .addEventListener("change", loadProducts);
  document
    .getElementById("checkout-button")
    .addEventListener("click", mockCheckout);
});

function loadProducts() {
  const q = document.getElementById("search-input").value;
  const category = document.getElementById("category-filter").value;
  const url = new URL(window.location.origin + "/products");
  if (q) url.searchParams.append("q", q);
  if (category) url.searchParams.append("category", category);

  fetch(url)
    .then((r) => r.json())
    .then(renderProducts)
    .catch((err) => console.error("Error fetching products:", err));
}

function renderProducts(products) {
  const grid = document.getElementById("product-grid");
  grid.innerHTML = "";
  products.forEach((p) => {
    const col = document.createElement("div");
    col.className = "col-md-3";
    col.innerHTML = `
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${p.name}</h5>
          <p class="card-text">Category: ${p.category}</p>
          <p class="card-price">$${p.price.toFixed(2)}</p>
          <button class="btn btn-primary" onclick="addToCart(${
            p.id
          })">Add to Cart</button>
        </div>
      </div>`;
    grid.appendChild(col);
  });
}

function addToCart(id) {
  fetch("/cart", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: id, quantity: 1 }),
  }).then(() => {
    cart[id] = (cart[id] || 0) + 1;
    updateCartUI();
  });
}

function updateCartUI() {
  const div = document.getElementById("cart-content");
  div.innerHTML = "";
  const ids = Object.keys(cart);
  if (!ids.length) {
    div.innerHTML = "<p>Your cart is empty.</p>";
    return;
  }
  const url = new URL(window.location.origin + "/products");
  url.searchParams.append("ids", ids.join(","));
  fetch(url)
    .then((r) => r.json())
    .then((products) => {
      let subtotal = 0;
      products.forEach((p) => {
        const qty = cart[p.id];
        const price = qty * p.price;
        subtotal += price;
        const item = document.createElement("div");
        item.className =
          "d-flex justify-content-between align-items-center mb-2";
        item.innerHTML = `
          <div>${p.name} — ${qty} × $${p.price.toFixed(2)} = $${price.toFixed(
          2
        )}</div>
          <button class="btn btn-sm btn-danger" onclick="removeFromCart(${
            p.id
          })">Remove</button>`;
        div.appendChild(item);
      });
      const total = document.createElement("div");
      total.className = "mt-3";
      total.innerHTML = `<strong>Subtotal: $${subtotal.toFixed(2)}</strong>`;
      div.appendChild(total);
    });
}

function removeFromCart(id) {
  delete cart[id];
  updateCartUI();
}

function mockCheckout() {
  const items = Object.entries(cart).map(([pid, qty]) => ({
    product_id: parseInt(pid, 10),
    quantity: qty,
  }));
  if (!items.length) return alert("Cart is empty.");
  fetch("/checkout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items }),
  })
    .then((r) => r.json())
    .then((d) => {
      alert(d.message);
      cart = {};
      updateCartUI();
    });
}
