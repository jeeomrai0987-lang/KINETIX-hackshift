import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const InvestorFinancialReport = () => {
  const { showToast } = useAuth();
  const [selectedEntity, setSelectedEntity] = useState('synthetix');

  return (
    <div className="flex flex-col w-full space-y-space-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider mb-1">
            <span>Investor Portal</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-semibold">Financial Reports</span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
            Verified Financial Telemetry &amp; Audits
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Quarterly attestation packs, verified ledger burn, and runway forecasts.
          </p>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <span className="font-label-md text-label-md text-outline">Entity:</span>
          <select
            value={selectedEntity}
            onChange={(e) => setSelectedEntity(e.target.value)}
            className="h-10 pl-3 pr-8 rounded-lg bg-surface-container-lowest text-on-surface font-label-md text-label-md font-semibold border border-surface-container shadow-sm focus:outline-none cursor-pointer"
          >
            <option value="synthetix">Synthetix AI (Selected)</option>
            <option value="polymatrix">PolyMatrix AI</option>
            <option value="kauri">Kauri Health</option>
            <option value="consolidated">Consolidated Portfolio View</option>
          </select>
        </div>
      </div>

      {/* Top 4 Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md">
        <div className="relative overflow-hidden rounded-xl bg-surface-container-lowest p-5 shadow-sm">
          <div className="flex items-center justify-between text-on-surface-variant mb-3">
            <span className="font-label-md text-label-md uppercase tracking-wider text-outline font-semibold">
              Monthly Burn Rate
            </span>
            <div className="w-8 h-8 rounded-lg bg-surface-container-low flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[18px]">trending_down</span>
            </div>
          </div>
          <div className="font-headline-lg text-headline-lg font-bold text-primary tracking-tight">
            -$14,800
          </div>
          <div className="mt-2.5 flex items-center gap-2 text-on-surface-variant font-body-sm text-body-sm">
            <span className="px-2 py-0.5 rounded bg-emerald-50 text-emerald-800 font-label-sm text-label-sm font-semibold">
              -4.2% MoM
            </span>
            <span>Audit confirmed</span>
          </div>
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-surface-container-high"></div>
        </div>

        <div className="relative overflow-hidden rounded-xl bg-surface-container-lowest p-5 shadow-sm">
          <div className="flex items-center justify-between text-on-surface-variant mb-3">
            <span className="font-label-md text-label-md uppercase tracking-wider text-outline font-semibold">
              Current Treasury Balance
            </span>
            <div className="w-8 h-8 rounded-lg bg-surface-container-low flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[18px]">account_balance</span>
            </div>
          </div>
          <div className="font-headline-lg text-headline-lg font-bold text-primary tracking-tight">
            $242,500
          </div>
          <div className="mt-2.5 flex items-center gap-2 text-on-surface-variant font-body-sm text-body-sm">
            <span className="px-2 py-0.5 rounded bg-surface-container text-primary font-label-sm text-label-sm font-semibold">
              FDIC Insured
            </span>
            <span>SVB Verified</span>
          </div>
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-surface-container-high"></div>
        </div>

        <div className="relative overflow-hidden rounded-xl bg-surface-container-lowest p-5 shadow-sm">
          <div className="flex items-center justify-between text-on-surface-variant mb-3">
            <span className="font-label-md text-label-md uppercase tracking-wider text-outline font-semibold">
              Net Runway
            </span>
            <div className="w-8 h-8 rounded-lg bg-surface-container-low flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[18px]">timelapse</span>
            </div>
          </div>
          <div className="font-headline-lg text-headline-lg font-bold text-secondary tracking-tight">
            16.4 Mos
          </div>
          <div className="mt-2.5 flex items-center gap-2 text-on-surface-variant font-body-sm text-body-sm">
            <span className="px-2 py-0.5 rounded bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
              Healthy
            </span>
            <span>Through Q1 2027</span>
          </div>
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-surface-container-high"></div>
        </div>

        <div className="relative overflow-hidden rounded-xl bg-surface-container-lowest p-5 shadow-sm">
          <div className="flex items-center justify-between text-on-surface-variant mb-3">
            <span className="font-label-md text-label-md uppercase tracking-wider text-outline font-semibold">
              Next Scheduled Audit
            </span>
            <div className="w-8 h-8 rounded-lg bg-surface-container-low flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined text-[18px]">event</span>
            </div>
          </div>
          <div className="font-headline-lg text-headline-lg font-bold text-primary tracking-tight">
            Nov 30, 2025
          </div>
          <div className="mt-2.5 flex items-center gap-2 text-on-surface-variant font-body-sm text-body-sm">
            <span className="px-2 py-0.5 rounded bg-surface-container text-primary font-label-sm text-label-sm font-semibold">
              Q4 Mid-Term
            </span>
            <span>Attestation lock</span>
          </div>
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary-container to-secondary"></div>
        </div>
      </div>

      {/* Main Workspace Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column (8 cols): Financial Analytics */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          <div className="rounded-xl bg-surface-container-lowest p-6 shadow-sm flex flex-col gap-5 border border-surface-container">
            <div className="flex items-center justify-between pb-4 border-b border-surface-container">
              <div>
                <h2 className="font-title-md text-title-md font-bold text-on-surface">Revenue vs. Burn Progression</h2>
                <p className="font-body-sm text-body-sm text-on-surface-variant">
                  Monthly financial telemetry verified via linked banking APIs
                </p>
              </div>
              <span className="font-code-sm text-code-sm text-secondary font-semibold">
                Merkle Root Validated
              </span>
            </div>

            {/* Trajectory comparison bars */}
            <div className="w-full h-48 flex items-end justify-between gap-3 px-2 pt-4">
              {[
                { m: 'May', r: 10, b: 70 },
                { m: 'Jun', r: 15, b: 72 },
                { m: 'Jul', r: 22, b: 76 },
                { m: 'Aug', r: 28, b: 78 },
                { m: 'Sep', r: 35, b: 80 },
                { m: 'Oct', r: 45, b: 82 },
              ].map((item) => (
                <div key={item.m} className="flex flex-col items-center flex-1 h-full justify-end gap-1">
                  <div className="w-full flex items-end justify-center gap-1.5 h-36">
                    <div className="w-3 bg-secondary rounded-t" style={{ height: `${item.r}%` }}></div>
                    <div className="w-3 bg-primary-container rounded-t" style={{ height: `${item.b}%` }}></div>
                  </div>
                  <span className="font-code-sm text-xs text-on-surface-variant">{item.m}</span>
                </div>
              ))}
            </div>

            <div className="flex items-center justify-center gap-6 pt-3 border-t border-surface-container font-label-sm text-label-sm">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-secondary"></span>
                <span>Monthly Recurring Revenue</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-primary-container"></span>
                <span>Operating Burn</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column (4 cols): Attestation Packs & Downloads */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
            <h3 className="font-title-md text-title-md font-bold text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-secondary">description</span>
              Quarterly Attestation Packs
            </h3>
            <div className="space-y-3 font-body-sm text-body-sm">
              <div className="p-3 rounded-lg bg-surface-container-low flex justify-between items-center">
                <div>
                  <div className="font-semibold text-on-surface">Q3 2025 Attestation Pack</div>
                  <div className="font-code-sm text-xs text-on-surface-variant">SHA-256 Verified • PDF</div>
                </div>
                <button
                  type="button"
                  onClick={() => showToast('Downloading Q3 2025 Attestation Pack')}
                  className="text-secondary hover:text-on-secondary-container"
                >
                  <span className="material-symbols-outlined text-[20px]">download</span>
                </button>
              </div>

              <div className="p-3 rounded-lg bg-surface-container-low flex justify-between items-center">
                <div>
                  <div className="font-semibold text-on-surface">Form 1065 &amp; Delaware K-1s</div>
                  <div className="font-code-sm text-xs text-on-surface-variant">Signed by CPA • ZIP</div>
                </div>
                <button
                  type="button"
                  onClick={() => showToast('Downloading Tax Disclosures')}
                  className="text-secondary hover:text-on-secondary-container"
                >
                  <span className="material-symbols-outlined text-[20px]">download</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
