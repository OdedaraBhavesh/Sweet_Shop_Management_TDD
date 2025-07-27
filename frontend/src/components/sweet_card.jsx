// SweetCard.js
import React from 'react';
import axios from 'axios';

const SweetCard = ({ sweet, fetchSweets }) => {
  const token = localStorage.getItem("token");
const purchaseSweet = async (id) => {
  const token = localStorage.getItem("token");
  try {
    const res = await axios.post(
      `http://localhost:8000/sweets/${id}/purchase`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`  // ✅ Secure request
        }
      }
    );
    alert("Purchase Successful!");
    fetchSweets();  // Refresh sweets quantity
  } catch (err) {
    alert(err.response?.data?.detail || "Purchase failed");
  }
};
const handlePurchase = async (sweetId) => {
  const token = localStorage.getItem("token");
  
  const res = await fetch(`http://127.0.0.1:8000/sweets/${sweetId}/purchase`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    }
  });

  const data = await res.json();

  if (res.ok) {
    alert("Purchase successful!");
  } else {
    alert(data.detail || "Purchase failed");
  }
};

  return (
    <div className="card" style={{ border: "1px solid #ddd", padding: 10, margin: 10 }}>
      <h3>{sweet.name}</h3>
      <p>Category: {sweet.category}</p>
      <p>Price: ₹{sweet.price}</p>
      <p>Available: {sweet.quantity}</p>
      <button
        disabled={sweet.quantity === 0}
        onClick={handlePurchase}
        style={{ backgroundColor: sweet.quantity === 0 ? "#ccc" : "#4CAF50", color: "#fff", padding: "8px 16px", border: "none" }}
      >
        {sweet.quantity === 0 ? "Out of Stock" : "Purchase"}
      </button>
    </div>
  );
};

export default SweetCard;
