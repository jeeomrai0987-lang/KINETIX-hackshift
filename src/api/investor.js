import apiClient from './client';

export const investorApi = {
  getDashboard: () => apiClient.get('/investor/dashboard'),
  getPortfolio: () => apiClient.get('/investor/portfolio'),
  getUpdates: () => apiClient.get('/investor/updates'),
  markUpdateRead: (updateId) => apiClient.post(`/investor/updates/${updateId}/read`),
  getFinancialReports: () => apiClient.get('/investor/financial-reports'),
  getInstruments: () => apiClient.get('/investor/instruments'),
  getDiscover: () => apiClient.get('/investor/discover'),
  requestDisclosure: (payload) => apiClient.post('/investor/disclosure-requests', payload),
  getSettings: () => apiClient.get('/investor/settings'),
  updateSettings: (settingsData) => apiClient.put('/investor/settings', settingsData),
  recertify: (payload = {}) => apiClient.post('/investor/settings/recertify', payload),
};

export default investorApi;
