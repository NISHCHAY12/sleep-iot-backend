import axios from "axios";

const BASE_URL = "https://web-production-22e4d0.up.railway.app";

export const getStatus = () =>
  axios.get(`${BASE_URL}/status`);

export const toggleSystem = () =>
  axios.post(`${BASE_URL}/toggle`);

export const setMode = (mode) =>
  axios.post(`${BASE_URL}/mode/${mode}`);

export const sendFeedback = (value) =>
  axios.post(`${BASE_URL}/feedback/${value}`);