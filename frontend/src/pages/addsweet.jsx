import React, { useState } from "react";
import { addSweet } from "../api/sweets";

const AddSweet = () => {
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");

  const handleSubmit = async () => {
    await addSweet({ name, price });
    alert("Sweet added successfully");
    window.location.href = "/admin";
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4">➕ Add Sweet</h2>
      <input
        type="text"
        placeholder="Sweet Name"
        className="border p-2 mb-2 w-full"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="number"
        placeholder="Price"
        className="border p-2 mb-2 w-full"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
      />
      <button className="bg-green-500 text-white px-4 py-2" onClick={handleSubmit}>
        Add
      </button>
    </div>
  );
};

export default AddSweet;
