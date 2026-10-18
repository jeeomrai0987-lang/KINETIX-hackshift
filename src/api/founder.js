import { api } from './client';

export const founderApi = {
  getMyVentures: () => api.get('/ventures/mine'),
  createVenture: (data) => api.post('/ventures', data),
  updateVenture: (id, data) => api.put(`/ventures/${id}`, data),
  getDashboard: (id) => api.get(`/ventures/${id}/dashboard`),
  decomposeThesis: (id, thesis) => api.post(`/ventures/${id}/decompose`, { thesis }),
  approveBlueprint: (id, roles) => api.post(`/ventures/${id}/blueprint/approve`, { roles }),
  getMatches: (id) => api.get(`/ventures/${id}/matches`),
  rerunMatches: (id) => api.post(`/ventures/${id}/matches/rerun`),
  inviteCandidate: (matchId, data = {}) => api.post(`/matches/${matchId}/invite`, data),
  getChallenge: (id) => api.get(`/ventures/${id}/challenge`),
  getSubmissions: (challengeId) => api.get(`/challenges/${challengeId}/submissions`),
  scoreSubmission: (submissionId, vectorScores, score, reviewerVerdict) =>
    api.post(`/submissions/${submissionId}/score`, { vectorScores, score, reviewerVerdict }),
  signSubmission: (submissionId, note) => api.post(`/submissions/${submissionId}/sign`, { signatureNote: note }),
  getSubmissionProof: (submissionId) => api.get(`/submissions/${submissionId}/proof`),
  getRestructuring: (id) => api.get(`/ventures/${id}/restructuring`),
  executeRestructuring: (id, candidateId, equityPct, note) =>
    api.post(`/ventures/${id}/restructuring/execute`, { candidateId, equityPct, note }),
  getFundingOpportunities: (id, category) =>
    api.get(`/ventures/${id}/funding-opportunities${category ? `?category=${category}` : ''}`),
  requestFunding: (opportunityId, ventureId) =>
    api.post(`/funding-opportunities/${opportunityId}/request`, { ventureId }),
  getFinancials: (id, range = '6m') => api.get(`/ventures/${id}/financials?range=${range}`),
  getTransactions: (id) => api.get(`/ventures/${id}/transactions`),
  getCapTable: (id) => api.get(`/ventures/${id}/cap-table`),
  exportFinancialsCsvUrl: (id) => `/api/v1/ventures/${id}/financials/export.csv`,
};
