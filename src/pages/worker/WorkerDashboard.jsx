import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const WorkerDashboard = () => {
  const { user, showToast } = useAuth();

  return (
    <div className="px-space-lg py-space-lg max-w-[1440px] mx-auto w-full flex flex-col gap-space-lg">
      {/* Top Status Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-space-sm bg-surface-container-lowest p-space-md rounded-xl shadow-sm">
        <div className="flex items-center gap-space-xs flex-wrap font-label-md text-label-md text-on-surface-variant">
          <span className="text-secondary font-semibold">Cohort Alpha '25</span>
          <span className="material-symbols-outlined text-[14px]">chevron_right</span>
          <span>Worker Portal</span>
          <span className="material-symbols-outlined text-[14px]">chevron_right</span>
          <span className="text-on-surface font-semibold">Talent Dashboard</span>
          <span className="inline-flex items-center gap-1.5 ml-space-sm px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm">
            <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
            Live Evaluation Mesh Active
          </span>
        </div>
        <div className="flex items-center gap-space-xs">
          <span className="font-code-sm text-code-sm text-on-surface-variant bg-surface-container px-2 py-0.5 rounded">
            NODE-ID: {user?.nodeId || 'TX-5512B'}
          </span>
          <span className="px-2 py-0.5 rounded-full bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wide">
            Demo data
          </span>
        </div>
      </div>

      {/* Page Header */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-space-md">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
            Talent Dashboard &amp; Execution Command
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Track blind evaluation metrics, active 48h challenges, and founder squad invitations.
          </p>
        </div>
        <div className="flex items-center gap-space-sm">
          <Link
            to="/worker/opportunities"
            className="px-4 py-2 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-all"
          >
            Explore Squads
          </Link>
          <Link
            to="/worker/invitations"
            className="px-4 py-2 rounded-lg bg-secondary text-on-secondary font-label-md text-label-md font-semibold hover:opacity-90 transition-all shadow-xs"
          >
            Review 3 Invitations
          </Link>
        </div>
      </div>

      {/* Top 4 Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md">
        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
                Rubric Standing
              </span>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="font-headline-md text-headline-md font-bold text-on-surface">Top 4%</span>
                <span className="font-code-sm text-secondary font-bold">96.4/100</span>
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[20px]">workspace_premium</span>
            </div>
          </div>
          <span className="font-body-sm text-xs text-on-surface-variant mt-3 border-t border-surface-container pt-2 block">
            Ranked among 1,420 cohort nodes
          </span>
        </div>

        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
                Matched Openings
              </span>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="font-headline-md text-headline-md font-bold text-on-surface">14 Roles</span>
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-primary">
              <span className="material-symbols-outlined text-[20px]">explore</span>
            </div>
          </div>
          <span className="font-body-sm text-xs text-secondary font-semibold mt-3 border-t border-surface-container pt-2 block">
            &gt;90% Complementary Fit
          </span>
        </div>

        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
                Squad Invitations
              </span>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="font-headline-md text-headline-md font-bold text-secondary">3 Pending</span>
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[20px]">mail</span>
            </div>
          </div>
          <span className="font-body-sm text-xs text-on-surface-variant mt-3 border-t border-surface-container pt-2 block">
            Direct offers with equity allocations
          </span>
        </div>

        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex flex-col justify-between">
          <div className="flex items-start justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
                Active Sprint
              </span>
              <div className="flex items-baseline gap-2 mt-1">
                <span className="font-headline-md text-headline-md font-bold text-on-surface">Sprint #3</span>
              </div>
            </div>
            <div className="w-10 h-10 rounded-lg bg-surface-container flex items-center justify-center text-primary">
              <span className="material-symbols-outlined text-[20px]">timer</span>
            </div>
          </div>
          <span className="font-body-sm text-xs text-error font-semibold mt-3 border-t border-surface-container pt-2 block">
            18h 42m left on Clock
          </span>
        </div>
      </div>

      {/* Main Grid: Active Challenge vs Invitations Preview */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        {/* Left Column (8 cols): Current Live Challenge Card */}
        <div className="lg:col-span-8 flex flex-col gap-space-lg">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col gap-space-md border border-surface-container">
            <div className="flex items-center justify-between pb-3 border-b border-surface-container">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-secondary animate-pulse"></span>
                <span className="font-title-md text-title-md font-bold text-on-surface">
                  Active Challenge: Multi-Agent MicroVM Stress Test
                </span>
              </div>
              <span className="px-2.5 py-0.5 rounded-full bg-error-container text-on-error-container font-code-sm text-xs font-semibold">
                Ends in 18h 42m
              </span>
            </div>

            <p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">
              Design a low-latency scheduler pipeline in Rust/Go capable of handling 50,000 synthetic adversarial
              events with sub-5ms p99 latency. Your submission is sandboxed and scored against zero-knowledge tests.
            </p>

            <div className="p-4 rounded-xl bg-surface-container-low flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <span className="font-label-sm text-xs text-on-surface-variant block">Repository Linked</span>
                <span className="font-code-sm text-xs text-secondary font-mono">
                  github.com/elena-vance-dist/microvm-scheduler
                </span>
              </div>
              <button
                type="button"
                onClick={() => showToast('Triggered sandboxed test run on GitHub commit')}
                className="px-4 py-2 rounded-lg bg-primary-container text-on-primary font-label-md text-label-md font-semibold hover:bg-primary transition-all shadow-xs"
              >
                Trigger Sandboxed Run
              </button>
            </div>
          </div>
        </div>

        {/* Right Column (4 cols): Quick Invitations */}
        <div className="lg:col-span-4 flex flex-col gap-space-md">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col gap-space-md border border-surface-container">
            <div className="flex items-center justify-between pb-2 border-b border-surface-container">
              <h2 className="font-title-md text-title-md font-bold text-on-surface">Direct Squad Offers</h2>
              <span className="font-label-sm text-xs text-secondary font-bold">3 Offers</span>
            </div>

            <div className="space-y-3">
              <div className="p-3 rounded-lg bg-surface-container-low flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <span className="font-label-md text-body-md font-bold text-on-surface">Synthetix AI</span>
                  <span className="font-code-sm text-secondary font-bold">15.0% Equity</span>
                </div>
                <p className="font-body-sm text-xs text-on-surface-variant">Lead Distributed Systems Architect</p>
                <Link
                  to="/worker/invitations"
                  className="font-label-sm text-xs text-secondary font-semibold hover:underline mt-1"
                >
                  Inspect Offer Terms →
                </Link>
              </div>

              <div className="p-3 rounded-lg bg-surface-container-low flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <span className="font-label-md text-body-md font-bold text-on-surface">PolyMatrix AI</span>
                  <span className="font-code-sm text-secondary font-bold">12.0% Equity</span>
                </div>
                <p className="font-body-sm text-xs text-on-surface-variant">Systems Performance Lead</p>
                <Link
                  to="/worker/invitations"
                  className="font-label-sm text-xs text-secondary font-semibold hover:underline mt-1"
                >
                  Inspect Offer Terms →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
