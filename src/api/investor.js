import { api } from './client';

export const investorApi = {
  getDashboard: () => api.get('/investor/dashboard'),
  getPortfolio: () => api.get('/investor/portfolio'),
  getUpdates: () => api.get('/investor/updates'),
  markUpdateRead: (id) => api.post(`/investor/updates/${id}/read`),
  getFinancialReports: () => api.get('/investor/financial-reports'),
  getInstruments: () => api.get('/investor/instruments'),
  getDiscoverStartups: () => api.get('/investor/discover'),
  createDisclosureRequest: (ventureId) => api.post('/investor/disclosure-requests', { ventureId }),
  getSettings: () => api.get('/investor/settings'),
  updateSettings: (data) => api.put('/investor/settings', data),
  recertify: () => api.post('/investor/settings/recertify'),
};
