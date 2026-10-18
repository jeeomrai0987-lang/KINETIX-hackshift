import apiClient from './client';

export const founderApi = {
  getVenturesMine: () => apiClient.get('/ventures/mine'),
  getMyVentures: () => apiClient.get('/ventures/mine'),
  createVenture: (data) => apiClient.post('/ventures', data),
  updateVenture: (ventureId, data) => apiClient.put(`/ventures/${ventureId}`, data),
  getDashboard: (ventureId) => apiClient.get(`/ventures/${ventureId}/dashboard`),
  decomposeThesis: (ventureId, thesis) => apiClient.post(`/ventures/${ventureId}/decompose`, { thesis }),
  approveBlueprint: (ventureId, payload = {}) =>
    apiClient.post(`/ventures/${ventureId}/blueprint/approve`, Array.isArray(payload) ? { blueprint: payload } : payload),
  getMatches: (ventureId) => apiClient.get(`/ventures/${ventureId}/matches`),
  rerunMatches: (ventureId) => apiClient.post(`/ventures/${ventureId}/matches/rerun`),
  inviteCandidate: (matchId, payload = {}) => apiClient.post(`/matches/${matchId}/invite`, payload),
  getChallenge: (ventureId) => apiClient.get(`/ventures/${ventureId}/challenge`),
  getSubmissions: (challengeId) => apiClient.get(`/challenges/${challengeId}/submissions`),
  scoreSubmission: (submissionId, payload) => apiClient.post(`/submissions/${submissionId}/score`, payload),
  signSubmission: (submissionId) => apiClient.post(`/submissions/${submissionId}/sign`),
  getSubmissionProof: (submissionId) => apiClient.get(`/submissions/${submissionId}/proof`),
  getRestructuring: (ventureId) => apiClient.get(`/ventures/${ventureId}/restructuring`),
  executeRestructuring: (ventureId, payload) => apiClient.post(`/ventures/${ventureId}/restructuring/execute`, payload),
  getFundingOpportunities: (ventureId, category = '') => {
    const query = category ? `?category=${encodeURIComponent(category)}` : '';
    return apiClient.get(`/ventures/${ventureId}/funding-opportunities${query}`);
  },
  requestFunding: (opportunityId, payload = {}) =>
    apiClient.post(`/funding-opportunities/${opportunityId}/request`, typeof payload === 'string' ? { note: payload } : (payload || {})),
  getFinancials: (ventureId, range = '6m') => apiClient.get(`/ventures/${ventureId}/financials?range=${range}`),
  getTransactions: (ventureId) => apiClient.get(`/ventures/${ventureId}/transactions`),
  getCapTable: (ventureId) => apiClient.get(`/ventures/${ventureId}/cap-table`),
  exportFinancialsCsv: (ventureId) => apiClient.get(`/ventures/${ventureId}/financials/export.csv`),
  downloadFinancialsCsv: async (ventureId) => {
    const csvText = await apiClient.get(`/ventures/${ventureId}/financials/export.csv`);
    if (typeof window !== 'undefined' && typeof document !== 'undefined') {
      const blob = new Blob([csvText], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `financials_${ventureId}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
    return csvText;
  },
};

export default founderApi;
