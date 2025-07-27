import React, { useEffect, useState } from "react";
import axios from "axios";
import "../css/Home.css";

function Home() {
  const [sweets, setSweets] = useState([]);
  const [filters, setFilters] = useState({
    name: "",
    category: "",
    minPrice: "",
    maxPrice: "",
    sortBy: "",
  });
  const [newSweet, setNewSweet] = useState({ id: "", name: "", category: "", price: "", quantity: "" });
  const [token, setToken] = useState(localStorage.getItem("token"));

  useEffect(() => {
    fetchSweets();
  }, []);

  const fetchSweets = async () => {
    const res = await axios.get("http://localhost:8000/sweets");
    setSweets(res.data);
  };

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleNewSweetChange = (e) => {
    setNewSweet({ ...newSweet, [e.target.name]: e.target.value });
  };

  const addSweet = async () => {
    try {
      await axios.post("http://localhost:8000/sweets/add", newSweet);
      fetchSweets();
    } catch (err) {
      alert("Failed to add sweet");
    }
  };

  const purchaseSweet = async (id, quantity) => {
    if (!token) return alert("Login required to purchase");

    try {
      await axios.post(
        `http://localhost:8000/sweets/${id}/purchase`,
        { quantity },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      fetchSweets();
      alert("Purchased and added to cart!");
    } catch (err) {
      alert("Purchase failed");
    }
  };

  const restockSweet = async (id, quantity) => {
    try {
      await axios.post(`http://localhost:8000/sweets/${id}/restock`, { quantity });
      fetchSweets();
    } catch (err) {
      alert("Restock failed");
    }
  };

  const deleteSweet = async (id) => {
    await axios.delete(`http://localhost:8000/sweets/${id}/delete`);
    fetchSweets();
  };

  return (
    <div className="home-container">
      <h1>🍭 Sweet Shop Management</h1>

      {/* Filter Section */}
      <div className="card">
        <h3>🔍 Search & Sort Sweets</h3>
        <input name="name" placeholder="Name" onChange={handleFilterChange} />
        <input name="category" placeholder="Category" onChange={handleFilterChange} />
        <input name="minPrice" placeholder="Min Price" onChange={handleFilterChange} />
        <input name="maxPrice" placeholder="Max Price" onChange={handleFilterChange} />
        <select name="sortBy" onChange={handleFilterChange}>
          <option>Sort By...</option>
          <option value="price_asc">Price ↑</option>
          <option value="price_desc">Price ↓</option>
        </select>
        <button className="apply-btn">Apply</button>
      </div>

      {/* Add Sweet Section */}
      <div className="card">
        <h3>➕ Add New Sweet</h3>
        <input name="id" placeholder="ID" onChange={handleNewSweetChange} />
        <input name="name" placeholder="Name" onChange={handleNewSweetChange} />
        <input name="category" placeholder="Category" onChange={handleNewSweetChange} />
        <input name="price" placeholder="Price" type="number" onChange={handleNewSweetChange} />
        <input name="quantity" placeholder="Quantity" type="number" onChange={handleNewSweetChange} />
        <button className="add-btn" onClick={addSweet}>Add Sweet</button>
      </div>

      {/* Table Section */}
      <table className="sweets-table">
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Category</th><th>Price</th><th>Quantity</th><th>Purchase</th><th>Restock</th><th>Delete</th>
          </tr>
        </thead>
        <tbody>
          {sweets.map((sweet) => (
            <tr key={sweet._id}>
              <td>{sweet.id}</td>
              <td>{sweet.name}</td>
              <td>{sweet.category}</td>
              <td>{sweet.price.toFixed(2)}</td>
              <td>{sweet.quantity}</td>
              <td>
                <input type="number" min="1" placeholder="Qty" id={`buy-${sweet._id}`} />
                <button
                  disabled={sweet.quantity === 0}
                  onClick={() =>
                    purchaseSweet(sweet._id, document.getElementById(`buy-${sweet._id}`).value)
                  }
                >
                  Buy
                </button>
              </td>
              <td>
                <input type="number" min="1" placeholder="Qty" id={`restock-${sweet._id}`} />
                <button
                  onClick={() =>
                    restockSweet(sweet._id, document.getElementById(`restock-${sweet._id}`).value)
                  }
                >
                  +
                </button>
              </td>
              <td>
                <button className="delete-btn" onClick={() => deleteSweet(sweet._id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Home;
