import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const WorkerProfile = () => {
  const { user, showToast } = useAuth();
  const [cloaked, setCloaked] = useState(true);

  const skills = [
    { name: 'Distributed Systems Architecture', level: 'Top 1% (Score 98/100)', verified: true },
    { name: 'Rust & Low-Level Memory Management', level: 'Top 2% (Score 96/100)', verified: true },
    { name: 'Consensus Engines (Raft, Paxos, PBFT)', level: 'Top 4% (Score 94/100)', verified: true },
    { name: 'MicroVM Isolation & Linux eBPF', level: 'Top 5% (Score 92/100)', verified: true },
    { name: 'Zero-Knowledge Cryptographic Proofs', level: 'Top 8% (Score 88/100)', verified: true },
  ];

  return (
    <div className="w-full max-w-[1440px] mx-auto px-margin-mobile md:px-margin py-space-lg space-y-space-lg">
      {/* Breadcrumbs */}
      <nav className="flex items-center gap-space-xs text-on-surface-variant font-label-md text-label-md">
        <span>Cohort Alpha '25</span>
        <span className="material-symbols-outlined text-[16px]">chevron_right</span>
        <span>Worker Portal</span>
        <span className="material-symbols-outlined text-[16px]">chevron_right</span>
        <span className="text-on-surface font-semibold">My Profile &amp; Verified Dossier</span>
      </nav>

      {/* Header Executive Banner Card */}
      <section className="relative bg-surface-container-lowest rounded-xl p-space-lg shadow-sm overflow-hidden border border-surface-container">
        <div className="flex flex-col xl:flex-row items-start xl:items-center justify-between gap-space-lg">
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-space-md">
            <div className="relative">
              <div className="w-20 h-20 rounded-xl overflow-hidden shadow-sm bg-primary-container flex items-center justify-center">
                <img
                  className="w-full h-full object-cover"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuAXDAn8ZFbqaXgUtAZFPSAMimDjdAoYUtHj9L77g4tSh_dzBGXy6q7ARHBvvPaEiQBevjgoVWtUl1CPRgJcoZ_Gyr1x8Zo7gNTBlUQObPUZdavCilarTN6yVjeMbRs58962jPDHojUKOmZ_bPn3g6RPFzhAkTcS32gCbsLDrLoGoPt23xW2bo98EiFz6_G89_dt-TciA5PCjPGcobNbxFBrua1O80BXj8xC1JSaqoZGvJJLCVcC2Qyt0g"
                  alt="Avatar"
                />
              </div>
              <span className="absolute -bottom-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-secondary text-on-secondary shadow-sm">
                <span className="material-symbols-outlined text-[12px]">verified_user</span>
              </span>
            </div>

            <div className="flex flex-col">
              <div className="flex flex-wrap items-center gap-space-xs">
                <h1 className="font-headline-md text-headline-md text-on-surface tracking-tight font-bold">
                  {user?.name || 'Alex Mercer'}
                </h1>
                <span className="font-code-sm text-code-sm px-2 py-0.5 rounded-full bg-surface-container text-on-surface font-semibold">
                  Node #{user?.nodeId || 'TX-5512B'}
                </span>
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                  <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
                  Tier A Candidate
                </span>
              </div>
              <p className="font-body-md text-body-md text-on-surface-variant mt-1 flex flex-wrap items-center gap-x-3 gap-y-1">
                <span className="text-secondary font-medium">Available for 20 hrs/week</span>
                <span>•</span>
                <span>Remote • UTC-5 (Eastern)</span>
                <span>•</span>
                <span className="font-medium text-on-surface">82% Profile Strength</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => {
                setCloaked(!cloaked);
                showToast(`Zero-bias identity cloaking ${!cloaked ? 'ENABLED' : 'PAUSED'}`);
              }}
              className="px-4 py-2 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-all flex items-center gap-1.5"
            >
              <span className="material-symbols-outlined text-[18px]">
                {cloaked ? 'visibility_off' : 'visibility'}
              </span>
              <span>{cloaked ? 'Cloaking Active' : 'Public Mode'}</span>
            </button>
            <button
              type="button"
              onClick={() => showToast('Portable credential verified and exported')}
              className="px-4 py-2 rounded-lg bg-primary-container text-on-primary font-label-md text-label-md font-semibold hover:bg-primary transition-all shadow-xs flex items-center gap-1.5"
            >
              <span className="material-symbols-outlined text-[18px]">badge</span>
              <span>Export Credential</span>
            </button>
          </div>
        </div>
      </section>

      {/* Verified Skills Grid */}
      <section className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col gap-space-md border border-surface-container">
        <div className="flex items-center justify-between pb-2 border-b border-surface-container">
          <div>
            <h2 className="font-title-md text-title-md font-bold text-on-surface">
              Verified Technical Competencies &amp; Challenge Scores
            </h2>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              Cryptographically audited through live sandboxed cohort sprint challenges
            </p>
          </div>
          <span className="px-2.5 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
            5 Attested Badges
          </span>
        </div>

        <div className="space-y-3">
          {skills.map((s, idx) => (
            <div
              key={idx}
              className="p-3.5 rounded-lg bg-surface-container-low flex flex-col sm:flex-row sm:items-center justify-between gap-2"
            >
              <div className="flex items-center gap-2.5">
                <span className="material-symbols-outlined text-secondary text-[20px]">verified</span>
                <span className="font-title-md text-body-md font-bold text-on-surface">{s.name}</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="font-code-sm text-xs text-secondary font-bold">{s.level}</span>
                <span className="px-2 py-0.5 rounded bg-surface-container-highest text-on-surface font-label-sm text-xs font-semibold">
                  Zero-Knowledge Proof
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};
