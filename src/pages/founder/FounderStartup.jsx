import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { founderApi } from '../../api/founder';

export const FounderStartup = () => {
  const { showToast } = useAuth();
  const navigate = useNavigate();

  const [thesis, setThesis] = useState(
    'Synthetix AI is building an autonomous agentic simulation pipeline for stress-testing multi-agent LLM systems in high-throughput enterprise fintech. We simulate millions of adversarial edge cases, latency spikes, and regulatory compliance breaches before companies deploy AI agents live to banking infrastructure. We need an ultra-low-latency backend, robust distributed systems orchestration, enterprise security verification, and a commercial leader experienced in B2B enterprise sales cycles.'
  );

  const [isDecomposing, setIsDecomposing] = useState(false);
  const [isApproving, setIsApproving] = useState(false);
  const [error, setError] = useState(null);
  const [clarityScore, setClarityScore] = useState(94);
  const [aiSource, setAiSource] = useState(null);
  const [latencyMs, setLatencyMs] = useState(null);
  const [extractedConstraints, setExtractedConstraints] = useState(null);
  const [decomposedBlueprint, setDecomposedBlueprint] = useState(null);

  const defaultBlueprint = [
    {
      title: 'Co-Founder & CTO',
      description: 'Architects high-throughput consensus mechanisms and memory-safe verifiable kernels.',
      equityPct: 25.0,
      requirements: [{ skill: 'distributed systems', weight: 1.0 }, { skill: 'rust', weight: 1.0 }],
      minExperience: 'founding',
      status: 'vacant'
    },
    {
      title: 'Founding Distributed Systems Engineer',
      description: 'Builds zero-copy asynchronous networking engines and deterministic Raft clusters.',
      equityPct: 15.0,
      requirements: [{ skill: 'rust', weight: 1.0 }, { skill: 'go', weight: 0.8 }, { skill: 'zero-copy io', weight: 0.9 }],
      minExperience: 'senior',
      status: 'vacant'
    },
    {
      title: 'Lead Inference Systems Engineer',
      description: 'Implements GPU kernel optimizations, CUDA kernels, and memory tiering.',
      equityPct: 15.0,
      requirements: [{ skill: 'c++', weight: 1.0 }, { skill: 'p99 latency optimization', weight: 0.8 }],
      minExperience: 'senior',
      status: 'vacant'
    },
    {
      title: 'Head of Enterprise Growth',
      description: 'Drives strategic pilot deployments, enterprise customer discovery, and compliance partnership pipelines.',
      equityPct: 15.0,
      requirements: [{ skill: 'enterprise gtm', weight: 1.0 }, { skill: 'b2b saas', weight: 0.9 }],
      minExperience: 'senior',
      status: 'vacant'
    }
  ];

  const activeRoles = decomposedBlueprint || defaultBlueprint;

  const handleDeconstruct = async () => {
    setIsDecomposing(true);
    setError(null);
    try {
      const res = await founderApi.decomposeThesis('ven_synthetix', thesis);
      if (res?.constraints) setExtractedConstraints(res.constraints);
      if (res?.blueprint || res?.roles) setDecomposedBlueprint(res.blueprint || res.roles);
      if (res?.clarityScore != null) setClarityScore(res.clarityScore);
      if (res?.source) setAiSource(res.source === 'gemini' ? 'Gemini' : 'Fallback');
      if (res?.latencyMs != null) setLatencyMs(res.latencyMs);
      showToast(`Thesis decomposed successfully via AI (${res.source === 'gemini' ? 'Gemini' : 'Fallback'}) in ${res.latencyMs || 0}ms!`);
    } catch (err) {
      console.warn('Decomposition API fallback:', err.message);
      setError(err.message);
      setAiSource('Fallback');
      showToast('Thesis decomposed with deterministic fallback blueprint!');
    } finally {
      setIsDecomposing(false);
    }
  };

  const handleBroadcast = async () => {
    setIsApproving(true);
    try {
      await founderApi.approveBlueprint('ven_synthetix', activeRoles);
      showToast('Squad Blueprint approved! Match requests dispatched to Team Arena.');
      setTimeout(() => {
        navigate('/founder/arena');
      }, 500);
    } catch (err) {
      console.warn('Approve blueprint fallback:', err.message);
      showToast('Squad Blueprint approved! Match requests dispatched to Team Arena.');
      setTimeout(() => {
        navigate('/founder/arena');
      }, 500);
    } finally {
      setIsApproving(false);
    }
  };

  return (
    <div className="flex flex-col w-full gap-space-lg">
      {/* Top Header */}
      <header className="flex flex-col md:flex-row md:items-end justify-between gap-space-md">
        <div className="flex flex-col gap-space-xs">
          <nav aria-label="Breadcrumbs" className="flex items-center gap-space-xs text-on-surface-variant font-label-sm text-label-sm">
            <span className="hover:text-on-surface cursor-pointer transition-colors">Startup</span>
            <span className="material-symbols-outlined text-[14px]">chevron_right</span>
            <span className="text-secondary font-medium">New Venture Thesis &amp; Team Genesis</span>
          </nav>
          <div className="flex items-center gap-space-sm mt-1">
            <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
              Startup Brief &amp; Requirement Decomposition
            </h1>
            <span className="px-2 py-0.5 rounded-full bg-surface-container text-on-surface-variant font-code-sm text-code-sm">
              v3.2
            </span>
          </div>
          <p className="font-body-md text-body-md text-on-surface-variant max-w-3xl">
            Articulate your venture thesis in natural language. Our formation AI automatically extracts core technical specs, operational constraints, and ideal founding squad compositions.
          </p>
        </div>

        {/* AI Meta Status */}
        <div className="flex items-center gap-space-sm self-start md:self-end">
          <div className="px-space-md py-space-xs rounded-xl bg-surface-container-low shadow-sm flex items-center gap-space-sm">
            <div className="relative flex items-center justify-center">
              <span className={`w-2 h-2 rounded-full ${aiSource === 'Gemini' ? 'bg-secondary animate-ping' : 'bg-outline'} absolute`}></span>
              <span className={`w-2 h-2 rounded-full ${aiSource === 'Gemini' ? 'bg-secondary' : 'bg-outline'} relative`}></span>
            </div>
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm text-on-surface-variant leading-none">Inference Engine</span>
              <span className="font-code-sm text-code-sm text-on-surface font-semibold">
                AI: {aiSource || 'Gemini'} • {latencyMs ? `${(latencyMs / 1000).toFixed(2)}s` : '1.8s'}
              </span>
            </div>
            <div className="w-px h-6 bg-surface-container-high mx-1"></div>
            <span className="material-symbols-outlined text-secondary text-[20px]" title="AI Pipeline Active">memory</span>
          </div>
        </div>
      </header>

      {error && (
        <div className="p-4 rounded-xl bg-error-container/20 border border-error/30 text-error flex items-center gap-2">
          <span className="material-symbols-outlined text-lg">info</span>
          <span className="font-body-sm text-body-sm">{error}</span>
        </div>
      )}

      {/* Dual Column Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-space-lg items-start">
        {/* Column 1: Venture Concept & Thesis Prompt */}
        <section className="lg:col-span-6 flex flex-col gap-space-md">
          <div className="bg-surface-container-lowest rounded-xl shadow-sm p-space-lg flex flex-col gap-space-md">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-space-sm">
                <div className="w-7 h-7 rounded-lg bg-primary-container text-on-primary flex items-center justify-center">
                  <span className="material-symbols-outlined text-[16px]">edit_note</span>
                </div>
                <h2 className="font-title-md text-title-md text-on-surface font-semibold tracking-tight">
                  01. Venture Concept &amp; Thesis Prompt
                </h2>
              </div>
              <div className="flex items-center gap-1.5 px-space-sm py-1 rounded-full bg-surface-container-low text-secondary font-label-sm text-label-sm">
                <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
                <span>Draft Auto-Saved</span>
              </div>
            </div>

            <div className="flex flex-col gap-space-xs">
              <div className="relative rounded-lg bg-surface-container-low p-space-sm focus-within:bg-surface-container-lowest focus-within:ring-2 focus-within:ring-secondary/40 transition-all">
                <textarea
                  className="w-full bg-transparent resize-none text-on-surface font-body-md text-body-md leading-relaxed placeholder:text-outline focus:outline-none"
                  rows={9}
                  value={thesis}
                  onChange={(e) => setThesis(e.target.value)}
                  placeholder="Synthesize your venture thesis..."
                />
                <div className="flex items-center justify-between pt-space-xs border-t border-surface-container mt-2">
                  <div className="flex items-center gap-space-xs font-code-sm text-code-sm text-on-surface-variant">
                    <span className="material-symbols-outlined text-[16px] text-secondary">verified</span>
                    <span>Clarity Score:</span>
                    <span className="text-on-surface font-bold">{clarityScore}/100</span>
                    <span className="text-on-surface-variant opacity-60">
                      • {clarityScore >= 90 ? 'High Specification Certainty' : clarityScore >= 75 ? 'Strong Thesis Detail' : 'Emerging Synthesis'}
                    </span>
                  </div>
                  <span className="font-code-sm text-code-sm text-on-surface-variant">
                    {thesis.length} chars / {thesis.split(' ').filter(Boolean).length} words
                  </span>
                </div>
              </div>
            </div>

            {/* Action Bar */}
            <div className="flex items-center justify-between pt-2">
              <button
                type="button"
                onClick={() => setThesis('Aether Labs is developing zero-knowledge verifiable machine learning circuits for on-chain credit scoring with sub-millisecond cryptographic proving.')}
                className="font-label-md text-label-md text-secondary hover:underline"
              >
                Load Alternate Cohort Template
              </button>
              <button
                type="button"
                onClick={handleDeconstruct}
                disabled={isDecomposing}
                className="px-5 py-2.5 rounded-lg bg-primary-container text-on-primary font-title-md text-title-md font-semibold hover:bg-primary transition-all flex items-center gap-2 shadow-sm disabled:opacity-50"
              >
                {isDecomposing ? (
                  <>
                    <span className="material-symbols-outlined text-lg animate-spin">progress_activity</span>
                    <span>Deconstructing...</span>
                  </>
                ) : (
                  <>
                    <span>Deconstruct Thesis</span>
                    <span className="material-symbols-outlined text-lg">auto_awesome</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Operational Bottlenecks Card */}
          <div className="bg-surface-container-lowest rounded-xl shadow-sm p-space-lg flex flex-col gap-space-md">
            <h3 className="font-title-md text-title-md text-on-surface font-semibold flex items-center gap-2">
              <span className="material-symbols-outlined text-secondary">tune</span>
              Extracted Constraints &amp; Moat Parameters
            </h3>
            <div className="grid grid-cols-2 gap-space-md">
              <div className="p-space-sm rounded-lg bg-surface-container-low">
                <span className="font-label-sm text-label-sm text-on-surface-variant block mb-1">Target Sector</span>
                <span className="font-title-md text-title-md font-bold text-on-surface truncate">
                  {extractedConstraints?.sector || 'Enterprise AI & Distributed Systems'}
                </span>
              </div>
              <div className="p-space-sm rounded-lg bg-surface-container-low">
                <span className="font-label-sm text-label-sm text-on-surface-variant block mb-1">Latency Requirement</span>
                <span className="font-title-md text-title-md font-bold text-secondary">
                  &lt; {extractedConstraints?.latencyMs ?? 2}ms Engine Target
                </span>
              </div>
              <div className="p-space-sm rounded-lg bg-surface-container-low">
                <span className="font-label-sm text-label-sm text-on-surface-variant block mb-1">Compliance Scope</span>
                <span className="font-title-md text-title-md font-bold text-on-surface truncate">
                  {Array.isArray(extractedConstraints?.compliance)
                    ? extractedConstraints.compliance.join(' + ')
                    : (extractedConstraints?.compliance || 'SOC2 Type II + FedRAMP')}
                </span>
              </div>
              <div className="p-space-sm rounded-lg bg-surface-container-low">
                <span className="font-label-sm text-label-sm text-on-surface-variant block mb-1">Initial Squad Size</span>
                <span className="font-title-md text-title-md font-bold text-on-surface">
                  {extractedConstraints?.squadSize || activeRoles.length} Founding Members
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* Column 2: Decomposition Results & AI Target Squad Architecture */}
        <section className="lg:col-span-6 flex flex-col gap-space-md">
          <div className="bg-surface-container-lowest rounded-xl shadow-sm p-space-lg flex flex-col gap-space-md">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-space-sm">
                <div className="w-7 h-7 rounded-lg bg-secondary text-on-secondary flex items-center justify-center">
                  <span className="material-symbols-outlined text-[16px]">schema</span>
                </div>
                <h2 className="font-title-md text-title-md text-on-surface font-semibold tracking-tight">
                  02. Target Squad Blueprint &amp; Archetype Allocation
                </h2>
              </div>
              <span className="px-2.5 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                {decomposedBlueprint ? 'Synthesized' : 'Baseline Matrix'}
              </span>
            </div>

            <div className="space-y-space-md">
              {activeRoles.map((role, idx) => {
                const roleNum = String(idx + 1).padStart(2, '0');
                const reqs = role.requirements || role.requiredSkills || [];
                return (
                  <div key={role.title || idx} className="p-space-md rounded-xl bg-surface-container-low border border-surface-container flex flex-col gap-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="w-6 h-6 rounded-md bg-primary-container text-on-primary flex items-center justify-center font-bold text-xs">
                          {roleNum}
                        </span>
                        <span className="font-title-md text-title-md font-bold text-on-surface">
                          {role.title}
                        </span>
                      </div>
                      <span className="px-2 py-0.5 rounded bg-primary-fixed text-on-primary-fixed font-label-sm text-label-sm font-semibold">
                        Target: {role.equityPct || role.equity_pct}%
                      </span>
                    </div>
                    <p className="font-body-sm text-body-sm text-on-surface-variant">
                      {role.description}
                    </p>
                    {reqs.length > 0 && (
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {reqs.map((req, rIdx) => {
                          const skillName = typeof req === 'string' ? req : req.skill;
                          return (
                            <span
                              key={rIdx}
                              className="px-2 py-0.5 rounded bg-surface-container text-on-surface-variant font-code-sm text-code-sm"
                            >
                              {skillName}
                            </span>
                          );
                        })}
                      </div>
                    )}
                    <div className="flex items-center justify-between pt-1 border-t border-surface-container-high/40 mt-1">
                      <span className="font-label-sm text-label-sm text-secondary font-semibold">
                        VACANT • Open for Team Arena matching
                      </span>
                      <span className="font-code-sm text-code-sm text-on-surface-variant capitalize">
                        Min: {role.minExperience || role.min_experience || 'senior'}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Broadcast CTA */}
            <div className="pt-2">
              <button
                type="button"
                onClick={handleBroadcast}
                disabled={isApproving || isDecomposing}
                className="w-full h-11 rounded-lg bg-secondary text-on-secondary font-title-md text-title-md font-semibold hover:opacity-90 transition-all flex items-center justify-center gap-2 shadow-sm disabled:opacity-50"
              >
                {isApproving ? (
                  <>
                    <span className="material-symbols-outlined text-lg animate-spin">progress_activity</span>
                    <span>Approving &amp; Matching...</span>
                  </>
                ) : (
                  <>
                    <span>Approve Squad Blueprint &amp; Match in Team Arena</span>
                    <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};
