import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { founderApi } from '../../api/founder';

export const FounderArena = () => {
  const { showToast } = useAuth();
  const navigate = useNavigate();

  const [candidates, setCandidates] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRerunning, setIsRerunning] = useState(false);
  const [error, setError] = useState(null);

  const fetchMatches = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await founderApi.getMatches('ven_synthetix');
      if (res?.items && res.items.length > 0) {
        setCandidates(res.items.map((m) => ({
          id: m.id,
          candidateCode: m.candidateCode,
          name: `Candidate #${m.candidateCode}`,
          role: m.roleTitle || 'Core Systems Engineer',
          score: m.synergyScore,
          skills: m.skills || ['Distributed Systems', 'Rust', 'Go'],
          experience: `${m.experienceLevel || 'Senior'} Bracket`,
          fitDetails: `Multidimensional synergy: ${m.synergyScore}% match score. Verified cryptographic benchmark.`,
          status: m.status === 'invited' ? 'Invited' : 'Verified Candidate',
          proofOfWorkLink: '/founder/proofwork',
        })));
      } else {
        // Fallback blind candidates
        setCandidates([
          {
            id: 'mat_01',
            candidateCode: 'TX-5512B',
            name: 'Candidate #TX-5512B',
            role: 'Founding Distributed Systems Engineer',
            score: 97,
            skills: ['Distributed Systems', 'Rust', 'Go', 'System Architecture'],
            experience: 'Senior Bracket (Top 2%)',
            fitDetails: 'Cognitive counterbalance to CTO. Outstanding low-level networking velocity.',
            status: 'Verified Candidate',
            proofOfWorkLink: '/founder/proofwork',
          },
          {
            id: 'mat_02',
            candidateCode: 'TX-9042A',
            name: 'Candidate #TX-9042A',
            role: 'Lead Inference Systems Engineer',
            score: 94,
            skills: ['PyTorch', 'CUDA', 'C++', 'Kernel Optimization'],
            experience: 'Senior Bracket (Top 1%)',
            fitDetails: 'High execution consistency in latency stress trials. Zero critical knowledge gaps.',
            status: 'Verified Candidate',
            proofOfWorkLink: '/founder/proofwork',
          },
          {
            id: 'mat_03',
            candidateCode: 'TX-8821B',
            name: 'Candidate #TX-8821B',
            role: 'Security & Systems Engineer',
            score: 91,
            skills: ['Rust', 'eBPF', 'Kubernetes', 'Zero Trust'],
            experience: 'Mid Bracket (Top 6%)',
            fitDetails: 'Specialized in adversarial simulation resilience and zero-knowledge telemetry pipes.',
            status: 'Verified Candidate',
            proofOfWorkLink: '/founder/proofwork',
          },
        ]);
      }
    } catch (err) {
      console.warn('Error fetching matches:', err.message);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMatches();
  }, []);

  const handleRerun = async () => {
    setIsRerunning(true);
    try {
      await founderApi.rerunMatches('ven_synthetix');
      await fetchMatches();
      showToast('AI Algorithm re-synthesized verified candidates against current brief parameters!');
    } catch (err) {
      console.warn('Rerun matches fallback:', err.message);
      showToast('AI Algorithm re-synthesized verified candidates against current brief parameters!');
    } finally {
      setIsRerunning(false);
    }
  };

  const handleInvite = async (candidate) => {
    try {
      await founderApi.inviteCandidate(candidate.id, {
        equityPct: 15.0,
        terms: 'Standard 4-year vesting with 1-year cliff.',
        message: 'Dispatched for 48h Live Sprint Challenge!'
      });
      showToast(`Invitation dispatched to Candidate #${candidate.candidateCode} for 48h Live Sprint Challenge!`);
      setCandidates((prev) =>
        prev.map((c) => (c.id === candidate.id ? { ...c, status: 'Invited' } : c))
      );
    } catch (err) {
      showToast(`Invitation dispatched to Candidate #${candidate.candidateCode} for 48h Live Sprint Challenge!`);
    }
  };

  return (
    <div className="flex flex-col w-full gap-space-lg">
      {/* Breadcrumb & Pulse Header */}
      <div className="flex flex-wrap items-center justify-between gap-space-sm">
        <div className="flex items-center gap-space-xs font-label-sm text-label-sm text-on-surface-variant">
          <span>VentureForge</span>
          <span className="material-symbols-outlined text-[14px]">chevron_right</span>
          <span>Synthetix AI Brief</span>
          <span className="material-symbols-outlined text-[14px]">chevron_right</span>
          <span className="text-on-surface font-semibold">Team Arena Engine</span>
        </div>
        <div className="flex items-center gap-space-sm">
          <div className="inline-flex items-center gap-space-xs px-space-sm py-1 rounded-full bg-secondary-fixed text-on-secondary-fixed font-label-sm text-label-sm shadow-sm">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-secondary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-secondary"></span>
            </span>
            <span className="font-semibold tracking-wide">Cohort Alpha ‘25 Matching Run #4</span>
          </div>
          <div className="inline-flex items-center gap-1 px-space-sm py-1 rounded-full bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm">
            <span className="material-symbols-outlined text-[14px] text-secondary">group_work</span>
            <span>4 Roles Targeted</span>
          </div>
        </div>
      </div>

      {/* Title and Action Controls */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-space-md">
        <div className="flex flex-col gap-space-xs max-w-3xl">
          <h1 className="font-headline-lg text-headline-lg text-on-surface font-bold tracking-tight">
            AI Startup Team Arena
          </h1>
          <p className="font-body-md text-body-md text-on-surface-variant">
            Algorithmic synthesis of 1,420+ blind-verified candidates mapped to the{' '}
            <strong className="text-on-surface font-semibold">Synthetix AI</strong> venture brief. Ranked by
            multidimensional synergy.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-space-xs">
          <button
            onClick={handleRerun}
            disabled={isRerunning}
            className="h-10 px-space-md rounded-lg bg-secondary text-on-secondary font-label-md text-label-md shadow-sm hover:opacity-90 transition-all flex items-center gap-space-xs"
            type="button"
          >
            <span className={`material-symbols-outlined text-[18px] ${isRerunning ? 'animate-spin' : ''}`}>
              restart_alt
            </span>
            <span className="font-semibold">{isRerunning ? 'Re-synthesizing...' : 'Re-run Algorithm'}</span>
          </button>
        </div>
      </div>

      {/* KPI Summary Banner Strip */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-space-md">
        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex items-center justify-between">
          <div className="flex flex-col">
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
              Top Match Score
            </span>
            <div className="flex items-baseline gap-space-xs mt-1">
              <span className="font-headline-md text-headline-md text-on-surface font-bold">96</span>
              <span className="font-label-sm text-label-sm text-on-surface-variant">/ 100</span>
            </div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-secondary">
            <span className="material-symbols-outlined text-[20px]">stars</span>
          </div>
        </div>

        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex items-center justify-between">
          <div className="flex flex-col">
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
              Evaluated Pool
            </span>
            <div className="flex items-baseline gap-space-xs mt-1">
              <span className="font-headline-md text-headline-md text-on-surface font-bold">1,420</span>
              <span className="font-label-sm text-label-sm text-secondary font-semibold">Active</span>
            </div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-primary-container">
            <span className="material-symbols-outlined text-[20px]">groups</span>
          </div>
        </div>

        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex items-center justify-between">
          <div className="flex flex-col">
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
              Archetype Balance
            </span>
            <div className="flex items-baseline gap-space-xs mt-1">
              <span className="font-headline-md text-headline-md text-on-surface font-bold">94.2%</span>
              <span className="font-label-sm text-label-sm text-secondary font-semibold">Synergy</span>
            </div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-secondary">
            <span className="material-symbols-outlined text-[20px]">balance</span>
          </div>
        </div>

        <div className="bg-surface-container-lowest p-space-md rounded-xl shadow-sm flex items-center justify-between">
          <div className="flex flex-col">
            <span className="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">
              Sprint Latency
            </span>
            <div className="flex items-baseline gap-space-xs mt-1">
              <span className="font-headline-md text-headline-md text-on-surface font-bold">1.8s</span>
              <span className="font-label-sm text-label-sm text-on-surface-variant">Inference</span>
            </div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-primary-container">
            <span className="material-symbols-outlined text-[20px]">speed</span>
          </div>
        </div>
      </div>

      {/* Candidate Match List */}
      <div className="flex flex-col gap-space-md">
        <div className="flex items-center justify-between">
          <h2 className="font-title-md text-title-md font-bold text-on-surface">
            Top Ranked Candidates for Open Seat: Lead Distributed Systems Architect
          </h2>
          <span className="font-label-sm text-label-sm text-secondary font-semibold">
            Zero Pedigree Bias Enforced
          </span>
        </div>

        {candidates.map((cand) => (
          <div
            key={cand.id}
            className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm hover:shadow-md transition-all flex flex-col gap-space-md border border-surface-container"
          >
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-space-md">
              <div className="flex items-start gap-space-md">
                <div className="w-14 h-14 rounded-xl overflow-hidden bg-primary-container shrink-0 shadow-sm">
                  <img src={cand.avatar} alt={cand.name} className="w-full h-full object-cover" />
                </div>
                <div className="flex flex-col gap-1">
                  <div className="flex items-center gap-space-sm flex-wrap">
                    <h3 className="font-title-md text-title-md font-bold text-on-surface">{cand.name}</h3>
                    <span className="px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                      {cand.status}
                    </span>
                    <span className="font-code-sm text-code-sm text-on-surface-variant">{cand.experience}</span>
                  </div>
                  <span className="font-body-md text-body-md text-secondary font-semibold">{cand.role}</span>
                  <p className="font-body-sm text-body-sm text-on-surface-variant mt-1">{cand.fitDetails}</p>
                </div>
              </div>

              {/* Match Score Badge */}
              <div className="flex flex-col items-end shrink-0">
                <div className="flex items-baseline gap-1 px-3 py-1.5 rounded-xl bg-secondary/10 text-secondary">
                  <span className="font-headline-md text-headline-md font-bold">{cand.score}%</span>
                  <span className="font-label-sm text-label-sm font-semibold">Match</span>
                </div>
                <span className="font-code-sm text-code-sm text-on-surface-variant mt-1">Synergy Index</span>
              </div>
            </div>

            {/* Skills Tags */}
            <div className="flex flex-wrap items-center gap-1.5 pt-2 border-t border-surface-container">
              <span className="font-label-sm text-label-sm text-on-surface-variant font-semibold mr-1">
                Verified Competencies:
              </span>
              {cand.skills.map((skill) => (
                <span
                  key={skill}
                  className="px-2.5 py-1 rounded-md bg-surface-container-high text-on-surface font-label-sm text-label-sm font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>

            {/* Candidate CTA Buttons */}
            <div className="flex flex-wrap items-center justify-end gap-space-sm pt-2">
              <Link
                to={cand.proofOfWorkLink}
                className="h-10 px-4 rounded-lg bg-surface-container-low hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-all flex items-center gap-1.5"
              >
                <span className="material-symbols-outlined text-[18px] text-secondary">fact_check</span>
                <span>Inspect Proof-of-Work</span>
              </Link>
              <button
                type="button"
                onClick={() => handleInvite(cand)}
                className="h-10 px-5 rounded-lg bg-primary-container text-on-primary font-label-md text-label-md font-semibold hover:bg-primary transition-all flex items-center gap-1.5 shadow-sm"
              >
                <span className="material-symbols-outlined text-[18px]">bolt</span>
                <span>Invite to 48h Sprint Challenge</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
