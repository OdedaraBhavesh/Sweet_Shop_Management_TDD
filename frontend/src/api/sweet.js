import axios from "axios";

const BASE_URL = "http://localhost:8000/api"; // FastAPI backend

export const fetchSweets = async () => {
  const response = await axios.get(`${BASE_URL}/sweets`);
  return response.data;
};

export const purchaseSweet = async (sweetId) => {
  const response = await axios.post(`${BASE_URL}/sweets/${sweetId}/purchase`);
  return response.data;
};
