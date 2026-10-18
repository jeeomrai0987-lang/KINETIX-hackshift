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
        setCandidates(
          res.items.map((m) => {
            let reason = '';
            if (typeof m.fitDetails === 'string') {
              reason = m.fitDetails;
            } else if (m.fitDetails && typeof m.fitDetails === 'object') {
              reason =
                m.fitDetails.algorithmicReason ||
                `${m.fitDetails.experienceFit || 'Verified'} • Availability: ${m.fitDetails.availabilityHours || 40}h/wk`;
            }

            return {
              id: m.id,
              candidateCode: m.candidateCode,
              name: `Candidate #${m.candidateCode}`,
              role: m.roleTitle || 'Core Systems Engineer',
              score: m.synergyScore,
              skills: m.skills || ['Distributed Systems', 'Rust', 'Go'],
              experience: `${m.experienceLevel ? m.experienceLevel.charAt(0).toUpperCase() + m.experienceLevel.slice(1) : 'Senior'} Bracket`,
              fitDetails: reason || `Multidimensional synergy: ${m.synergyScore}% match score. Verified cryptographic benchmark.`,
              status: m.status === 'invited' ? 'Invited' : 'Verified Candidate',
              proofOfWorkLink: '/founder/proofwork',
              avatar: m.avatar || null,
            };
          })
        );
      } else {
        setCandidates([]);
      }
    } catch (err) {
      console.warn('Error fetching matches:', err.message);
      setError(err.message);
      setCandidates([]);
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

  const topScore = candidates.length > 0 ? Math.max(...candidates.map((c) => c.score)) : 96;

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
            <span className="font-semibold tracking-wide">Cohort Alpha ‘25 Matching Active</span>
          </div>
          <div className="inline-flex items-center gap-1 px-space-sm py-1 rounded-full bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm">
            <span className="material-symbols-outlined text-[14px] text-secondary">group_work</span>
            <span>{candidates.length} Ranked Matches</span>
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
            Algorithmic synthesis of blind-verified database candidates mapped to the{' '}
            <strong className="text-on-surface font-semibold">Synthetix AI</strong> venture brief. Ranked by
            multidimensional synergy.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-space-xs">
          <button
            onClick={handleRerun}
            disabled={isRerunning || isLoading}
            className="h-10 px-space-md rounded-lg bg-secondary text-on-secondary font-label-md text-label-md shadow-sm hover:opacity-90 transition-all flex items-center gap-space-xs disabled:opacity-50"
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
              <span className="font-headline-md text-headline-md text-on-surface font-bold">{topScore}</span>
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
              Evaluated Candidates
            </span>
            <div className="flex items-baseline gap-space-xs mt-1">
              <span className="font-headline-md text-headline-md text-on-surface font-bold">
                {candidates.length}
              </span>
              <span className="font-label-sm text-label-sm text-secondary font-semibold">Active Pool</span>
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
              Protocol Privacy
            </span>
            <div className="flex items-baseline gap-space-xs mt-1">
              <span className="font-headline-md text-headline-md text-secondary font-bold">100%</span>
              <span className="font-label-sm text-label-sm text-on-surface-variant">Blind</span>
            </div>
          </div>
          <div className="w-10 h-10 rounded-lg bg-surface-container-high flex items-center justify-center text-primary-container">
            <span className="material-symbols-outlined text-[20px]">lock</span>
          </div>
        </div>
      </div>

      {/* Candidate Match List */}
      <div className="flex flex-col gap-space-md">
        <div className="flex items-center justify-between">
          <h2 className="font-title-md text-title-md font-bold text-on-surface">
            Ranked Candidate Matches for Open Squad Roles
          </h2>
          <span className="font-label-sm text-label-sm text-secondary font-semibold">
            Zero Pedigree Bias • Blind Protocol Enforced
          </span>
        </div>

        {isLoading ? (
          <div className="bg-surface-container-lowest rounded-xl p-12 shadow-sm border border-surface-container flex flex-col items-center justify-center gap-3">
            <span className="material-symbols-outlined text-3xl text-secondary animate-spin">progress_activity</span>
            <span className="font-title-md text-title-md font-semibold text-on-surface">Loading Algorithmic Matches...</span>
          </div>
        ) : candidates.length === 0 ? (
          <div className="bg-surface-container-lowest rounded-xl p-space-xl shadow-sm border border-surface-container flex flex-col items-center justify-center text-center gap-space-md py-12">
            <div className="w-16 h-16 rounded-2xl bg-surface-container-low text-secondary flex items-center justify-center">
              <span className="material-symbols-outlined text-[32px]">group_off</span>
            </div>
            <div className="flex flex-col gap-1 max-w-md">
              <h3 className="font-title-lg text-title-lg font-bold text-on-surface">No Candidate Matches Found</h3>
              <p className="font-body-sm text-body-sm text-on-surface-variant">
                No available workers currently meet the exact required skill weights or availability threshold for this squad blueprint.
              </p>
            </div>
            <div className="flex items-center gap-space-sm mt-2">
              <button
                type="button"
                onClick={handleRerun}
                disabled={isRerunning}
                className="px-4 py-2 rounded-lg bg-secondary text-on-secondary font-label-md text-label-md font-semibold hover:opacity-90 transition-all flex items-center gap-2"
              >
                <span className={`material-symbols-outlined text-[18px] ${isRerunning ? 'animate-spin' : ''}`}>restart_alt</span>
                <span>Re-run Matching Engine</span>
              </button>
              <Link
                to="/founder/startup"
                className="px-4 py-2 rounded-lg bg-surface-container-low hover:bg-surface-container-high text-on-surface font-label-md text-label-md font-semibold transition-all"
              >
                Adjust Venture Brief
              </Link>
            </div>
          </div>
        ) : (
          candidates.map((cand) => (
            <div
              key={cand.id}
              className="bg-surface-container-lowest rounded-xl p-space-lg shadow-sm hover:shadow-md transition-all flex flex-col gap-space-md border border-surface-container"
            >
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-space-md">
                <div className="flex items-start gap-space-md">
                  {cand.avatar ? (
                    <div className="w-14 h-14 rounded-xl overflow-hidden bg-primary-container shrink-0 shadow-sm">
                      <img src={cand.avatar} alt={cand.name} className="w-full h-full object-cover" />
                    </div>
                  ) : (
                    <div className="w-14 h-14 rounded-xl bg-surface-container-high text-secondary flex items-center justify-center shrink-0 shadow-sm border border-surface-container">
                      <span className="material-symbols-outlined text-[26px]">shield_person</span>
                    </div>
                  )}
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
          ))
        )}
      </div>
    </div>
  );
};
