const [cart, setCart] = useState([]);

const fetchCart = async () => {
  const res = await fetch('http://localhost:8000/cart');
  const data = await res.json();
  setCart(data);
};
