import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { founderApi } from '../../api/founder';

export const FounderProofWork = () => {
  const { showToast } = useAuth();
  const [proofData, setProofData] = useState({
    hash: '0x4b7f892a01c4d9e8f1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4',
    candidateCode: 'TX-5512B',
    score: 99,
    testsPassed: 48,
    testsTotal: 48,
    p99LatencyMs: 1.84,
    reviewerVerdict: 'Cryptographically signed by automated zero-bias test harness.',
    sprintName: 'Sprint 3 / Distributed Consensus',
  });

  useEffect(() => {
    founderApi.getSubmissionProof('sub_elena_01')
      .then((data) => {
        if (data) {
          setProofData((prev) => ({
            ...prev,
            hash: data.hash || prev.hash,
            score: data.score || prev.score,
            testsPassed: data.testsPassed || prev.testsPassed,
            testsTotal: data.testsTotal || prev.testsTotal,
            p99LatencyMs: data.p99LatencyMs || prev.p99LatencyMs,
            reviewerVerdict: data.reviewerVerdict || prev.reviewerVerdict,
            sprintName: data.sprintName || prev.sprintName,
          }));
        }
      })
      .catch((err) => console.warn('Proof API fallback:', err.message));
  }, []);

  const handleCopyHash = () => {
    navigator.clipboard.writeText(proofData.hash);
    showToast('Cryptographic Digest copied to clipboard');
  };

  return (
    <div className="flex flex-col w-full gap-space-lg">
      {/* Header and Digest */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-space-md">
        <div className="flex flex-col gap-space-xs">
          <nav className="flex items-center gap-2 font-body-sm text-body-sm text-on-surface-variant">
            <span>Cohort Alpha '25</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span>Proof of Work</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-semibold">Candidate #TX-9042A</span>
          </nav>
          <div className="flex items-center gap-space-sm flex-wrap mt-1">
            <h1 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
              Proof-of-Work Verification
            </h1>
            <div className="flex items-center gap-1.5 px-space-sm py-1 rounded-full bg-surface-container-low shadow-sm">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-secondary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-secondary"></span>
              </span>
              <span className="font-label-sm text-label-sm text-on-secondary-container">
                SHA-256: 0x8f9c7e2b...4a189f
              </span>
              <button
                type="button"
                onClick={handleCopyHash}
                className="text-on-surface-variant hover:text-secondary flex items-center ml-1"
                title="Copy Cryptographic Digest"
              >
                <span className="material-symbols-outlined text-[14px]">content_copy</span>
              </button>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-space-sm flex-wrap">
          <button
            type="button"
            onClick={() => showToast('Opening raw sandbox repository in browser viewer')}
            className="h-10 px-space-md rounded-lg bg-surface-container-lowest text-on-surface font-label-md text-label-md flex items-center gap-space-xs shadow-sm hover:bg-surface-container-high transition-colors"
          >
            <span className="material-symbols-outlined text-[18px] text-secondary">terminal</span>
            <span>Raw Sandbox Repo</span>
          </button>
          <button
            type="button"
            onClick={() => showToast('Public verification URL copied: https://ventureforge.ai/verify/TX-9042A')}
            className="h-10 px-space-md rounded-lg bg-surface-container-lowest text-on-surface font-label-md text-label-md flex items-center gap-space-xs shadow-sm hover:bg-surface-container-high transition-colors"
          >
            <span className="material-symbols-outlined text-[18px] text-on-surface-variant">share</span>
            <span>Share Certificate</span>
          </button>
          <button
            type="button"
            onClick={() => showToast('Proof of Work dossier PDF download initiated')}
            className="h-10 px-space-lg rounded-lg bg-primary-container text-on-primary font-label-md text-label-md flex items-center gap-space-xs shadow-md hover:bg-primary transition-all"
          >
            <span className="material-symbols-outlined text-[18px]">download</span>
            <span>Download PDF</span>
          </button>
        </div>
      </div>

      {/* Main Dossier Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg">
        {/* Left Column (8 cols): Candidate Profile & Verified Telemetry */}
        <div className="lg:col-span-8 flex flex-col gap-space-lg">
          {/* Identity Card */}
          <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm relative overflow-hidden">
            <div className="flex flex-col sm:flex-row items-start gap-space-lg">
              <div className="relative shrink-0">
                <div className="w-20 h-20 rounded-xl overflow-hidden bg-surface-container-high shadow-inner">
                  <img
                    className="w-full h-full object-cover"
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuCrFd9FXpH1DVp90x6QYI3kcBlABNYtgFYxaa-elUwjSWxyV56HX1Uir3Bo-JqKk3TkfehwV64tbjsMvhw9FVCYgdY2H_bGj_WUycEQb8Dik8Hw6UG-DAyLKzDMeTucfRCt_DgSFD6L_pCOl0A8YFS_ujCydDFtmuuoeY7hOIu_gb7QgAuFUQWPIUNLCYl78krYPxXqb-rVILLe9UGsKUdf2HDshK8T-ZrUTNmAMRphT1t5VEKD26jNtQ"
                    alt="Julian Vance"
                  />
                </div>
                <div className="absolute -bottom-2 -right-2 w-7 h-7 rounded-full bg-secondary text-on-secondary flex items-center justify-center shadow-md">
                  <span className="material-symbols-outlined text-[16px]">verified</span>
                </div>
              </div>

              <div className="flex flex-col gap-space-xs flex-1 min-w-0">
                <div className="flex items-center gap-space-sm flex-wrap">
                  <span className="font-headline-md text-headline-md text-on-surface font-bold tracking-tight">
                    Julian Vance
                  </span>
                  <span className="px-space-xs py-0.5 rounded bg-surface-container-high font-code-sm text-code-sm text-on-surface-variant">
                    Candidate ID #TX-9042A
                  </span>
                  <span className="px-space-xs py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                    Team Alpha
                  </span>
                </div>
                <p className="font-title-md text-title-md text-on-surface-variant font-medium">
                  Lead Distributed Systems Architect &amp; High-Throughput Systems Engineer
                </p>
                <div className="flex flex-wrap items-center gap-x-space-md gap-y-1 pt-space-xs text-on-surface-variant font-body-sm text-body-sm">
                  <span className="flex items-center gap-1">
                    <span className="material-symbols-outlined text-[16px] text-secondary">memory</span>
                    Rust / Go Core
                  </span>
                  <span>•</span>
                  <span>8 Yrs Verifiable Experience</span>
                  <span>•</span>
                  <span className="text-secondary font-semibold">Top 1% Execution Velocity</span>
                </div>
              </div>
            </div>
          </div>

          {/* 4 Execution Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-space-md">
            <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm">
              <span className="font-label-sm text-label-sm text-on-surface-variant block">Composite Score</span>
              <span className="font-headline-md text-headline-md font-bold text-secondary">94.2</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant">Top Tier (Alpha)</span>
            </div>
            <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm">
              <span className="font-label-sm text-label-sm text-on-surface-variant block">p99 Latency</span>
              <span className="font-headline-md text-headline-md font-bold text-on-surface">3.8ms</span>
              <span className="font-body-sm text-body-sm text-secondary">50k TPS Load</span>
            </div>
            <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm">
              <span className="font-label-sm text-label-sm text-on-surface-variant block">Consensus Replay</span>
              <span className="font-headline-md text-headline-md font-bold text-on-surface">100%</span>
              <span className="font-body-sm text-body-sm text-secondary">Deterministic</span>
            </div>
            <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm">
              <span className="font-label-sm text-label-sm text-on-surface-variant block">Memory Leaks</span>
              <span className="font-headline-md text-headline-md font-bold text-on-surface">0 Bytes</span>
              <span className="font-body-sm text-body-sm text-secondary">48h Soak Test</span>
            </div>
          </div>

          {/* Test Harness Terminal Log */}
          <div className="bg-primary-container text-on-primary rounded-xl p-space-lg shadow-sm flex flex-col gap-space-sm font-mono text-xs">
            <div className="flex items-center justify-between pb-2 border-b border-white/10">
              <span className="text-secondary-fixed font-bold">VentureForge Execution Harness v4.2 [Sandboxed Run]</span>
              <span className="text-white/60">Passed 50,000 / 50,000 cases</span>
            </div>
            <div className="space-y-1 text-white/80 leading-relaxed">
              <p className="text-emerald-400">[PASS] microvm::harness::spawn_50k_threads ... OK (duration: 1.42s)</p>
              <p className="text-emerald-400">[PASS] consensus::raft::split_brain_partition ... RECOVERED in 14ms</p>
              <p className="text-emerald-400">[PASS] memory::leak_detector::valgrind_verify ... 0 leaks, 0 suppressions</p>
              <p className="text-emerald-400">[PASS] crypto::merkle::root_hash_attestation ... SIGNED: 0x8f9c7e2b34a189fc</p>
              <p className="text-white/50 pt-2">// Final status: Cryptographically verified and anchored on Arbitrum One L2</p>
            </div>
          </div>
        </div>

        {/* Right Column (4 cols): Protocol Attestation Pack */}
        <div className="lg:col-span-4 flex flex-col gap-space-md">
          <div className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm flex flex-col gap-space-md border border-surface-container">
            <h3 className="font-title-md text-title-md font-bold text-on-surface flex items-center gap-2">
              <span className="material-symbols-outlined text-secondary">verified_user</span>
              Protocol Attestation Pack
            </h3>
            <div className="space-y-3 font-body-sm text-body-sm text-on-surface-variant">
              <div>
                <span className="font-label-sm text-label-sm text-outline block">Anchored On</span>
                <span className="font-medium text-on-surface">Arbitrum One (Contract 0x892a...c01)</span>
              </div>
              <div>
                <span className="font-label-sm text-label-sm text-outline block">Evaluator Blind Quorum</span>
                <span className="font-medium text-on-surface">3/3 AI Judges Unanimous</span>
              </div>
              <div>
                <span className="font-label-sm text-label-sm text-outline block">Zero-Knowledge Proof</span>
                <span className="font-medium text-on-surface">ZK-SNARK Groth16 Verified</span>
              </div>
              <div>
                <span className="font-label-sm text-label-sm text-outline block">Squad Recommendation</span>
                <span className="font-bold text-secondary">Immediate Inclusion (Rank #1)</span>
              </div>
            </div>

            <button
              type="button"
              onClick={() => showToast('Julian Vance officially welcomed to Synthetix AI Cap Table!')}
              className="mt-2 w-full h-11 rounded-lg bg-secondary text-on-secondary font-title-md text-title-md font-semibold hover:opacity-90 transition-all flex items-center justify-center gap-2 shadow-sm"
            >
              <span>Accept &amp; Wire into Squad</span>
              <span className="material-symbols-outlined text-[18px]">done</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
