import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const InvestorInvestmentTerms = () => {
  const { showToast } = useAuth();
  const [filterType, setFilterType] = useState('all');

  const instruments = [
    {
      id: 'inst_1',
      entity: 'Synthetix AI',
      type: 'safe',
      typeLabel: 'Post-Money SAFE (with MFN & Pro-Rata Side Letter)',
      principal: '$200,000 USD',
      valCap: '$10,000,000',
      discount: '20%',
      equity: '2.0%',
      contractAddr: '0x892a...c01',
      dateSigned: 'Oct 04, 2025',
      status: 'Verified & Notarized',
    },
    {
      id: 'inst_2',
      entity: 'PolyMatrix AI',
      type: 'safe',
      typeLabel: 'Post-Money SAFE (Y-Combinator Standard Format)',
      principal: '$150,000 USD',
      valCap: '$8,000,000',
      discount: '20%',
      equity: '1.875%',
      contractAddr: '0x33e1...9f12',
      dateSigned: 'Aug 18, 2025',
      status: 'Verified & Notarized',
    },
    {
      id: 'inst_3',
      entity: 'Kauri Health',
      type: 'grant',
      typeLabel: 'Grant Token Warrant & Side Letter',
      principal: '$75,000 USD',
      valCap: '$5,000,000',
      discount: '15%',
      equity: '1.5%',
      contractAddr: '0x77c2...e881',
      dateSigned: 'Jun 22, 2025',
      status: 'Verified & Notarized',
    },
  ];

  const filtered =
    filterType === 'all'
      ? instruments
      : instruments.filter((i) => i.type === filterType);

  return (
    <div className="flex flex-col w-full space-y-space-lg">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider mb-1">
            <span>Investor Portal</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-semibold">Investment Terms</span>
          </div>
          <h1 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
            Investment Terms &amp; Legal Instruments
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Standardized post-money SAFEs, side letters, and notarized equity instruments.
          </p>
        </div>

        <button
          type="button"
          onClick={() => showToast('Full legal instruments archive ZIP generated')}
          className="h-10 px-4 rounded-lg bg-primary-container text-on-primary font-title-md text-title-md font-semibold hover:bg-primary transition-all shadow-sm flex items-center gap-2 self-start sm:self-auto"
        >
          <span className="material-symbols-outlined text-[18px]">folder_zip</span>
          <span>Download All Agreements</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-surface-container-lowest p-3 rounded-xl shadow-sm">
        <div className="flex items-center gap-1">
          {[
            { id: 'all', label: 'All Instruments (3)' },
            { id: 'safe', label: 'SAFEs (2)' },
            { id: 'grant', label: 'Grants & Warrants (1)' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setFilterType(tab.id)}
              className={`px-4 py-2 rounded-lg font-label-md text-label-md font-semibold transition-all ${
                filterType === tab.id
                  ? 'bg-primary text-on-primary shadow-xs'
                  : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
        <span className="font-code-sm text-xs text-on-surface-variant px-3">
          SEC Rule 506(c) Compliant
        </span>
      </div>

      {/* Cards List */}
      <div className="space-y-space-md">
        {filtered.map((item) => (
          <div
            key={item.id}
            className="bg-surface-container-lowest rounded-xl p-6 shadow-sm hover:shadow-md transition-all border border-surface-container"
          >
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-surface-container">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-surface-container-low flex items-center justify-center text-primary shrink-0 shadow-sm">
                  <span className="material-symbols-outlined text-[26px]">description</span>
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-headline-sm text-headline-sm text-on-surface font-bold">{item.entity}</h3>
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-secondary-container/50 text-on-secondary-container font-label-sm text-label-sm font-semibold">
                      <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
                      {item.status}
                    </span>
                  </div>
                  <p className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">{item.typeLabel}</p>
                </div>
              </div>

              <div className="text-left sm:text-right">
                <span className="font-label-sm text-label-sm text-outline uppercase font-semibold">
                  Invested Principal
                </span>
                <div className="font-headline-sm text-headline-sm text-on-surface font-bold">{item.principal}</div>
              </div>
            </div>

            {/* Strip */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-xl bg-surface-container-low/60 my-4">
              <div>
                <span className="font-label-sm text-xs text-outline block">Valuation Cap</span>
                <span className="font-title-md text-title-md text-on-surface font-bold">{item.valCap}</span>
              </div>
              <div>
                <span className="font-label-sm text-xs text-outline block">Discount Rate</span>
                <span className="font-title-md text-title-md text-on-surface font-bold">{item.discount}</span>
              </div>
              <div>
                <span className="font-label-sm text-xs text-outline block">Ownership Equivalent</span>
                <span className="font-title-md text-title-md text-secondary font-bold">{item.equity}</span>
              </div>
              <div>
                <span className="font-label-sm text-xs text-outline block">Date Signed</span>
                <span className="font-title-md text-title-md text-on-surface font-bold">{item.dateSigned}</span>
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-between gap-4 pt-1">
              <span className="font-code-sm text-xs text-on-surface-variant font-mono">
                Smart Contract: <strong className="text-secondary">{item.contractAddr}</strong>
              </span>
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => showToast(`Smart contract verified on Arbitrum: ${item.contractAddr}`)}
                  className="px-3.5 py-1.5 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-colors flex items-center gap-1"
                >
                  <span className="material-symbols-outlined text-[16px]">verified</span>
                  <span>Verify On-Chain</span>
                </button>
                <button
                  type="button"
                  onClick={() => showToast(`Downloading executed SAFE agreement PDF for ${item.entity}`)}
                  className="px-3.5 py-1.5 rounded-lg bg-primary-container text-on-primary font-label-md text-label-md font-semibold hover:bg-primary transition-all flex items-center gap-1 shadow-xs"
                >
                  <span className="material-symbols-outlined text-[16px]">download</span>
                  <span>Download SAFE (PDF)</span>
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
