import { api } from './client';

export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (email, password) => api.post('/auth/login', { email, password }),
  demoLogin: (role) => api.post(`/auth/demo/${role}`),
  getMe: () => api.get('/auth/me'),
};
