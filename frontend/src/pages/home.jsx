import React from 'react';
import SweetList from '../components/Sweet_list';

import '../css/home.css';

const Home = () => {
  return (
    <div className="home-container">
      <header className="header">
        <h1>🧁The Sweet Spot</h1>
      </header>
      <SweetList />
      <footer className="footer">
        <p>© 2025 Sweet Shop. Made with 🍬 and ❤️</p>
      </footer>
    </div>
  );
};

export default Home;

