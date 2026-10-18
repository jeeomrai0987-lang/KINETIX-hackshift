import apiClient from './client';

export const authApi = {
  register: (payload) => apiClient.post('/auth/register', payload),
  login: (credentials) => apiClient.post('/auth/login', credentials),
  demoLogin: (role) => apiClient.post(`/auth/demo/${role}`),
  getMe: () => apiClient.get('/auth/me'),
};

export default authApi;
