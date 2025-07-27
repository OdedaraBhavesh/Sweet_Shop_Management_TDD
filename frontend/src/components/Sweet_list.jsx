import React, { useEffect, useState } from 'react';
import SweetRow from './sweetrow';

const SweetList = () => {
  const [sweets, setSweets] = useState([]);
  const [filters, setFilters] = useState({ name: '', category: '', minPrice: '', maxPrice: '' });
  const [sortKey, setSortKey] = useState('');
  const [newSweet, setNewSweet] = useState({ name: '', category: '', price: '', quantity: '' });

  const fetchSweets = async () => {
    try {
      const res = await fetch('http://localhost:8000/sweets');
      const data = await res.json();
      setSweets(data);
    } catch (err) {
      console.error('Failed to fetch sweets:', err);
    }
  };

  useEffect(() => {
    fetchSweets();
  }, []);

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleNewSweetChange = (e) => {
    setNewSweet({ ...newSweet, [e.target.name]: e.target.value });
  };

  const applyFilters = () => {
    let filtered = [...sweets];
    if (filters.name) filtered = filtered.filter(s => s.name.toLowerCase().includes(filters.name.toLowerCase()));
    if (filters.category) filtered = filtered.filter(s => s.category.toLowerCase().includes(filters.category.toLowerCase()));
    if (filters.minPrice) filtered = filtered.filter(s => s.price >= parseFloat(filters.minPrice));
    if (filters.maxPrice) filtered = filtered.filter(s => s.price <= parseFloat(filters.maxPrice));
    if (sortKey) filtered.sort((a, b) => (a[sortKey] > b[sortKey] ? 1 : -1));
    setSweets(filtered);
  };

  const handleAddSweet = async () => {
    const response = await fetch('http://localhost:8000/sweets', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: newSweet.name,
        category: newSweet.category,
        price: parseFloat(newSweet.price),
        quantity: parseInt(newSweet.quantity)
      })
    });
    if (response.ok) {
      fetchSweets();
      setNewSweet({ name: '', category: '', price: '', quantity: '' });
    }
  };

  return (
    <div className="sweet-section">
      <div className="filter-card">
        <h2>🛠️ Search & Sort Sweets</h2>
        <div className="filter-grid">
          <input name="name" placeholder="Name" onChange={handleFilterChange} />
          <input name="category" placeholder="Category" onChange={handleFilterChange} />
          <input name="minPrice" placeholder="Min Price" onChange={handleFilterChange} />
          <input name="maxPrice" placeholder="Max Price" onChange={handleFilterChange} />
        </div>
        <div className="filter-actions">
          <select onChange={(e) => setSortKey(e.target.value)}>
            <option value="">Sort By...</option>
            <option value="name">Name</option>
            <option value="price">Price</option>
            <option value="quantity">Quantity</option>
          </select>
          <button className="btn filter-btn" onClick={applyFilters}>Apply Filters</button>
        </div>
      </div>

      <div className="add-sweet-card">
        <h2>🆕 Add New Sweet</h2>
        <div className="add-grid">
          <input name="name" placeholder="Name" value={newSweet.name} onChange={handleNewSweetChange} />
          <input name="category" placeholder="Category" value={newSweet.category} onChange={handleNewSweetChange} />
          <input name="price" placeholder="Price" value={newSweet.price} onChange={handleNewSweetChange} />
          <input name="quantity" placeholder="Quantity" value={newSweet.quantity} onChange={handleNewSweetChange} />
          <button className="btn add-btn" onClick={handleAddSweet}>Add Sweet</button>
        </div>
      </div>

      <div className="sweet-table-wrapper">
        <table className="sweet-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Qty</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sweets.map(sweet => (
              <SweetRow key={sweet._id} sweet={sweet} refreshSweetList={fetchSweets} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SweetList;
