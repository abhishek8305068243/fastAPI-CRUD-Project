import React, { useEffect, useState, useMemo } from "react";
import axios from "axios";   // Axios HTTP client (API calls ke liye)
import "./App.css";
import TaglineSection from "./TaglineSection";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

// Custom toast helper functions
import {
  toastSuccess,
  toastError,
  toastInfo,
  toastWarning,
} from "./utils/toast";


// Axios instance create kiya with base backend URL
// Isse baar-baar full URL likhne ki zarurat nahi padti
const api = axios.create({
  baseURL: "https://fastapi-crud-project-2-2sm8.onrender.com",
});

function App() {

  // ======================
  // State Declarations
  // ======================

  // Products list jo backend se aayegi
  const [products, setProducts] = useState([]);

  // Form state (Add / Edit product ke liye)
  const [form, setForm] = useState({
    id: "",
    name: "",
    description: "",
    price: "",
    quantity: "",
    category: "",

  });

  // Edit mode ke liye product ID
  const [editId, setEditId] = useState(null);

  // Success message state
  const [message, setMessage] = useState("");

  // Error message state
  const [error, setError] = useState("");

  // Loading state (API calls ke time disable buttons)
  const [loading, setLoading] = useState(false);

  // Search filter text
  const [filter, setFilter] = useState("");

  // Sorting field (id, name, price, quantity)
  const [sortField, setSortField] = useState("id");

  // Sorting direction (asc / desc)
  const [sortDirection, setSortDirection] = useState("asc");




  // Auto-dismiss messages after 5 seconds - msg change hota hai to 5 sec bad usko empty kr deta hai
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        setMessage("");
      }, 5000);

      // Cleanup
      return () => clearTimeout(timer);
    }
  }, [message]);



  // Initial load: fetch products
  useEffect(() => {
    fetchProducts();
  }, []);




  // useEffect - error auto dismiss - error msg ko 5 sec bad clear krta hai
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError("");
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);



  // Fetch all products from backend
  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await api.get("/products");
      setProducts(res.data);
      setError("");
    } catch (err) {
      setError("Failed to fetch products");
    }
    setLoading(false);

  };


  // sorting handler
  const handleSort = (field) => {
    // Agar same field pe click hua to direction toggle
    if (sortField !== field) {
      setSortField(field);
      setSortDirection("asc");
      return;
    }
    setSortDirection(sortDirection === "asc" ? "desc" : "asc");
  };

  // Filter + Sort combined (useMemo for performance)
  const filteredProducts = useMemo(() => {
    let filtered = products;

    // Apply filter
    const q = filter.trim().toLowerCase();
    if (q) {
      filtered = products.filter(
        (p) =>
          String(p.id).includes(q) ||
          p.name?.toLowerCase().includes(q) ||
          p.description?.toLowerCase().includes(q)
      );
    }

    // Apply sorting
    return filtered.sort((a, b) => {
      let aVal = a[sortField];
      let bVal = b[sortField];

      // Number fields
      if (
        sortField === "id" ||
        sortField === "price" ||
        sortField === "quantity" ||
        sortField ===  "category"
      ) {
        aVal = Number(aVal);
        bVal = Number(bVal);
      } else {
        // Handle string fields
        aVal = String(aVal).toLowerCase();
        bVal = String(bVal).toLowerCase();
      }

      if (aVal < bVal) return sortDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [products, filter, sortField, sortDirection]);

  // Handle form input
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };


  // ======================
  // Reset form after submit / cancel
  // ======================
  const resetForm = () => {
    setForm({ id: "", name: "", description: "", price: "", quantity: "", category: "" });
    setEditId(null);
  };


  // Create or update product**************************************************
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setError("");
    try {
      if (editId) {
        // update product
        const response = await api.put(`/products${editId}`, {
          ...form,
          id: Number(form.id),
          price: Number(form.price),
          quantity: Number(form.quantity),
          category: (form.category),
        });
        console.log("Update: ", response);
        toastSuccess("Product updated successfully");


        // UI me product update
        if (response.data) {
          setProducts((prev) =>
            prev.map((item) => {
              if (item.id === editId) {
                return response.data;
              }
              return item;
            })
          );
        }
      } else {
        // CREATE product
        const response = await api.post("/products", {
          ...form,
          id: Number(form.id),
          price: Number(form.price),
          quantity: Number(form.quantity),
          category: (form.category)
        });
        toastSuccess("Product created successfully");
        console.log("Response: ", response);

        if (response.data) {
          setProducts((prev) => [response.data, ...prev]);
        }
      }

      resetForm();
      //fetchProducts();
    } catch (err) {
      console.error("API ERROR:", err);
      toastError(err.response?.data.detail || "Operation failed");
    }
    setLoading(false);
  };

  // Edit Button handler**************************************************************
  const handleEdit = (product) => {
    setForm({
      id: product.id,
      name: product.name,
      description: product.description,
      price: product.price,
      quantity: product.quantity,
      category: product.category,
    });
    setEditId(product.id);
    setMessage("");
    setError("");
  };

  // Delete product************************************************************
  const handleDelete = async (id) => {
    const ok = window.confirm("Delete this product?");
    if (!ok) return;
    setLoading(true);
    setMessage("");
    setError("");
    try {
      await api.delete(`/products${id}`);
      toastSuccess("Product deleted successfully");
      // fetchProducts();

      setProducts((prev) => {
        return prev.filter((item) => {
          return item.id !== id;
        });
      });
    } catch (err) {
      setError("Delete failed");
    }
    setLoading(false);
  };


  //======================
  // Price formatting helper
  // ======================
  const currency = (n) =>
    typeof n === "number" ? n.toFixed(2) : Number(n || 0).toFixed(2);


  // ======================
  // JSX UI Rendering
  // ======================
  return (
    <div className="app-bg">
      <header className="topbar">
        <div className="brand">
          <span className="brand-badge">📦</span>
          <h1>Inventory Management System</h1>
        </div>
        <div className="top-actions">
          <button
            className="btn btn-light"
            onClick={fetchProducts}
            disabled={loading}
          >
            Refresh
          </button>
        </div>
      </header>


      <div className="container">
        <div className="stats">
          <div className="chip">Total: {products.length}</div>
          <div className="search">
            <input
              type="text"
              placeholder="Search by id, name or description..."
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            />
          </div>
        </div>

        <div className="content-grid">
          <div className="card form-card">
            <h2>{editId ? "Edit Product" : "Add Product"}</h2>
            <form onSubmit={handleSubmit} className="product-form">
              <input
                type="number"
                name="id"
                placeholder="ID"
                value={form.id}
                onChange={handleChange}
                required
                disabled={!!editId}
              />
              <input
                type="text"
                name="name"
                placeholder="Name"
                value={form.name}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="description"
                placeholder="Description"
                value={form.description}
                onChange={handleChange}
                required
              />
              <input
                type="number"
                name="price"
                placeholder="Price"
                value={form.price}
                onChange={handleChange}
                required
                step="0.01"
              />
              <input
                type="number"
                name="quantity"
                placeholder="Quantity"
                value={form.quantity}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="category"
                placeholder="category"
                value={form.category}
                onChange={handleChange}
                required
              />
              <div className="form-actions">
                <button className="btn" type="submit" disabled={loading}>
                  {editId ? "Update" : "Add"} {loading && "Please wait"}
                </button>
                {editId && (
                  <button
                    className="btn btn-secondary"
                    type="button"
                    onClick={() => {
                      resetForm();
                      setMessage("");
                      setError("");
                    }}
                  >
                    Cancel
                  </button>
                )}
              </div>
            </form>
            {message && <div className="success-msg">{message}</div>}
            {error && <div className="error-msg">{error}</div>}
          </div>

          <TaglineSection />

          <div className="card list-card">
            <h2>Products</h2>{(
            <div className="scroll-x">
              <table className="product-table">
                <thead>
                  <tr>
                    <th
                      className={`sortable ${sortField === "id" ? `sort-${sortDirection}` : ""
                        }`}
                      onClick={() => handleSort("id")}
                    >
                      ID
                    </th>
                    <th
                      className={`sortable ${sortField === "name" ? `sort-${sortDirection}` : ""
                        }`}
                      onClick={() => handleSort("name")}
                    >
                      Name
                    </th>
                    <th>Description</th>
                    <th
                      className={`sortable ${sortField === "price" ? `sort-${sortDirection}` : ""
                        }`}
                      onClick={() => handleSort("price")}
                    >
                      Price
                    </th>
                    <th
                      className={`sortable ${sortField === "quantity" ? `sort-${sortDirection}` : ""
                        }`}
                      onClick={() => handleSort("quantity")}
                    >
                      Quantity
                    </th>

                     <th
                      className={`sortable ${sortField === "category" ? `sort-${sortDirection}` : ""
                        }`}
                      onClick={() => handleSort("category")}
                    >
                      category
                    </th>

                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProducts.map((p) => (
                    <tr key={p.id}>
                      <td>{p.id}</td>
                      <td className="name-cell">{p.name}</td>
                      <td className="desc-cell" title={p.description}>
                        {p.description}
                      </td>
                      <td className="price-cell">${currency(p.price)}</td>
                      <td>
                        <span className="qty-badge">{p.quantity}</span>
                      </td>
                      <td className="category-cell">{p.category}</td>
                      <td>
                        <div className="row-actions">
                          <button
                            className="btn btn-edit"
                            onClick={() => handleEdit(p)}
                          >
                            Edit
                          </button>
                          <button
                            className="btn btn-delete"
                            onClick={() => handleDelete(p.id)}
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {filteredProducts.length === 0 && (
                    <tr>
                      <td colSpan={6} className="empty">
                        No products found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            )}
          </div>
        </div>
      </div>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        pauseOnHover
        draggable
      />
    </div>
  );
}

export default App;
