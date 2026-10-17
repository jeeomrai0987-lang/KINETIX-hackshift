import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const InvestorSettings = () => {
  const { showToast } = useAuth();

  const [sectors, setSectors] = useState(['FinTech & AI', 'Distributed Systems', 'HealthTech', 'DevTools']);
  const [newSector, setNewSector] = useState('');
  const [walletAddr, setWalletAddr] = useState('0x88f2190A2bEE9481cFA42099C4E5512B');
  const [instantAlerts, setInstantAlerts] = useState(true);
  const [weeklyDigest, setWeeklyDigest] = useState(true);

  const handleAddSector = () => {
    if (newSector.trim() && !sectors.includes(newSector.trim())) {
      setSectors([...sectors, newSector.trim()]);
      setNewSector('');
    }
  };

  const handleRemoveSector = (sec) => {
    setSectors(sectors.filter((s) => s !== sec));
  };

  const handleSave = () => {
    showToast('Investor preferences and wallet telemetry saved successfully');
  };

  return (
    <div className="flex flex-col w-full space-y-space-lg max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
            Investor Account &amp; Syndicate Settings
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Manage SEC compliance status, notification triggers, and Web3 attestation vaults.
          </p>
        </div>
        <button
          type="button"
          onClick={handleSave}
          className="h-10 px-5 rounded-lg bg-secondary text-on-secondary font-title-md text-title-md font-semibold hover:opacity-90 transition-all shadow-sm flex items-center gap-1.5 self-start sm:self-auto"
        >
          <span className="material-symbols-outlined text-[18px]">check</span>
          <span>Save Changes</span>
        </button>
      </div>

      {/* Section 1: Accreditation Status */}
      <section className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
        <h2 className="font-title-md text-title-md font-bold text-on-surface flex items-center gap-2">
          <span className="material-symbols-outlined text-secondary">verified</span>
          Accreditation &amp; Compliance Status
        </h2>

        <div className="p-3.5 rounded-lg bg-surface-container-low flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <p className="font-title-md text-body-md text-on-surface font-semibold">
              Accredited Investor &amp; Qualified Purchaser
            </p>
            <p className="font-body-sm text-xs text-on-surface-variant">
              Validated through VentureForge SEC Rule 506(c) Protocol • Expires Nov 2026
            </p>
          </div>
          <button
            type="button"
            onClick={() => showToast('Re-certification request submitted to compliance officer')}
            className="px-3 py-1.5 rounded-lg bg-surface-container-high text-on-surface font-label-sm text-xs font-semibold self-start sm:self-auto"
          >
            Re-Certify
          </button>
        </div>

        {/* Sectors */}
        <div className="flex flex-col gap-2 pt-2">
          <label className="font-label-sm text-xs uppercase tracking-wider text-on-surface-variant font-semibold">
            Preferred Cohort Sectors
          </label>
          <div className="flex flex-wrap gap-2">
            {sectors.map((sec) => (
              <span
                key={sec}
                className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary-container text-on-primary font-label-sm text-xs font-medium"
              >
                <span>{sec}</span>
                <span
                  onClick={() => handleRemoveSector(sec)}
                  className="material-symbols-outlined text-[14px] cursor-pointer hover:opacity-75"
                >
                  close
                </span>
              </span>
            ))}
          </div>

          <div className="flex items-center gap-2 mt-2">
            <input
              type="text"
              placeholder="Add sector..."
              value={newSector}
              onChange={(e) => setNewSector(e.target.value)}
              className="h-9 px-3 rounded-lg bg-surface-container-low font-body-sm text-xs text-on-surface placeholder:text-outline focus:outline-none"
            />
            <button
              type="button"
              onClick={handleAddSector}
              className="h-9 px-3 rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-label-sm text-xs font-semibold"
            >
              Add Sector
            </button>
          </div>
        </div>
      </section>

      {/* Section 2: Notifications */}
      <section className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
        <h2 className="font-title-md text-title-md font-bold text-on-surface flex items-center gap-2">
          <span className="material-symbols-outlined text-secondary">notifications</span>
          Notification &amp; Reporting Channels
        </h2>

        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-lg bg-surface-container-low">
            <div>
              <p className="font-semibold text-on-surface text-body-md">Instant Milestone Alerts (WhatsApp &amp; SMS)</p>
              <p className="font-body-sm text-xs text-on-surface-variant">
                Direct ping when portfolio ventures achieve verified sprint deliverables.
              </p>
            </div>
            <input
              type="checkbox"
              checked={instantAlerts}
              onChange={(e) => setInstantAlerts(e.target.checked)}
              className="w-5 h-5 accent-secondary cursor-pointer"
            />
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg bg-surface-container-low">
            <div>
              <p className="font-semibold text-on-surface text-body-md">Weekly Syndicate Digest (Email)</p>
              <p className="font-body-sm text-xs text-on-surface-variant">
                Consolidated report covering burn changes, new recruits, and valuation adjustments.
              </p>
            </div>
            <input
              type="checkbox"
              checked={weeklyDigest}
              onChange={(e) => setWeeklyDigest(e.target.checked)}
              className="w-5 h-5 accent-secondary cursor-pointer"
            />
          </div>
        </div>
      </section>

      {/* Section 3: Web3 Vault Address */}
      <section className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
        <h2 className="font-title-md text-title-md font-bold text-on-surface flex items-center gap-2">
          <span className="material-symbols-outlined text-secondary">account_balance_wallet</span>
          Syndicate Attestation Multi-Sig Vault
        </h2>
        <div className="flex flex-col gap-1.5">
          <label className="font-label-sm text-xs text-on-surface-variant font-semibold">
            Arbitrum One Multi-Sig Vault Address
          </label>
          <input
            type="text"
            value={walletAddr}
            onChange={(e) => setWalletAddr(e.target.value)}
            className="w-full h-10 px-3.5 rounded-lg bg-surface-container-low text-on-surface font-code-sm text-xs font-mono focus:outline-none focus:ring-1 focus:ring-secondary"
          />
          <span className="font-body-sm text-xs text-on-surface-variant">
            Used for signing automated SAFE token warrants and receiving Merkle root hash certificates.
          </span>
        </div>
      </section>
    </div>
  );
};
