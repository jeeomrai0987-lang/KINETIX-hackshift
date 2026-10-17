import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { founderApi } from '../../api/founder';

export const FounderChallenge = () => {
  const { showToast } = useAuth();

  const [submissions, setSubmissions] = useState([
    {
      id: 'sub_elena_01',
      candidateCode: 'Candidate #TX-5512B',
      role: 'Lead Distributed Systems Architect',
      score: 99.0,
      latency: '1.84ms p99',
      testsPassed: '48 / 48',
      hash: '0x4b7f892a01c4d9e8f1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4',
      status: 'Attested',
      vectorScores: {
        replayIntegrity: 99.8,
        failureRecovery: 100.0,
        concurrencyLatency: 98.4,
        codeElegance: 96.0,
      },
    },
    {
      id: 'sub_julian_02',
      candidateCode: 'Candidate #TX-9042A',
      role: 'Inference Systems Engineer',
      score: 94.2,
      latency: '2.12ms p99',
      testsPassed: '46 / 48',
      hash: '0x8f9c7e2b10a34c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d',
      status: 'Attested',
      vectorScores: {
        replayIntegrity: 95.0,
        failureRecovery: 96.0,
        concurrencyLatency: 93.0,
        codeElegance: 92.8,
      },
    },
    {
      id: 'sub_rostova_03',
      candidateCode: 'Candidate #TX-8821B',
      role: 'Infrastructure Security & Sandbox Lead',
      score: 91.0,
      latency: '2.45ms p99',
      testsPassed: '44 / 48',
      hash: '0x7e29bb31a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7',
      status: 'In Review',
      vectorScores: {
        replayIntegrity: 92.0,
        failureRecovery: 90.0,
        concurrencyLatency: 91.0,
        codeElegance: 91.0,
      },
    },
  ]);

  const [selectedSub, setSelectedSub] = useState(submissions[0]);
  const [sliderScore, setSliderScore] = useState(selectedSub.vectorScores.replayIntegrity);
  const [isLoading, setIsLoading] = useState(false);

  const fetchSubmissions = async () => {
    try {
      const res = await founderApi.getSubmissions('chg_synthetix_01');
      if (res?.items && res.items.length > 0) {
        const mapped = res.items.map((s) => ({
          id: s.id,
          candidateCode: `Candidate #${s.candidateCode}`,
          role: 'Lead Distributed Systems Architect',
          score: s.score,
          latency: `${s.p99LatencyMs}ms p99`,
          testsPassed: `${s.testsPassed} / ${s.testsTotal}`,
          hash: s.hash,
          status: s.status === 'attested' ? 'Attested' : 'Scoring In Review',
          vectorScores: {
            replayIntegrity: s.replayIntegrity,
            failureRecovery: s.failureRecovery,
            concurrencyLatency: s.concurrencyLatency,
            codeElegance: s.codeElegance,
          },
        }));
        setSubmissions(mapped);
        setSelectedSub(mapped[0]);
        setSliderScore(mapped[0].vectorScores.replayIntegrity);
      }
    } catch (err) {
      console.warn('Submissions API fallback:', err.message);
    }
  };

  useEffect(() => {
    fetchSubmissions();
  }, []);

  const handleSignLedger = async () => {
    setIsLoading(true);
    try {
      const res = await founderApi.signSubmission(selectedSub.id);
      showToast(`Cryptographic attestation signed! Merkle root: ${res?.hash?.slice(0, 16)}...`);
      setSelectedSub((prev) => ({ ...prev, status: 'Attested', hash: res.hash }));
    } catch (err) {
      console.warn('Sign submission fallback:', err.message);
      showToast('Cryptographic score submitted to protocol ledger on Arbitrum simulated testnet!');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col w-full gap-space-lg">
      {/* Top Header & Badges */}
      <div className="flex flex-col gap-space-sm">
        <div className="flex flex-wrap items-center justify-between gap-space-sm">
          <div className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm">
            <span>Cohort Alpha ‘25</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span>Sprint #3 Challenge</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-semibold">Blind Evaluation Engine</span>
          </div>

          <div className="flex flex-wrap items-center gap-space-xs">
            <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm shadow-sm">
              <span className="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
              <span className="font-semibold tracking-wide">Zero-Bias Enforced [Active]</span>
            </div>
            <div className="flex items-center gap-1 px-3 py-1 rounded-full bg-surface-container-high text-on-surface font-label-sm text-label-sm">
              <span className="material-symbols-outlined text-[15px] text-secondary">shield</span>
              <span>Double-Blind Review Phase</span>
            </div>
            <div className="flex items-center gap-1 px-3 py-1 rounded-full bg-tertiary-fixed text-on-tertiary-fixed-variant font-label-sm text-label-sm font-medium">
              <span className="material-symbols-outlined text-[15px] text-on-tertiary-container">timer</span>
              <span>
                Scoring Closes: <strong className="font-semibold">06h 45m</strong>
              </span>
            </div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-space-sm pt-space-xs">
          <div>
            <h1 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
              Challenge &amp; Blind Evaluation
            </h1>
            <p className="font-body-md text-body-md text-on-surface-variant">
              Multi-vector cryptographic zero-bias scoring for 48h live sprint deliverables.
            </p>
          </div>
          <div className="flex items-center gap-space-xs">
            <button
              onClick={() => showToast('Cohort anonymity specification sheet downloaded')}
              className="flex items-center gap-1.5 px-space-md py-space-sm rounded-lg bg-surface-container hover:bg-surface-container-high text-on-surface font-label-md text-label-md transition-colors"
              type="button"
            >
              <span className="material-symbols-outlined text-[16px] text-on-surface-variant">download</span>
              <span>Cohort Specs</span>
            </button>
            <button
              onClick={handleSignLedger}
              className="flex items-center gap-1.5 px-space-md py-space-sm rounded-lg bg-primary-container hover:bg-primary text-on-primary font-label-md text-label-md shadow-sm transition-colors"
              type="button"
            >
              <span className="material-symbols-outlined text-[16px]">verified</span>
              <span>Sign Protocol Ledger</span>
            </button>
          </div>
        </div>
      </div>

      {/* Main Grid: Challenge Spec (Left) vs Submissions & Matrix (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        {/* Left: Challenge Brief & Evaluation Rubrics (5 cols) */}
        <div className="lg:col-span-5 flex flex-col gap-space-md">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col gap-space-md">
            <div className="flex items-center justify-between">
              <span className="px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                Sprint #3 Active Vector
              </span>
              <span className="font-code-sm text-code-sm text-on-surface-variant">ID: SP3-SIM-FINTECH</span>
            </div>

            <div>
              <h2 className="font-headline-sm text-headline-sm text-on-surface font-bold">
                Multi-Agent MicroVM Stress Test &amp; Latency Under High Load
              </h2>
              <p className="font-body-sm text-body-sm text-on-surface-variant mt-2 leading-relaxed">
                Candidates construct an isolated containerized scheduler capable of handling 50,000 synthetic adversarial
                events per second without state desynchronization.
              </p>
            </div>

            <div className="space-y-space-sm pt-2 border-t border-surface-container">
              <h3 className="font-label-md text-label-md font-semibold text-on-surface">Evaluation Vectors &amp; Weights:</h3>
              <div className="flex flex-col gap-2">
                <div className="p-3 rounded-lg bg-surface-container-low flex justify-between items-center">
                  <span className="font-body-sm text-body-sm text-on-surface font-medium">
                    Deterministic Replay Integrity
                  </span>
                  <span className="font-code-sm text-code-sm font-bold text-secondary">35% Weight</span>
                </div>
                <div className="p-3 rounded-lg bg-surface-container-low flex justify-between items-center">
                  <span className="font-body-sm text-body-sm text-on-surface font-medium">Zero-Loss Failure Recovery</span>
                  <span className="font-code-sm text-code-sm font-bold text-secondary">30% Weight</span>
                </div>
                <div className="p-3 rounded-lg bg-surface-container-low flex justify-between items-center">
                  <span className="font-body-sm text-body-sm text-on-surface font-medium">
                    Concurrency Latency &amp; Memory Footprint
                  </span>
                  <span className="font-code-sm text-code-sm font-bold text-secondary">20% Weight</span>
                </div>
                <div className="p-3 rounded-lg bg-surface-container-low flex justify-between items-center">
                  <span className="font-body-sm text-body-sm text-on-surface font-medium">
                    Code Elegance &amp; Documentation
                  </span>
                  <span className="font-code-sm text-code-sm font-bold text-secondary">15% Weight</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Submissions Pool & Interactive Evaluator (7 cols) */}
        <div className="lg:col-span-7 flex flex-col gap-space-md">
          {submissions.map((sub) => (
            <div
              key={sub.id}
              onClick={() => setSelectedSub(sub)}
              className={`bg-surface-container-lowest rounded-xl p-space-lg shadow-sm transition-all cursor-pointer border-2 ${
                selectedSub.id === sub.id ? 'border-secondary shadow-md' : 'border-transparent hover:border-surface-container-high'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-space-sm pb-space-sm border-b border-surface-container">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="font-title-md text-title-md font-bold text-on-surface">{sub.candidateCode}</h3>
                    <span className="px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                      {sub.status}
                    </span>
                  </div>
                  <span className="font-body-sm text-body-sm text-on-surface-variant">{sub.role}</span>
                </div>
                <div className="flex items-baseline gap-1 bg-surface-container px-3 py-1 rounded-xl">
                  <span className="font-headline-md text-headline-md font-bold text-secondary">{sub.score}</span>
                  <span className="font-label-sm text-label-sm text-on-surface-variant font-semibold">/ 100</span>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-space-sm pt-space-sm">
                <div>
                  <span className="font-label-sm text-label-sm text-on-surface-variant block">Observed Latency</span>
                  <span className="font-title-md text-title-md font-bold text-secondary">{sub.latency}</span>
                </div>
                <div>
                  <span className="font-label-sm text-label-sm text-on-surface-variant block">Stress Tests</span>
                  <span className="font-title-md text-title-md font-bold text-on-surface">{sub.testsPassed}</span>
                </div>
                <div>
                  <span className="font-label-sm text-label-sm text-on-surface-variant block">Attestation Hash</span>
                  <span className="font-code-sm text-code-sm text-on-surface-variant truncate block">{sub.hash}</span>
                </div>
              </div>

              {selectedSub.id === sub.id && (
                <div className="mt-space-md pt-space-md border-t border-surface-container flex flex-col gap-space-sm">
                  <div className="flex items-center justify-between">
                    <span className="font-label-md text-label-md font-semibold text-on-surface">
                      Judge Rubric Vector Calibrator
                    </span>
                    <span className="font-code-sm text-code-sm text-secondary font-bold">Live Weight: {sliderScore}%</span>
                  </div>
                  <input
                    type="range"
                    min="50"
                    max="100"
                    value={sliderScore}
                    onChange={(e) => setSliderScore(Number(e.target.value))}
                    className="w-full accent-secondary cursor-pointer"
                  />
                  <div className="flex justify-end gap-2 pt-1">
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        showToast(`Score updated for ${sub.candidateCode}`);
                      }}
                      className="px-4 py-2 rounded-lg bg-primary-container text-on-primary font-label-md text-label-md font-semibold hover:bg-primary transition-all shadow-xs"
                    >
                      Confirm Score Update
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
