import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Toast } from './components/common/Toast';

import { ProtectedRoute } from './components/auth/ProtectedRoute';

// Layouts
import { FounderLayout } from './components/layout/FounderLayout';
import { InvestorLayout } from './components/layout/InvestorLayout';
import { WorkerLayout } from './components/layout/WorkerLayout';

// Public & Auth
import { LandingPage } from './pages/public/LandingPage';
import { AuthPage } from './pages/auth/AuthPage';

// Founder Pages
import { FounderDashboard } from './pages/founder/FounderDashboard';
import { FounderStartup } from './pages/founder/FounderStartup';
import { FounderArena } from './pages/founder/FounderArena';
import { FounderChallenge } from './pages/founder/FounderChallenge';
import { FounderProofWork } from './pages/founder/FounderProofWork';
import { FounderRestructuring } from './pages/founder/FounderRestructuring';
import { FounderFunding } from './pages/founder/FounderFunding';
import { FounderFinancial } from './pages/founder/FounderFinancial';

// Investor Pages
import { InvestorDashboard } from './pages/investor/InvestorDashboard';
import { InvestorPortfolio } from './pages/investor/InvestorPortfolio';
import { InvestorStartup } from './pages/investor/InvestorStartup';
import { InvestorFinancialReport } from './pages/investor/InvestorFinancialReport';
import { InvestorInvestmentTerms } from './pages/investor/InvestorInvestmentTerms';
import { InvestorDiscoverStartups } from './pages/investor/InvestorDiscoverStartups';
import { InvestorSettings } from './pages/investor/InvestorSettings';

// Worker Pages
import { WorkerDashboard } from './pages/worker/WorkerDashboard';
import { WorkerProfile } from './pages/worker/WorkerProfile';
import { WorkerOpportunities } from './pages/worker/WorkerOpportunities';
import { WorkerInvitations } from './pages/worker/WorkerInvitations';
import { WorkerProofOfWork } from './pages/worker/WorkerProofOfWork';
import { WorkerSettings } from './pages/worker/WorkerSettings';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public & Authentication */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/landing" element={<LandingPage />} />
          <Route path="/landing.html" element={<Navigate to="/" replace />} />
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/login" element={<AuthPage />} />
          <Route path="/login.html" element={<Navigate to="/auth" replace />} />
          <Route path="/register" element={<AuthPage />} />

          {/* Founder Portal Routes */}
          <Route
            path="/founder"
            element={
              <ProtectedRoute allowedRole="founder">
                <FounderLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/founder/dashboard" replace />} />
            <Route path="dashboard" element={<FounderDashboard />} />
            <Route path="startup" element={<FounderStartup />} />
            <Route path="arena" element={<FounderArena />} />
            <Route path="challenge" element={<FounderChallenge />} />
            <Route path="proofwork" element={<FounderProofWork />} />
            <Route path="restructuring" element={<FounderRestructuring />} />
            <Route path="funding" element={<FounderFunding />} />
            <Route path="financial" element={<FounderFinancial />} />
          </Route>

          {/* Investor Portal Routes */}
          <Route
            path="/investor"
            element={
              <ProtectedRoute allowedRole="investor">
                <InvestorLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/investor/dashboard" replace />} />
            <Route path="dashboard" element={<InvestorDashboard />} />
            <Route path="portfolio" element={<InvestorPortfolio />} />
            <Route path="startup" element={<InvestorStartup />} />
            <Route path="financial-report" element={<InvestorFinancialReport />} />
            <Route path="investment-terms" element={<InvestorInvestmentTerms />} />
            <Route path="discover-startups" element={<InvestorDiscoverStartups />} />
            <Route path="settings" element={<InvestorSettings />} />
          </Route>

          {/* Worker Portal Routes */}
          <Route
            path="/worker"
            element={
              <ProtectedRoute allowedRole="worker">
                <WorkerLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/worker/dashboard" replace />} />
            <Route path="dashboard" element={<WorkerDashboard />} />
            <Route path="profile" element={<WorkerProfile />} />
            <Route path="opportunities" element={<WorkerOpportunities />} />
            <Route path="invitations" element={<WorkerInvitations />} />
            <Route path="proof-of-work" element={<WorkerProofOfWork />} />
            <Route path="settings" element={<WorkerSettings />} />
          </Route>

          {/* Legacy HTML path redirects for backward compatibility */}
          <Route path="/Founder/dashboard.html" element={<Navigate to="/founder/dashboard" replace />} />
          <Route path="/Founder/startup.html" element={<Navigate to="/founder/startup" replace />} />
          <Route path="/Founder/arena.html" element={<Navigate to="/founder/arena" replace />} />
          <Route path="/Founder/challenge.html" element={<Navigate to="/founder/challenge" replace />} />
          <Route path="/Founder/proofwork.html" element={<Navigate to="/founder/proofwork" replace />} />
          <Route path="/Founder/restructuring.html" element={<Navigate to="/founder/restructuring" replace />} />
          <Route path="/Founder/funding.html" element={<Navigate to="/founder/funding" replace />} />
          <Route path="/Founder/financial.html" element={<Navigate to="/founder/financial" replace />} />

          <Route path="/investor/dashboard.html" element={<Navigate to="/investor/dashboard" replace />} />
          <Route path="/investor/portfolio.html" element={<Navigate to="/investor/portfolio" replace />} />
          <Route path="/investor/startup.html" element={<Navigate to="/investor/startup" replace />} />
          <Route path="/investor/financial_report.html" element={<Navigate to="/investor/financial-report" replace />} />
          <Route path="/investor/investment_terms.html" element={<Navigate to="/investor/investment-terms" replace />} />
          <Route path="/investor/discover_startups.html" element={<Navigate to="/investor/discover-startups" replace />} />
          <Route path="/investor/settings.html" element={<Navigate to="/investor/settings" replace />} />

          <Route path="/worker/dashboard.html" element={<Navigate to="/worker/dashboard" replace />} />
          <Route path="/worker/profile.html" element={<Navigate to="/worker/profile" replace />} />
          <Route path="/worker/opportunities.html" element={<Navigate to="/worker/opportunities" replace />} />
          <Route path="/worker/invitations.html" element={<Navigate to="/worker/invitations" replace />} />
          <Route path="/worker/proof_of_work_report.html" element={<Navigate to="/worker/proof-of-work" replace />} />
          <Route path="/worker/settings.html" element={<Navigate to="/worker/settings" replace />} />

          {/* Catch-all Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        <Toast />
      </BrowserRouter>
    </AuthProvider>
  );
}
