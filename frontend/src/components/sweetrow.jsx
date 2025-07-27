import React from 'react';

const SweetRow = ({ sweet, onPurchase }) => {
  const handlePurchase = () => {
    if (sweet.quantity > 0) {
      onPurchase(sweet._id);
    }
  };

  return (
    <div className="sweet-card">
      <h3>{sweet.name}</h3>
      <p>Price: ₹{sweet.price}</p>
      <p>Available: {sweet.quantity}</p>
      <button
        onClick={handlePurchase}
        disabled={sweet.quantity === 0}
      >
        {sweet.quantity === 0 ? 'Out of Stock' : 'Purchase'}
      </button>
    </div>
  );
};

export default SweetRow;
