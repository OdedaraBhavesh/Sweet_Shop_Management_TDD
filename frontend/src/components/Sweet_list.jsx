import React, { useEffect, useState } from 'react';
import axios from 'axios';
import SweetRow from './sweetrow'; // ⬅️ import the component

const SweetList = () => {
  const [sweets, setSweets] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/sweets')
      .then(response => setSweets(response.data))
      .catch(error => console.error("Error fetching sweets:", error));
  }, []);

  const handlePurchase = async (sweetId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`http://localhost:8000/purchase/${sweetId}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert("Purchase successful");
      // Refresh the sweet list to update quantity
      const updatedSweets = await axios.get('http://localhost:8000/sweets');
      setSweets(updatedSweets.data);
    } catch (error) {
      alert("Purchase failed");
      console.error(error);
    }
  };

  return (
    <div className="sweet-list">
      <h2>Available Sweets</h2>
      {sweets.map(sweet => (
        <SweetRow key={sweet._id} sweet={sweet} onPurchase={handlePurchase} />
      ))}
    </div>
  );
};

export default SweetList;
