import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const WorkerInvitations = () => {
  const { showToast } = useAuth();
  const [activeTab, setActiveTab] = useState('pending');

  const [invites, setInvites] = useState([
    {
      id: 'inv_1',
      squad: 'Synthetix AI',
      role: 'Lead Distributed Systems Architect',
      equity: '15.0% Equity Grant',
      terms: '4-Year Vesting with 1-Year Cliff • Post-Money SAFE Protected',
      founder: 'Elena Vance (CEO)',
      message:
        'We reviewed your 50k TPS MicroVM benchmark submission and were blown away by your low-latency scheduler execution. We would love to have you as a founding team member to build out our high-throughput enterprise simulation stack.',
      status: 'pending',
      date: 'Today at 10:42 AM',
    },
    {
      id: 'inv_2',
      squad: 'PolyMatrix AI',
      role: 'High-Throughput Systems Core Engineer',
      equity: '12.0% Equity Grant',
      terms: 'Standard Founder Stock Agreement • Early Exercise Supported',
      founder: 'Dr. Aaron Meyer (CEO)',
      message:
        'Your background in distributed state synchronization fits perfectly with our continuous compliance simulation architecture.',
      status: 'pending',
      date: 'Yesterday at 3:15 PM',
    },
    {
      id: 'inv_3',
      squad: 'ChronoDB',
      role: 'Founding Storage Engine Architect',
      equity: '14.0% Equity Grant',
      terms: 'Delaware C-Corp Cap Table Slot • Series Pre-Seed',
      founder: 'Vikram Joshi (CEO)',
      message:
        'We are building the fastest vector storage engine for LLMs. Your zero-copy memory benchmarks match our exact technical roadmap requirements.',
      status: 'pending',
      date: '2 days ago',
    },
  ]);

  const handleAccept = (inv) => {
    setInvites(invites.map((i) => (i.id === inv.id ? { ...i, status: 'accepted' } : i)));
    showToast(`Congratulations! You accepted the offer from ${inv.squad}. Wired into Cap Table!`);
  };

  const handleDecline = (inv) => {
    setInvites(invites.map((i) => (i.id === inv.id ? { ...i, status: 'declined' } : i)));
    showToast(`Declined invitation from ${inv.squad}.`);
  };

  const filtered = invites.filter((i) => {
    if (activeTab === 'pending') return i.status === 'pending';
    if (activeTab === 'accepted') return i.status === 'accepted';
    return true;
  });

  return (
    <div className="relative w-full overflow-hidden px-margin py-space-lg max-w-[1440px] mx-auto space-y-space-lg">
      {/* Header */}
      <div className="flex flex-col gap-space-sm">
        <nav className="flex items-center gap-space-xs font-label-md text-label-md text-on-surface-variant">
          <span>Cohort Alpha '25</span>
          <span className="material-symbols-outlined text-[14px]">chevron_right</span>
          <span>Worker Portal</span>
          <span className="material-symbols-outlined text-[14px]">chevron_right</span>
          <span className="text-secondary font-semibold">Squad Invitations &amp; Offers</span>
        </nav>

        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-space-md">
          <div className="flex flex-col max-w-2xl">
            <div className="inline-flex items-center gap-2 mb-1.5">
              <span className="w-2 h-2 rounded-full bg-secondary"></span>
              <span className="font-label-sm text-label-sm text-secondary font-bold tracking-widest uppercase">
                Verified Talent Matcher
              </span>
            </div>
            <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              Team &amp; Squad Invitations
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant mt-1">
              Direct squad invitations from founders based on your verified sprint evaluations and rubric percentile.
            </p>
          </div>

          <div className="flex items-center gap-space-md bg-surface-container-lowest shadow-sm rounded-xl px-space-md py-space-sm self-start lg:self-auto border border-surface-container">
            <div className="w-10 h-10 rounded-lg bg-surface-container-low flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[22px]">verified_user</span>
            </div>
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider font-semibold">
                Rubric Score
              </span>
              <div className="flex items-baseline gap-1">
                <span className="font-headline-sm text-headline-sm text-on-surface font-bold">96.4</span>
                <span className="font-label-sm text-label-sm text-secondary font-semibold">/ Top 3%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-surface-container pb-2">
        <button
          onClick={() => setActiveTab('pending')}
          className={`px-4 py-2 rounded-lg font-label-md text-label-md font-semibold transition-all ${
            activeTab === 'pending'
              ? 'bg-primary-container text-on-primary'
              : 'text-on-surface-variant hover:bg-surface-container'
          }`}
        >
          Pending Offers ({invites.filter((i) => i.status === 'pending').length})
        </button>
        <button
          onClick={() => setActiveTab('accepted')}
          className={`px-4 py-2 rounded-lg font-label-md text-label-md font-semibold transition-all ${
            activeTab === 'accepted'
              ? 'bg-primary-container text-on-primary'
              : 'text-on-surface-variant hover:bg-surface-container'
          }`}
        >
          Accepted Squads ({invites.filter((i) => i.status === 'accepted').length})
        </button>
      </div>

      {/* Invitations List */}
      <div className="space-y-space-md">
        {filtered.length === 0 ? (
          <div className="p-8 text-center bg-surface-container-lowest rounded-xl text-on-surface-variant">
            No invitations in this view.
          </div>
        ) : (
          filtered.map((inv) => (
            <div
              key={inv.id}
              className="bg-surface-container-lowest rounded-xl p-6 shadow-sm hover:shadow-md transition-all flex flex-col gap-4 border border-surface-container"
            >
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-4 border-b border-surface-container">
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="font-headline-sm text-headline-sm font-bold text-on-surface">{inv.squad}</h2>
                    <span className="px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                      Official Offer
                    </span>
                  </div>
                  <span className="font-title-md text-title-md text-secondary font-bold">{inv.role}</span>
                  <p className="font-body-sm text-xs text-on-surface-variant mt-1">Invited by {inv.founder} • {inv.date}</p>
                </div>

                <div className="text-left sm:text-right">
                  <span className="font-headline-sm text-headline-sm font-bold text-on-surface block">
                    {inv.equity}
                  </span>
                  <span className="font-code-sm text-xs text-on-surface-variant">{inv.terms}</span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-surface-container-low font-body-md text-body-md text-on-surface italic">
                "{inv.message}"
              </div>

              {inv.status === 'pending' ? (
                <div className="flex flex-wrap items-center justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => handleDecline(inv)}
                    className="px-4 py-2 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-colors"
                  >
                    Decline
                  </button>
                  <button
                    type="button"
                    onClick={() => handleAccept(inv)}
                    className="px-5 py-2 rounded-lg bg-secondary text-on-secondary font-label-md text-label-md font-semibold hover:opacity-90 transition-all shadow-sm flex items-center gap-1.5"
                  >
                    <span className="material-symbols-outlined text-[18px]">check_circle</span>
                    <span>Accept Offer &amp; Join Cap Table</span>
                  </button>
                </div>
              ) : (
                <div className="flex items-center justify-end text-emerald-700 font-bold text-sm gap-1 pt-2">
                  <span className="material-symbols-outlined text-[18px]">check_circle</span>
                  <span>Joined Founding Squad</span>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
