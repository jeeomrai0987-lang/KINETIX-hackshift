import { api } from './client';

export const workerApi = {
  getDashboard: () => api.get('/worker/dashboard'),
  getProfile: () => api.get('/worker/profile'),
  updateProfile: (data) => api.put('/worker/profile', data),
  getSettings: () => api.get('/worker/settings'),
  updateSettings: (data) => api.put('/worker/settings', data),
  getOpportunities: () => api.get('/worker/opportunities'),
  refreshOpportunities: () => api.post('/worker/opportunities/refresh'),
  applyOpportunity: (roleId, blindToken) => api.post(`/worker/opportunities/${roleId}/apply`, { blindToken }),
  getInvitations: (status) => api.get(`/worker/invitations${status ? `?status=${status}` : ''}`),
  acceptInvitation: (id) => api.post(`/invitations/${id}/accept`),
  declineInvitation: (id) => api.post(`/invitations/${id}/decline`),
  getProofOfWork: () => api.get('/worker/proof-of-work'),
};
