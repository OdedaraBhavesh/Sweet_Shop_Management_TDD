import React, { useState } from "react";

export default function SweetRow({ sweet, refreshSweetList }) {
  const [qty, setQty] = useState(1);

  const handleBuy = async () => {
  const response = await fetch('http://localhost:8000/cart', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...sweet, quantity: 1 }) // add 1 qty to cart
  });

  if (response.ok) {
    await fetchSweets();     // Refresh sweets quantity
    await fetchCart();       // Refresh cart
  }
};

  const handleRestock = async () => {
    await fetch(`http://localhost:8000/sweets/${sweet._id}/restock`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quantity: qty }),
    });
    refreshSweetList();
  };

  const handleDelete = async () => {
    await fetch(`http://localhost:8000/sweets/${sweet._id}`, {
      method: "DELETE",
    });
    refreshSweetList();
  };

  return (
    <tr>
      <td>{sweet.name}</td>
      <td>{sweet.category}</td>
      <td>₹{sweet.price}</td>
      <td>{sweet.quantity}</td>
      <td>
        <input
          type="number"
          min="1"
          value={qty}
          onChange={(e) => setQty(parseInt(e.target.value))}
          style={{ width: "50px" }}
        />
      </td>
      <td>
        <button disabled={sweet.quantity === 0} onClick={handleBuy}>Buy</button>

        <button onClick={handleRestock}>+</button>
        <button onClick={handleDelete}>Delete</button>
      </td>
    </tr>
  );
}
