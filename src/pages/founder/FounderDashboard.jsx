import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { founderApi } from '../../api/founder';

export const FounderDashboard = () => {
  const { user, showToast } = useAuth();
  const [activeTab, setActiveTab] = useState('all');
  const [showCandidateModal, setShowCandidateModal] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDashboard = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // First get venture ID or fallback to 'ven_synthetix'
      const myVentures = await founderApi.getMyVentures().catch(() => ({ items: [] }));
      const ventureId = myVentures?.items?.[0]?.id || 'ven_synthetix';
      const data = await founderApi.getDashboard(ventureId);
      setDashboardData(data);
    } catch (err) {
      console.warn('Using local fallback for dashboard:', err.message);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  return (
    <div className="flex flex-col w-full gap-space-lg">
      {/* Top Welcome & Telemetry Action Bar */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-space-md bg-surface-container-lowest p-space-lg rounded-xl shadow-sm">
        <div className="flex flex-col gap-space-xs">
          <div className="flex items-center gap-space-sm flex-wrap">
            <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              Welcome back, {user?.name || 'Elena'}
            </h1>
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-secondary-container/50 text-on-secondary-container font-label-sm text-label-sm">
              <span className="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
              <span>Live Telemetry Active</span>
            </div>
            <div className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-surface-container text-on-surface-variant font-code-sm text-code-sm">
              <span>Batch Alpha #204</span>
            </div>
          </div>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Overview of <span className="font-semibold text-primary-container">{user?.entity || 'Synthetix AI'}</span>{' '}
            venture formation, team restructuring, &amp; sprint velocity.
          </p>
        </div>

        {/* Quick Control CTAs */}
        <div className="flex items-center gap-space-sm flex-wrap">
          <Link
            to="/founder/arena"
            className="px-space-md h-10 rounded-lg bg-surface-container-low hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-all flex items-center gap-2 shadow-sm"
          >
            <span className="material-symbols-outlined text-[18px]">person_add</span>
            <span>Invite Co-founder</span>
          </Link>
          <Link
            to="/founder/challenge"
            className="px-space-md h-10 rounded-lg bg-secondary hover:bg-on-secondary-fixed-variant text-on-secondary font-label-md text-label-md font-semibold transition-all shadow-sm flex items-center gap-2"
          >
            <span className="material-symbols-outlined text-[18px]">bolt</span>
            <span>Launch Sprint Challenge</span>
          </Link>
        </div>
      </div>

      {/* 4-Stat Metric Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-space-md">
        {/* Stat 1: Squad Synergy */}
        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex flex-col gap-1">
              <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
                Squad Synergy
              </span>
              <div className="flex items-baseline gap-2">
                <span className="font-headline-md text-headline-md font-bold text-on-surface">88%</span>
                <span className="font-label-sm text-label-sm text-secondary font-semibold flex items-center">
                  <span className="material-symbols-outlined text-[14px]">trending_up</span>+4% boost
                </span>
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-primary-container">
              <span className="material-symbols-outlined text-[20px]">group_work</span>
            </div>
          </div>
          <div className="mt-space-md">
            <div className="flex justify-between items-center font-body-sm text-body-sm text-on-surface-variant mb-1.5">
              <span>3 of 4 Core Roles Active</span>
              <span className="text-tertiary-container font-semibold">1 Vacancy</span>
            </div>
            <div className="w-full bg-surface-container-high h-2 rounded-full overflow-hidden flex">
              <div className="bg-secondary h-full rounded-full transition-all duration-500" style={{ width: '75%' }}></div>
              <div className="bg-tertiary-fixed-dim h-full w-[25%] opacity-60"></div>
            </div>
          </div>
        </div>

        {/* Stat 2: Active Challenge */}
        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex flex-col gap-1">
              <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
                Active Challenge
              </span>
              <span className="font-title-md text-title-md font-bold text-primary-container truncate max-w-[170px]" title="Sprint #3: GTM Stress Test">
                Sprint #3: GTM Test
              </span>
            </div>
            <div className="w-10 h-10 rounded-lg bg-secondary-container/40 flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[20px]">timer</span>
            </div>
          </div>
          <div className="mt-space-md">
            <div className="flex items-center justify-between mb-1.5">
              <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-error-container text-on-error-container font-label-sm text-label-sm font-semibold">
                <span className="material-symbols-outlined text-[13px]">alarm</span> 18h 42m left
              </span>
              <span className="font-body-sm text-body-sm text-on-surface-variant">2/3 Done</span>
            </div>
            <div className="w-full bg-surface-container-high h-2 rounded-full overflow-hidden">
              <div className="bg-primary-container h-full rounded-full transition-all duration-500" style={{ width: '66.6%' }}></div>
            </div>
          </div>
        </div>

        {/* Stat 3: Investor Pipeline */}
        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex flex-col gap-1">
              <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
                Investor Pipeline
              </span>
              <div className="flex items-baseline gap-2">
                <span className="font-headline-md text-headline-md font-bold text-on-surface">14 VCs</span>
                <span className="font-label-sm text-label-sm px-2 py-0.5 rounded-full bg-surface-container font-semibold text-secondary">
                  94% avg fit
                </span>
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-primary-container">
              <span className="material-symbols-outlined text-[20px]">handshake</span>
            </div>
          </div>
          <div className="mt-space-md flex items-center justify-between">
            <span className="font-body-sm text-body-sm text-on-surface-variant">3 Term Sheet Inquiries</span>
            <Link to="/founder/funding" className="font-label-sm text-label-sm text-secondary font-semibold hover:underline flex items-center gap-0.5">
              Syndicates <span className="material-symbols-outlined text-[14px]">arrow_forward</span>
            </Link>
          </div>
        </div>

        {/* Stat 4: Net Monthly Burn */}
        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col justify-between hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex flex-col gap-1">
              <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
                Net Monthly Burn
              </span>
              <div className="flex items-baseline gap-2">
                <span className="font-headline-md text-headline-md font-bold text-on-surface">-$14,800</span>
                <span className="font-label-sm text-label-sm px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-semibold">
                  Healthy
                </span>
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-primary-container">
              <span className="material-symbols-outlined text-[20px]">account_balance</span>
            </div>
          </div>
          <div className="mt-space-md flex items-center justify-between">
            <span className="font-body-sm text-body-sm text-on-surface-variant">
              Runway: <strong className="text-on-surface font-semibold">16.4 Mos</strong>
            </span>
            <span className="font-code-sm text-code-sm text-on-surface-variant">$242k Treasury</span>
          </div>
        </div>
      </div>

      {/* Primary Workspace: Two-Column Composition */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        {/* Main Column (Left, 8 Cols) */}
        <div className="lg:col-span-8 flex flex-col gap-space-lg">
          {/* Critical Restructuring / Vacancy Alert Banner */}
          <div className="relative overflow-hidden rounded-xl bg-gradient-to-r from-tertiary-fixed to-tertiary-fixed-dim/40 p-space-md lg:p-space-lg shadow-sm">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-space-md">
              <div className="flex items-start gap-space-md">
                <div className="w-11 h-11 rounded-lg bg-tertiary-container text-on-tertiary-container flex items-center justify-center shrink-0 shadow-sm mt-0.5 sm:mt-0">
                  <span className="material-symbols-outlined text-[24px]">crisis_alert</span>
                </div>
                <div className="flex flex-col gap-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-title-md text-title-md font-bold text-on-tertiary-fixed">
                      Vacancy Alert: Lead Distributed Systems Architect
                    </span>
                    <span className="px-2 py-0.5 rounded-full bg-on-tertiary-fixed text-tertiary-fixed font-label-sm text-label-sm uppercase tracking-wider font-bold">
                      Dynamic Restructuring
                    </span>
                  </div>
                  <p className="font-body-md text-body-md text-on-tertiary-fixed-variant max-w-2xl">
                    Founding engineer departed Sprint #2. AI matching has automatically evaluated, scored, and shortlisted{' '}
                    <strong className="text-on-tertiary-fixed font-semibold">3 high-complementarity replacements (&gt;92% fit)</strong> from the verified Cohort Arena pool.
                  </p>
                </div>
              </div>
              <div className="flex sm:flex-col lg:flex-row items-center gap-2 w-full sm:w-auto shrink-0">
                <Link
                  to="/founder/restructuring"
                  className="flex-1 sm:flex-none px-4 py-2 rounded-lg bg-tertiary-container hover:bg-tertiary text-on-tertiary font-label-md text-label-md font-semibold transition-colors shadow-sm text-center"
                >
                  Review Candidates (3)
                </Link>
                <button
                  onClick={() => showToast('Restructuring smart-contract protocol rules synced')}
                  className="flex-1 sm:flex-none px-3.5 py-2 rounded-lg bg-surface-container-lowest/80 hover:bg-surface-container-lowest text-on-tertiary-fixed font-label-md text-label-md font-semibold transition-colors"
                  type="button"
                >
                  Protocol Log
                </button>
              </div>
            </div>
          </div>

          {/* Current Founding Squad Roster Card */}
          <div className="bg-surface-container-lowest rounded-xl shadow-sm p-space-lg flex flex-col gap-space-md">
            <div className="flex items-center justify-between flex-wrap gap-2 pb-space-sm border-b border-surface-container">
              <div>
                <h2 className="font-title-md text-title-md font-bold text-on-surface">Founding Squad Roster</h2>
                <p className="font-body-sm text-body-sm text-on-surface-variant">
                  Algorithmic role balance, archetype alignment, &amp; sprint equity status
                </p>
              </div>
              <div className="flex items-center gap-space-sm">
                <span className="px-2.5 py-1 rounded-full bg-surface-container font-label-sm text-label-sm text-on-surface font-semibold">
                  4 Roles Provisioned • 1 Seat Open
                </span>
              </div>
            </div>

            {/* Roster Member List */}
            <div className="flex flex-col gap-space-sm">
              {/* Member 1: Elena Vance */}
              <div className="p-space-md rounded-xl bg-surface-container-low hover:bg-surface-container transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-space-md">
                <div className="flex items-center gap-space-md">
                  <div className="relative w-12 h-12 rounded-xl bg-primary-container text-on-primary flex items-center justify-center font-bold text-[18px] shrink-0">
                    EV
                    <span className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-secondary flex items-center justify-center text-[10px] text-on-secondary shadow-sm">
                      <span className="material-symbols-outlined text-[10px]">star</span>
                    </span>
                  </div>
                  <div className="flex flex-col">
                    <div className="flex items-center gap-2">
                      <span className="font-title-md text-title-md font-bold text-on-surface">Elena Vance (You)</span>
                      <span className="px-2 py-0.5 rounded-full bg-primary-fixed text-on-primary-fixed font-label-sm text-label-sm font-semibold">
                        Founder / CEO
                      </span>
                    </div>
                    <div className="flex items-center gap-space-sm font-body-sm text-body-sm text-on-surface-variant flex-wrap mt-0.5">
                      <span className="font-medium text-secondary">Visionary / GTM</span>
                      <span>•</span>
                      <span>42.5% Equity Allocated</span>
                      <span>•</span>
                      <span className="text-on-surface-variant">Sprint Role: Strategy Lead</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-space-md self-end sm:self-center">
                  <div className="flex flex-col items-end">
                    <span className="font-code-sm text-code-sm text-on-surface-variant">Squad Synergy</span>
                    <span className="font-label-md text-label-md font-bold text-secondary">98% Fit Index</span>
                  </div>
                  <span className="px-2.5 py-1 rounded-full bg-secondary-container/60 text-on-secondary-container font-label-sm text-label-sm font-semibold">
                    Verified
                  </span>
                </div>
              </div>

              {/* Member 2: Marcus Chen */}
              <div className="p-space-md rounded-xl bg-surface-container-low hover:bg-surface-container transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-space-md">
                <div className="flex items-center gap-space-md">
                  <div className="relative w-12 h-12 rounded-xl bg-surface-container-highest text-on-surface font-bold text-[18px] flex items-center justify-center shrink-0">
                    MC
                    <span className="absolute -bottom-1 -right-1 w-3.5 h-3.5 rounded-full bg-secondary"></span>
                  </div>
                  <div className="flex flex-col">
                    <div className="flex items-center gap-2">
                      <span className="font-title-md text-title-md font-bold text-on-surface">Marcus Chen</span>
                      <span className="px-2 py-0.5 rounded-full bg-surface-container-high text-on-surface font-label-sm text-label-sm">
                        Co-Founder / CTO
                      </span>
                    </div>
                    <div className="flex items-center gap-space-sm font-body-sm text-body-sm text-on-surface-variant flex-wrap mt-0.5">
                      <span className="font-medium text-primary-container">Deep Tech / Infra</span>
                      <span>•</span>
                      <span>32.0% Equity Allocated</span>
                      <span>•</span>
                      <span>Sprint Role: ML Pipeline</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-space-md self-end sm:self-center">
                  <div className="flex flex-col items-end">
                    <span className="font-code-sm text-code-sm text-on-surface-variant">Squad Synergy</span>
                    <span className="font-label-md text-label-md font-bold text-secondary">95% Fit Index</span>
                  </div>
                  <span className="px-2.5 py-1 rounded-full bg-surface-container text-on-surface-variant font-label-sm text-label-sm font-semibold">
                    Active Sprint
                  </span>
                </div>
              </div>

              {/* Member 3: Sarah Jenkins */}
              <div className="p-space-md rounded-xl bg-surface-container-low hover:bg-surface-container transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-space-md">
                <div className="flex items-center gap-space-md">
                  <div className="relative w-12 h-12 rounded-xl bg-surface-container-highest text-on-surface font-bold text-[18px] flex items-center justify-center shrink-0">
                    SJ
                    <span className="absolute -bottom-1 -right-1 w-3.5 h-3.5 rounded-full bg-secondary"></span>
                  </div>
                  <div className="flex flex-col">
                    <div className="flex items-center gap-2">
                      <span className="font-title-md text-title-md font-bold text-on-surface">Sarah Jenkins</span>
                      <span className="px-2 py-0.5 rounded-full bg-surface-container-high text-on-surface font-label-sm text-label-sm">
                        Head of Growth
                      </span>
                    </div>
                    <div className="flex items-center gap-space-sm font-body-sm text-body-sm text-on-surface-variant flex-wrap mt-0.5">
                      <span className="font-medium text-primary-container">Commercial / PLG</span>
                      <span>•</span>
                      <span>10.5% Equity Allocated</span>
                      <span>•</span>
                      <span>Sprint Role: 24 Enterprise Demos</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-space-md self-end sm:self-center">
                  <div className="flex flex-col items-end">
                    <span className="font-code-sm text-code-sm text-on-surface-variant">Squad Synergy</span>
                    <span className="font-label-md text-label-md font-bold text-secondary">91% Fit Index</span>
                  </div>
                  <span className="px-2.5 py-1 rounded-full bg-surface-container text-on-surface-variant font-label-sm text-label-sm font-semibold">
                    Active Sprint
                  </span>
                </div>
              </div>

              {/* Member 4: Vacant Open Seat */}
              <div className="p-space-md rounded-xl bg-tertiary-fixed/30 hover:bg-tertiary-fixed/50 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-space-md">
                <div className="flex items-center gap-space-md">
                  <div className="w-12 h-12 rounded-xl bg-tertiary-fixed-dim text-on-tertiary-fixed flex items-center justify-center shrink-0">
                    <span className="material-symbols-outlined text-[24px]">person_search</span>
                  </div>
                  <div className="flex flex-col">
                    <div className="flex items-center gap-2">
                      <span className="font-title-md text-title-md font-bold text-on-tertiary-fixed">
                        Distributed Systems Architect
                      </span>
                      <span className="px-2 py-0.5 rounded-full bg-tertiary-fixed text-on-tertiary-fixed-variant font-label-sm text-label-sm font-bold">
                        Open Seat
                      </span>
                    </div>
                    <div className="flex items-center gap-space-sm font-body-sm text-body-sm text-on-tertiary-fixed-variant flex-wrap mt-0.5">
                      <span>Target: High-Throughput Golang/K8s</span>
                      <span>•</span>
                      <span>15.0% Reserve Pool</span>
                      <span>•</span>
                      <span className="font-medium text-on-tertiary-container">3 Blind Profiles Ready</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-space-md self-end sm:self-center">
                  <div className="flex flex-col items-end">
                    <span className="font-code-sm text-code-sm text-on-tertiary-fixed-variant">AI Threshold</span>
                    <span className="font-label-md text-label-md font-bold text-on-tertiary-container">
                      &gt;92% Complementarity
                    </span>
                  </div>
                  <Link
                    to="/founder/restructuring"
                    className="px-3 py-1.5 rounded-lg bg-tertiary-container hover:bg-tertiary text-on-tertiary font-label-md text-label-md font-semibold transition-colors flex items-center gap-1 shadow-sm"
                  >
                    <span>Evaluate</span>
                    <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
                  </Link>
                </div>
              </div>
            </div>

            {/* Sprint Milestones Micro-Tracker */}
            <div className="pt-space-sm mt-space-xs flex flex-col gap-space-xs border-t border-surface-container">
              <div className="flex items-center justify-between">
                <span className="font-label-md text-label-md font-semibold text-on-surface">
                  Sprint #3 Deliverables Checklist
                </span>
                <span className="font-body-sm text-body-sm text-on-surface-variant">Live Validation Engine</span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-space-sm mt-1">
                <div className="p-space-sm rounded-lg bg-surface-container-low flex items-center gap-2">
                  <span className="material-symbols-outlined text-secondary text-[20px]">check_circle</span>
                  <div className="flex flex-col min-w-0">
                    <span className="font-label-sm text-label-sm font-semibold text-on-surface truncate">
                      Value Prop Synthetic Deck
                    </span>
                    <span className="font-body-sm text-body-sm text-on-surface-variant">Approved (Score: 96)</span>
                  </div>
                </div>
                <div className="p-space-sm rounded-lg bg-surface-container-low flex items-center gap-2">
                  <span className="material-symbols-outlined text-secondary text-[20px]">check_circle</span>
                  <div className="flex flex-col min-w-0">
                    <span className="font-label-sm text-label-sm font-semibold text-on-surface truncate">
                      Cold Lead Conversion API
                    </span>
                    <span className="font-body-sm text-body-sm text-on-surface-variant">Passed 40 Stress Tests</span>
                  </div>
                </div>
                <div className="p-space-sm rounded-lg bg-surface-container-low flex items-center gap-2">
                  <span className="material-symbols-outlined text-outline text-[20px]">pending</span>
                  <div className="flex flex-col min-w-0">
                    <span className="font-label-sm text-label-sm font-semibold text-on-surface truncate">
                      Investor Teaser Delivery
                    </span>
                    <span className="font-body-sm text-body-sm text-on-surface-variant">In Review (18h left)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Secondary Column (Right, 4 Cols) */}
        <div className="lg:col-span-4 flex flex-col gap-space-lg">
          {/* Financial Trajectory Chart Card */}
          <div className="bg-surface-container-lowest rounded-xl shadow-sm p-space-lg flex flex-col justify-between">
            <div className="flex items-center justify-between mb-space-sm">
              <div>
                <h2 className="font-title-md text-title-md font-bold text-on-surface">Financial Trajectory</h2>
                <p className="font-body-sm text-body-sm text-on-surface-variant">MRR scaling vs. monthly burn</p>
              </div>
              <span className="px-2 py-0.5 rounded-full bg-surface-container font-code-sm text-code-sm text-on-surface-variant">
                Last 6 Mos
              </span>
            </div>

            {/* Legend */}
            <div className="flex items-center gap-space-md mb-space-md">
              <div className="flex items-center gap-1.5 font-label-sm text-label-sm text-on-surface">
                <span className="w-3 h-3 rounded-sm bg-secondary"></span>
                <span>Revenue</span>
              </div>
              <div className="flex items-center gap-1.5 font-label-sm text-label-sm text-on-surface-variant">
                <span className="w-3 h-3 rounded-sm bg-primary-container"></span>
                <span>Expenses</span>
              </div>
            </div>

            {/* Custom Inline Visual Chart */}
            <div className="w-full h-44 flex items-end justify-between gap-2 px-1 pb-1">
              {[
                { m: 'Oct', r: '12%', b: '72%' },
                { m: 'Nov', r: '18%', b: '75%' },
                { m: 'Dec', r: '25%', b: '80%' },
                { m: 'Jan', r: '32%', b: '78%' },
                { m: 'Feb', r: '42%', b: '84%' },
                { m: 'Mar', r: '54%', b: '86%' },
              ].map((item) => (
                <div key={item.m} className="flex flex-col items-center flex-1 h-full justify-end gap-1 group">
                  <div className="w-full flex items-end justify-center gap-1 h-32">
                    <div
                      className="w-2.5 sm:w-3 bg-secondary rounded-t transition-all group-hover:opacity-80"
                      style={{ height: item.r }}
                    ></div>
                    <div
                      className="w-2.5 sm:w-3 bg-primary-container rounded-t transition-all group-hover:opacity-80"
                      style={{ height: item.b }}
                    ></div>
                  </div>
                  <span className="font-code-sm text-code-sm text-on-surface-variant">{item.m}</span>
                </div>
              ))}
            </div>

            {/* Metric Summary Footnote */}
            <div className="mt-space-md p-space-sm rounded-lg bg-surface-container-low flex flex-col gap-1">
              <div className="flex items-center justify-between font-label-sm text-label-sm">
                <span className="text-on-surface-variant">Current MRR</span>
                <span className="font-bold text-on-surface">
                  $8,500 <span className="text-secondary font-semibold">(+28% MoM)</span>
                </span>
              </div>
              <div className="flex items-center justify-between font-label-sm text-label-sm">
                <span className="text-on-surface-variant">Gross Expenses</span>
                <span className="font-semibold text-on-surface">$21,400 / mo</span>
              </div>
              <div className="flex items-center justify-between font-label-sm text-label-sm pt-1 mt-0.5 border-t border-surface-container">
                <span className="text-on-surface-variant">Runway Projection</span>
                <span className="font-bold text-secondary">16.4 Months Solid</span>
              </div>
            </div>
          </div>

          {/* Activity Feed */}
          <div className="bg-surface-container-lowest rounded-xl shadow-sm p-space-lg flex flex-col">
            <div className="flex items-center justify-between mb-space-md">
              <div className="flex items-center gap-2">
                <h2 className="font-title-md text-title-md font-bold text-on-surface">Cohort &amp; Sprint Log</h2>
                <span className="w-2 h-2 rounded-full bg-secondary"></span>
              </div>
              <span className="font-code-sm text-code-sm text-on-surface-variant">Live Feed</span>
            </div>

            <div className="flex flex-col gap-space-md relative pl-5">
              <div className="absolute left-2 top-2 bottom-2 w-0.5 bg-surface-container-high"></div>

              {[
                {
                  dot: 'bg-secondary',
                  title: 'Blind Scoring Completed',
                  time: '25m ago',
                  desc: 'Candidate Beta-902 scored 94.2/100 on Kubernetes orchestrator challenge.',
                },
                {
                  dot: 'bg-primary-container',
                  title: 'Pitch Deck Inquired',
                  time: '2h ago',
                  desc: 'Apex Horizon Capital requested unlocked data room privileges.',
                },
                {
                  dot: 'bg-surface-tint',
                  title: 'Candidate Screener',
                  time: '4h ago',
                  desc: 'Automated WhatsApp screening finished for applicant Alex K. (91% affinity).',
                },
                {
                  dot: 'bg-outline',
                  title: 'Cap Table Auto-Vesting',
                  time: 'Yesterday',
                  desc: 'System adjusted role allocations according to Sprint #2 deliverables completion.',
                },
              ].map((activity, idx) => (
                <div key={idx} className="relative flex flex-col gap-0.5">
                  <span
                    className={`absolute -left-5 top-1 w-2.5 h-2.5 rounded-full ${activity.dot} ring-4 ring-surface-container-lowest`}
                  ></span>
                  <div className="flex items-center justify-between">
                    <span className="font-label-sm text-label-sm font-semibold text-on-surface">
                      {activity.title}
                    </span>
                    <span className="font-code-sm text-code-sm text-on-surface-variant">{activity.time}</span>
                  </div>
                  <p className="font-body-sm text-body-sm text-on-surface-variant">{activity.desc}</p>
                </div>
              ))}
            </div>

            <button
              onClick={() => showToast('Full audit trail log exported to report')}
              className="mt-space-md w-full py-2 rounded-lg bg-surface-container-low hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-colors text-center"
              type="button"
            >
              View Complete Audit Log
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
