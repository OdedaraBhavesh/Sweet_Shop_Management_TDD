// src/services/api.js

import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // FastAPI default port
  withCredentials: false, // use true if using cookies for auth
});

export default api;
