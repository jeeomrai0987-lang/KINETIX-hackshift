import apiClient from './client';

export const workerApi = {
  getDashboard: () => apiClient.get('/worker/dashboard'),
  getProfile: () => apiClient.get('/worker/profile'),
  updateProfile: (profileData) => apiClient.put('/worker/profile', profileData),
  getSettings: () => apiClient.get('/worker/settings'),
  updateSettings: (settingsData) => apiClient.put('/worker/settings', settingsData),
  getOpportunities: () => apiClient.get('/worker/opportunities'),
  refreshOpportunities: () => apiClient.post('/worker/opportunities/refresh'),
  applyOpportunity: (roleId, payload = {}) => apiClient.post(`/worker/opportunities/${roleId}/apply`, payload),
  getInvitations: (status = '') => {
    const query = status ? `?status=${encodeURIComponent(status)}` : '';
    return apiClient.get(`/worker/invitations${query}`);
  },
  acceptInvitation: (invitationId, payload = {}) => apiClient.post(`/invitations/${invitationId}/accept`, payload),
  declineInvitation: (invitationId, payload = {}) => apiClient.post(`/invitations/${invitationId}/decline`, payload),
  getProofOfWork: () => apiClient.get('/worker/proof-of-work'),
};

export default workerApi;
