import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export const WorkerSettings = () => {
  const { user, showToast } = useAuth();

  const [cloaked, setCloaked] = useState(true);
  const [phone, setPhone] = useState('+1 (555) 382-9014');
  const [whatsappSync, setWhatsappSync] = useState(true);
  const [githubUrl, setGithubUrl] = useState('https://github.com/elena-vance-dist');
  const [weeklyAvailability, setWeeklyAvailability] = useState('20');

  const handleSave = () => {
    showToast('Worker telemetry, anonymity shield, and WhatsApp integration preferences saved!');
  };

  return (
    <div className="px-space-lg py-space-lg max-w-[1440px] mx-auto w-full space-y-space-lg">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-space-md pb-space-lg">
        <div className="flex flex-col gap-space-xs">
          <nav className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wider">
            <span>Cohort Alpha '25</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span>Worker Portal</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-semibold">Account &amp; Protocol Settings</span>
          </nav>
          <div className="flex items-center gap-space-sm mt-1">
            <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              Worker Account &amp; Privacy Settings
            </h1>
            <span className="px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold uppercase tracking-wide">
              Shield v4.2
            </span>
          </div>
          <p className="font-body-md text-body-md text-on-surface-variant max-w-3xl">
            Configure your zero-bias anonymity shield, notification channels, development keys, and cohort participation
            preferences.
          </p>
        </div>

        <div className="flex items-center gap-space-sm shrink-0">
          <button
            type="button"
            onClick={handleSave}
            className="px-space-lg h-10 rounded-lg bg-secondary text-on-secondary hover:opacity-90 transition-all shadow-sm flex items-center gap-space-xs font-title-md text-title-md font-semibold"
          >
            <span className="material-symbols-outlined text-[18px]">check</span>
            <span>Save Changes</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Main Settings Sections */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          {/* Section 1: Anonymity Cloak */}
          <section className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-secondary text-[24px]">shield</span>
                <div>
                  <h2 className="font-title-md text-title-md font-bold text-on-surface">Zero-Bias Cloaking Shield</h2>
                  <p className="font-body-sm text-xs text-on-surface-variant">
                    Founders and syndicates only inspect your cryptographic code benchmarks and cognitive fit scores until mutual reveal.
                  </p>
                </div>
              </div>
              <label className="relative inline-flex items-center cursor-pointer shrink-0">
                <input
                  type="checkbox"
                  checked={cloaked}
                  onChange={(e) => setCloaked(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-surface-container-highest peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-secondary"></div>
              </label>
            </div>

            <div className="p-3.5 rounded-lg bg-surface-container-low flex justify-between items-center text-xs">
              <span className="text-on-surface-variant">Current Node Alias:</span>
              <span className="font-mono font-bold text-secondary">#{user?.nodeId || 'TX-5512B'} (CLOAKED)</span>
            </div>
          </section>

          {/* Section 2: WhatsApp Dispatch Screening */}
          <section className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-secondary text-[24px]">chat</span>
              <div>
                <h2 className="font-title-md text-title-md font-bold text-on-surface">
                  WhatsApp Challenge Screening Dispatch
                </h2>
                <p className="font-body-sm text-xs text-on-surface-variant">
                  Receive automated async challenge prompts and sprint reminders directly in chat.
                </p>
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-label-sm text-xs font-semibold text-on-surface">Phone Number for WhatsApp Dispatch</label>
              <input
                type="text"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="w-full h-10 px-3.5 rounded-lg bg-surface-container-low text-on-surface font-body-sm text-xs focus:outline-none focus:ring-1 focus:ring-secondary"
              />
            </div>

            <div className="flex items-center justify-between p-3 rounded-lg bg-surface-container-low text-xs">
              <span className="font-semibold text-on-surface">Allow Voice &amp; Audio Answer Submissions</span>
              <input
                type="checkbox"
                checked={whatsappSync}
                onChange={(e) => setWhatsappSync(e.target.checked)}
                className="w-4 h-4 accent-secondary cursor-pointer"
              />
            </div>
          </section>

          {/* Section 3: Linked Code Repositories */}
          <section className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-secondary text-[24px]">terminal</span>
              <div>
                <h2 className="font-title-md text-title-md font-bold text-on-surface">Linked Sandbox Repository</h2>
                <p className="font-body-sm text-xs text-on-surface-variant">
                  GitHub account linked for automated zero-knowledge code evaluation sandboxes.
                </p>
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-label-sm text-xs font-semibold text-on-surface">GitHub Profile / Proof of Work URL</label>
              <input
                type="url"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                className="w-full h-10 px-3.5 rounded-lg bg-surface-container-low text-on-surface font-body-sm text-xs focus:outline-none focus:ring-1 focus:ring-secondary"
              />
            </div>
          </section>
        </div>

        {/* Right Sidebar: Availability */}
        <div className="lg:col-span-4 flex flex-col gap-6">
          <div className="bg-surface-container-lowest rounded-xl p-6 shadow-sm flex flex-col gap-4 border border-surface-container">
            <h3 className="font-title-md text-title-md font-bold text-on-surface">Sprint Availability</h3>
            <div className="flex flex-col gap-1.5">
              <label className="font-label-sm text-xs text-on-surface-variant">Weekly Hours Committed:</label>
              <select
                value={weeklyAvailability}
                onChange={(e) => setWeeklyAvailability(e.target.value)}
                className="h-10 px-3 rounded-lg bg-surface-container-low text-on-surface font-semibold text-xs border border-surface-container focus:outline-none cursor-pointer"
              >
                <option value="10">10 hrs/week (Part-time exploration)</option>
                <option value="20">20 hrs/week (Active sprint cycle)</option>
                <option value="40">40+ hrs/week (Full-time founding squad)</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
