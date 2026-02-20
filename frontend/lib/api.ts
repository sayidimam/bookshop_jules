import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getBooks = async (params: any = {}) => {
  const response = await api.get('/catalog/books/', { params });
  return response.data;
};

export const getBookDetail = async (slug: string) => {
  const response = await api.get(`/catalog/books/${slug}/`);
  return response.data;
};

export default api;
