import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const LandingPage = () => {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();

  const handlePortalEntry = () => {
    if (user?.role === 'investor') navigate('/investor/dashboard');
    else if (user?.role === 'worker') navigate('/worker/dashboard');
    else navigate('/founder/dashboard');
  };

  return (
    <div className="bg-background font-body-md text-body-md text-on-surface antialiased">
      {/* Top Navigation Header */}
      <header className="fixed top-0 w-full z-50 bg-surface/80 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)]">
        <div className="h-16 max-w-7xl mx-auto px-6 lg:px-12 flex items-center justify-between gap-space-lg">
          <Link to="/" className="flex items-center gap-space-md">
            <img
              alt="VentureForge AI Logo"
              className="h-8 w-auto object-contain"
              src="https://lh3.googleusercontent.com/aida/AEtjO1UFGfu5Xb2n4cvQa09mVmUxLW2NXOMyJIZibjDBXaBIcdR3BFaFg04_p49080Tb4xi6EIRQFTKFc6QnPtw9uxJwaBqQwoK1K2NkFKQreqVlSWGs0znR_2OPX25UQZZ3LcnlfbGsRkoaIdb12hFfIaP6lEGbMxaI9JZHoA_syD-aVxcKROl3Is-0ePC57cHtn18ghJQ5zbDeC1SU5mOze0yxgAiy6OXTdWaN2PzJoYjeNUsQwggJwkHY2ID_"
            />
            <span className="font-title-md text-title-md text-on-surface tracking-tight font-semibold">
              VentureForge AI
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-space-xl">
            <a href="#flywheel" className="font-body-md text-body-md text-on-surface-variant hover:text-on-surface transition-colors">
              How It Works
            </a>
            <a href="#features" className="font-body-md text-body-md text-on-surface-variant hover:text-on-surface transition-colors">
              Features
            </a>
            <a href="#whatsapp" className="font-body-md text-body-md text-on-surface-variant hover:text-on-surface transition-colors">
              WhatsApp Flow
            </a>
            <a href="#arena-preview" className="font-body-md text-body-md text-on-surface-variant hover:text-on-surface transition-colors">
              Synergy Arena
            </a>
          </nav>

          <div className="flex items-center gap-space-md">
            {isAuthenticated ? (
              <button
                onClick={handlePortalEntry}
                className="inline-flex items-center justify-center gap-2 px-space-md py-space-xs font-label-md text-label-md text-on-primary bg-primary hover:bg-primary-container rounded-lg transition-colors shadow-sm"
              >
                <span>Go to {user?.role ? user.role.toUpperCase() : 'APP'} Portal</span>
                <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
              </button>
            ) : (
              <>
                <Link
                  to="/auth?mode=login"
                  className="inline-flex items-center justify-center px-space-md py-space-xs font-label-md text-label-md text-on-surface hover:text-primary transition-colors"
                >
                  Sign in
                </Link>
                <Link
                  to="/auth?mode=register"
                  className="inline-flex items-center justify-center px-space-md py-space-xs font-label-md text-label-md text-on-primary bg-primary hover:bg-primary-container rounded-lg transition-colors shadow-sm"
                >
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Main Page Body */}
      <main className="w-full pt-16 bg-background">
        <div className="flex flex-col w-full">
          {/* Atmospheric Glow Layer */}
          <div className="relative w-full overflow-hidden">
            <div className="absolute -top-32 left-1/2 -translate-x-1/2 w-[720px] h-[340px] bg-secondary-fixed opacity-30 blur-[120px] pointer-events-none rounded-full"></div>
            <div className="absolute top-48 right-10 w-[380px] h-[380px] bg-surface-container opacity-50 blur-[100px] pointer-events-none rounded-full"></div>

            {/* 1. Hero Section */}
            <section className="relative max-w-7xl mx-auto px-6 lg:px-12 pt-12 pb-20 flex flex-col items-center text-center">
              {/* Eyebrow Pill */}
              <div className="inline-flex items-center gap-space-sm px-3 py-1 rounded-full bg-surface-container-lowest shadow-sm mb-6">
                <span className="inline-flex items-center gap-1.5 font-label-sm text-label-sm text-secondary font-semibold">
                  <span className="material-symbols-outlined text-[15px]">auto_awesome</span>
                  AI-Powered Co-Founder &amp; Venture Engine
                </span>
                <span className="w-1 h-1 rounded-full bg-outline-variant"></span>
                <span className="font-code-sm text-code-sm px-2 py-0.5 rounded-full bg-surface-container text-on-surface-variant font-medium">
                  Cohort Alpha '25 Live
                </span>
              </div>

              {/* Main Headline */}
              <h1 className="font-display-hero text-display-hero text-primary max-w-4xl tracking-tight mb-4">
                Where Ideas Become Ventures
              </h1>

              {/* Subtitle */}
              <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl mb-8">
                Assemble high-conviction founding teams, validate synergy through blind challenge trials, and unlock
                early-stage capital.
              </p>

              {/* CTA Action Row */}
              <div className="flex flex-wrap items-center justify-center gap-space-md mb-16">
                <Link
                  to="/auth"
                  className="inline-flex items-center justify-center gap-2 h-11 px-6 rounded-lg bg-primary text-on-primary font-title-md text-title-md shadow-md hover:bg-primary-container transition-all hover:translate-y-[-1px]"
                >
                  <span>Launch Venture Brief</span>
                  <span className="material-symbols-outlined text-[18px]">arrow_forward</span>
                </Link>
                <a
                  href="#flywheel"
                  className="inline-flex items-center justify-center gap-2 h-11 px-6 rounded-lg bg-surface-container-lowest text-on-surface font-title-md text-title-md shadow-sm hover:bg-surface-container-low transition-all"
                >
                  <span className="material-symbols-outlined text-secondary text-[20px]">explore</span>
                  <span>Explore How It Works</span>
                </a>
              </div>

              {/* Hero Preview Graphic: Candidate Synergy Console */}
              <div
                className="w-full max-w-5xl rounded-xl bg-surface-container-lowest p-6 lg:p-8 shadow-xl text-left relative"
                id="arena-preview"
              >
                <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-6 border-b border-surface-container">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-secondary/10 flex items-center justify-center">
                      <span className="material-symbols-outlined text-secondary text-[24px]">verified_user</span>
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-title-md text-title-md text-primary font-semibold">
                          Challenge Arena: Cohort Alpha-7
                        </span>
                        <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse"></span>
                          Instant Verified
                        </span>
                      </div>
                      <p className="font-body-sm text-body-sm text-on-surface-variant">
                        Autonomous 48-Hour Execution Sprint • Blind ID:{' '}
                        <span className="font-code-sm text-code-sm text-primary">#VF-8492-EXEC</span>
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="font-code-sm text-code-sm px-3 py-1 rounded bg-surface-container text-on-surface font-medium">
                      Sprint Time: 41h 28m left
                    </span>
                    <div className="px-3 py-1 rounded bg-primary text-on-primary font-code-sm text-code-sm font-semibold tracking-wide">
                      CONFIDENTIAL
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                  {/* Left: Synergy Metric & Breakdown */}
                  <div className="lg:col-span-5 rounded-lg bg-surface-container-low p-5 flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <span className="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider">
                          Algorithmic Fit
                        </span>
                        <span className="font-code-sm text-code-sm text-secondary font-semibold">
                          99.2% Confidence
                        </span>
                      </div>
                      <div className="flex items-baseline gap-2 mb-4">
                        <span className="font-display-hero text-display-hero text-primary font-bold">96.4%</span>
                        <span className="font-title-md text-title-md text-secondary font-semibold">Synergy Index</span>
                      </div>
                      <p className="font-body-sm text-body-sm text-on-surface-variant mb-6">
                        Exceptional complementary cognitive vectors across Distributed Systems Architecture and B2B
                        Enterprise Go-To-Market strategy.
                      </p>
                    </div>
                    <div className="space-y-3 pt-4 bg-surface-container-lowest/60 rounded-lg p-3.5">
                      <div className="flex items-center justify-between text-body-sm font-body-sm">
                        <span className="text-on-surface">Complementary Quotient</span>
                        <span className="font-code-sm font-semibold text-primary">98 / 100</span>
                      </div>
                      <div className="w-full bg-surface-container h-1.5 rounded-full overflow-hidden">
                        <div className="bg-secondary h-full rounded-full" style={{ width: '98%' }}></div>
                      </div>
                      <div className="flex items-center justify-between text-body-sm font-body-sm pt-1">
                        <span className="text-on-surface">Stress Execution Concordance</span>
                        <span className="font-code-sm font-semibold text-primary">94 / 100</span>
                      </div>
                      <div className="w-full bg-surface-container h-1.5 rounded-full overflow-hidden">
                        <div className="bg-secondary h-full rounded-full" style={{ width: '94%' }}></div>
                      </div>
                    </div>
                  </div>

                  {/* Center: Radar Balance Visual */}
                  <div className="lg:col-span-4 rounded-lg bg-surface-container-lowest p-5 shadow-sm flex flex-col items-center justify-between border border-surface-container">
                    <div className="w-full flex items-center justify-between">
                      <span className="font-title-md text-title-md text-primary font-semibold">Archetype Radar</span>
                      <span className="font-label-sm text-label-sm text-secondary uppercase font-semibold">
                        Tech / GTM Balance
                      </span>
                    </div>

                    {/* SVG Radar Graphic */}
                    <div className="relative w-48 h-48 my-2 flex items-center justify-center">
                      <svg className="w-full h-full text-surface-container" viewBox="0 0 200 200">
                        <polygon
                          fill="none"
                          points="100,20 176,55 176,145 100,180 24,145 24,55"
                          stroke="currentColor"
                          strokeWidth="1"
                        />
                        <polygon
                          fill="none"
                          points="100,50 148,72 148,128 100,150 52,128 52,72"
                          stroke="currentColor"
                          strokeWidth="1"
                        />
                        <polygon
                          fill="none"
                          points="100,75 124,86 124,114 100,125 76,114 76,86"
                          stroke="currentColor"
                          strokeWidth="1"
                        />
                        <line stroke="currentColor" strokeDasharray="2 2" strokeWidth="1" x1="100" x2="100" y1="20" y2="180" />
                        <line stroke="currentColor" strokeDasharray="2 2" strokeWidth="1" x1="24" x2="176" y1="55" y2="145" />
                        <line stroke="currentColor" strokeDasharray="2 2" strokeWidth="1" x1="24" x2="176" y1="145" y2="55" />
                        <polygon
                          fill="#006972"
                          fillOpacity="0.25"
                          points="100,32 165,70 152,135 100,165 42,130 38,62"
                          stroke="#006972"
                          strokeWidth="2"
                        />
                        <circle cx="100" cy="32" fill="#006972" r="3.5" />
                        <circle cx="165" cy="70" fill="#006972" r="3.5" />
                        <circle cx="152" cy="135" fill="#006972" r="3.5" />
                        <circle cx="100" cy="165" fill="#006972" r="3.5" />
                        <circle cx="42" cy="130" fill="#006972" r="3.5" />
                        <circle cx="38" cy="62" fill="#006972" r="3.5" />
                      </svg>
                      <span className="absolute top-0 font-code-sm text-[10px] text-on-surface-variant font-semibold">
                        Arch
                      </span>
                      <span className="absolute right-0 font-code-sm text-[10px] text-on-surface-variant font-semibold">
                        GTM
                      </span>
                      <span className="absolute bottom-0 font-code-sm text-[10px] text-on-surface-variant font-semibold">
                        Product
                      </span>
                      <span className="absolute left-0 font-code-sm text-[10px] text-on-surface-variant font-semibold">
                        Ops
                      </span>
                    </div>

                    <div className="w-full flex items-center justify-between text-body-sm font-body-sm text-on-surface-variant">
                      <span>Dynamic equilibrium</span>
                      <span className="font-code-sm font-semibold text-secondary">Optimal 1:1.08</span>
                    </div>
                  </div>

                  {/* Right: Blind Matched Founder Profiles */}
                  <div className="lg:col-span-3 flex flex-col justify-between gap-3">
                    <div className="rounded-lg bg-surface-container-low p-4 shadow-sm">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-label-sm text-label-sm font-bold text-primary">Founder Alpha (Blind)</span>
                        <span className="font-code-sm text-[11px] px-1.5 py-0.5 rounded bg-surface-container-highest text-on-surface font-medium">
                          9.8/10 Tech
                        </span>
                      </div>
                      <div className="font-body-sm text-body-sm text-on-surface-variant mb-2">
                        Ex-Infra Lead • 8 Yrs Distributed Systems • 2 Prior Exits
                      </div>
                      <div className="flex flex-wrap gap-1">
                        <span className="font-code-sm text-[10px] px-2 py-0.5 rounded-full bg-surface-container-lowest text-on-surface">
                          Rust
                        </span>
                        <span className="font-code-sm text-[10px] px-2 py-0.5 rounded-full bg-surface-container-lowest text-on-surface">
                          Distributed AI
                        </span>
                      </div>
                    </div>

                    <div className="rounded-lg bg-surface-container-low p-4 shadow-sm">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-label-sm text-label-sm font-bold text-primary">Founder Beta (Blind)</span>
                        <span className="font-code-sm text-[11px] px-1.5 py-0.5 rounded bg-surface-container-highest text-on-surface font-medium">
                          9.6/10 GTM
                        </span>
                      </div>
                      <div className="font-body-sm text-body-sm text-on-surface-variant mb-2">
                        Enterprise PLG Strategist • Scaled $0M → $14M ARR
                      </div>
                      <div className="flex flex-wrap gap-1">
                        <span className="font-code-sm text-[10px] px-2 py-0.5 rounded-full bg-surface-container-lowest text-on-surface">
                          Enterprise GTM
                        </span>
                        <span className="font-code-sm text-[10px] px-2 py-0.5 rounded-full bg-surface-container-lowest text-on-surface">
                          Category Design
                        </span>
                      </div>
                    </div>

                    <Link
                      to="/auth"
                      className="rounded-lg bg-primary-container p-3.5 text-on-primary flex items-center justify-between hover:bg-primary transition-colors"
                    >
                      <div className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-secondary-fixed text-[18px]">lock_open</span>
                        <span className="font-label-md text-label-md">Mutual reveal ready</span>
                      </div>
                      <span className="font-code-sm text-code-sm text-secondary-fixed font-bold">Inspect →</span>
                    </Link>
                  </div>
                </div>
              </div>
            </section>
          </div>

          {/* 2. The 5-Step Loop Section (Flywheel) */}
          <section className="w-full bg-surface-container-low py-20" id="flywheel">
            <div className="max-w-7xl mx-auto px-6 lg:px-12">
              <div className="text-center max-w-3xl mx-auto mb-16">
                <span className="font-label-md text-label-md uppercase tracking-wider text-secondary font-bold mb-2 block">
                  System Architecture
                </span>
                <h2 className="font-headline-lg text-headline-lg text-primary mb-3 font-bold">
                  The Venture Formation Flywheel
                </h2>
                <p className="font-body-lg text-body-lg text-on-surface-variant">
                  A continuous, high-fidelity engine transforming raw concept theses into funded, execution-tested
                  corporate entities.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
                <div className="hidden md:block absolute top-12 left-[10%] right-[10%] h-0.5 bg-surface-container-highest z-0"></div>

                {[
                  {
                    step: '01',
                    title: 'Idea',
                    tag: 'Prompt-to-Thesis',
                    desc: 'Deconstruct abstract visions into rigorous market theses and target role architectures in minutes.',
                    badge: 'Role Matrix Gen',
                  },
                  {
                    step: '02',
                    title: 'Team Arena',
                    tag: 'Archetype Matching',
                    desc: 'Cross-match psychological and cognitive archetypes to forge complementary co-founder dyads.',
                    badge: 'Cognitive Delta < 0.12',
                  },
                  {
                    step: '03',
                    title: 'Challenge',
                    tag: '48h Live Sprint',
                    desc: 'Co-founders tackle live real-world problem vectors under time constraint to test execution velocity.',
                    badge: 'Simulated Crisis Tests',
                  },
                  {
                    step: '04',
                    title: 'Blind Scores',
                    tag: 'Multi-Vector Eval',
                    desc: 'Unbiased AI rubric scoring code output, strategic alignment, and dispute resolution behavior.',
                    badge: 'Zero-Bias Protocol',
                  },
                  {
                    step: '05',
                    title: 'Funding',
                    tag: 'Syndicate Matching',
                    desc: 'Direct matching with pre-seed venture syndicates and angel networks backed by verified sprint logs.',
                    badge: 'Cap Table Auto-Wire',
                  },
                ].map((item, idx) => (
                  <div
                    key={item.step}
                    className="relative z-10 rounded-xl bg-surface-container-lowest p-5 shadow-sm flex flex-col items-center text-center group hover:shadow-md transition-all"
                  >
                    <div
                      className={`w-14 h-14 rounded-full flex items-center justify-center font-title-md text-title-md font-bold mb-4 shadow-sm group-hover:scale-105 transition-transform ${
                        idx % 2 === 0 ? 'bg-primary text-on-primary' : 'bg-secondary text-on-secondary'
                      }`}
                    >
                      {item.step}
                    </div>
                    <span className="font-title-md text-title-md text-primary font-bold mb-1">{item.title}</span>
                    <span className="font-label-sm text-label-sm text-secondary font-semibold mb-2">{item.tag}</span>
                    <p className="font-body-sm text-body-sm text-on-surface-variant">{item.desc}</p>
                    <div className="mt-4 pt-3 w-full text-center border-t border-surface-container">
                      <span className="font-code-sm text-[11px] text-on-surface-variant font-medium">{item.badge}</span>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-10 rounded-xl bg-surface-container-lowest p-4 max-w-2xl mx-auto flex items-center justify-center gap-3 text-center shadow-sm">
                <span className="material-symbols-outlined text-secondary animate-spin">sync</span>
                <span className="font-body-sm text-body-sm text-on-surface-variant">
                  <strong className="text-primary font-semibold">Continuous Evolution:</strong> Capital events trigger
                  subsequent hiring arenas, squad restructurings, or new spin-off venture theses.
                </span>
              </div>
            </div>
          </section>

          {/* 3. Three Feature Cards */}
          <section className="max-w-7xl mx-auto px-6 lg:px-12 py-20 w-full" id="features">
            <div className="flex flex-col md:flex-row md:items-end justify-between mb-12">
              <div>
                <span className="font-label-md text-label-md uppercase tracking-wider text-secondary font-bold mb-2 block">
                  Institutional Capabilities
                </span>
                <h2 className="font-headline-lg text-headline-lg text-primary tracking-tight font-bold">
                  Precision Venture Assembly
                </h2>
              </div>
              <p className="font-body-md text-body-md text-on-surface-variant max-w-md mt-4 md:mt-0">
                Engineered to remove pedigree bias, eliminate founder friction, and validate real-world operational
                chemistry before incorporation.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Feature Card 1 */}
              <div className="rounded-xl bg-surface-container-lowest p-6 shadow-md flex flex-col justify-between hover:shadow-lg transition-all group">
                <div>
                  <div className="w-12 h-12 rounded-lg bg-surface-container-low flex items-center justify-center text-secondary mb-6 group-hover:bg-secondary group-hover:text-on-secondary transition-colors">
                    <span className="material-symbols-outlined text-[24px]">group_work</span>
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-secondary-container/40 text-on-secondary-container font-semibold">
                      Cognitive Diversity
                    </span>
                  </div>
                  <h3 className="font-headline-sm text-headline-sm text-primary mb-3 font-bold">
                    AI Startup Team Arena
                  </h3>
                  <p className="font-body-md text-body-md text-on-surface-variant mb-6">
                    Automated team fit analysis balancing engineering, product, and GTM archetypes with real-time synergy
                    scoring and cognitive diversity metrics.
                  </p>
                </div>
                <div className="rounded-lg bg-surface-container-low p-3.5 space-y-2">
                  <div className="flex justify-between items-center text-body-sm font-body-sm">
                    <span className="text-on-surface">Archetype Balance</span>
                    <span className="font-code-sm font-semibold text-secondary">Balanced 34/33/33</span>
                  </div>
                  <div className="flex gap-1 h-1.5 w-full">
                    <div className="bg-primary h-full rounded-sm" style={{ width: '34%' }}></div>
                    <div className="bg-secondary h-full rounded-sm" style={{ width: '33%' }}></div>
                    <div className="bg-primary-container h-full rounded-sm" style={{ width: '33%' }}></div>
                  </div>
                  <span className="font-code-sm text-[11px] text-on-surface-variant block">
                    Zero overlap in decision paralysis vectors
                  </span>
                </div>
              </div>

              {/* Feature Card 2 */}
              <div className="rounded-xl bg-surface-container-lowest p-6 shadow-md flex flex-col justify-between hover:shadow-lg transition-all group">
                <div>
                  <div className="w-12 h-12 rounded-lg bg-surface-container-low flex items-center justify-center text-secondary mb-6 group-hover:bg-secondary group-hover:text-on-secondary transition-colors">
                    <span className="material-symbols-outlined text-[24px]">published_with_changes</span>
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-secondary-container/40 text-on-secondary-container font-semibold">
                      Resilience Layer
                    </span>
                  </div>
                  <h3 className="font-headline-sm text-headline-sm text-primary mb-3 font-bold">
                    Dynamic Team Restructuring
                  </h3>
                  <p className="font-body-md text-body-md text-on-surface-variant mb-6">
                    Seamless founder replacement protocol with contingency AI talent pools, instant cap-table
                    adjustments, and zero-loss knowledge handovers.
                  </p>
                </div>
                <div className="rounded-lg bg-surface-container-low p-3.5 space-y-2">
                  <div className="flex items-center justify-between text-body-sm font-body-sm">
                    <span className="text-on-surface">Replacement Latency</span>
                    <span className="font-code-sm font-semibold text-secondary">&lt; 14 Hours</span>
                  </div>
                  <div className="flex items-center gap-2 text-body-sm font-body-sm text-on-surface-variant">
                    <span className="material-symbols-outlined text-[16px] text-secondary">check_circle</span>
                    <span>Automated clean equity vesting restructures</span>
                  </div>
                  <span className="font-code-sm text-[11px] text-on-surface-variant block">
                    Context-aware repository summaries preserved
                  </span>
                </div>
              </div>

              {/* Feature Card 3 */}
              <div className="rounded-xl bg-surface-container-lowest p-6 shadow-md flex flex-col justify-between hover:shadow-lg transition-all group">
                <div>
                  <div className="w-12 h-12 rounded-lg bg-surface-container-low flex items-center justify-center text-secondary mb-6 group-hover:bg-secondary group-hover:text-on-secondary transition-colors">
                    <span className="material-symbols-outlined text-[24px]">attach_money</span>
                  </div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-secondary-container/40 text-on-secondary-container font-semibold">
                      Capital Acceleration
                    </span>
                  </div>
                  <h3 className="font-headline-sm text-headline-sm text-primary mb-3 font-bold">
                    Funding Discovery
                  </h3>
                  <p className="font-body-md text-body-md text-on-surface-variant mb-6">
                    Algorithmic angel and micro-VC matching based on verified challenge output and objective team
                    execution velocity rather than pedigree.
                  </p>
                </div>
                <div className="rounded-lg bg-surface-container-low p-3.5 space-y-2">
                  <div className="flex justify-between items-center text-body-sm font-body-sm">
                    <span className="text-on-surface">Investor Syndicate Match</span>
                    <span className="font-code-sm font-semibold text-secondary">42 Active Funds</span>
                  </div>
                  <div className="flex items-center gap-2 text-body-sm font-body-sm text-on-surface-variant">
                    <span className="material-symbols-outlined text-[16px] text-secondary">insights</span>
                    <span>Velocity telemetry shared automatically</span>
                  </div>
                  <span className="font-code-sm text-[11px] text-on-surface-variant block">
                    Pre-seed terms generated in 3.4 days avg
                  </span>
                </div>
              </div>
            </div>
          </section>

          {/* 4. WhatsApp Candidate Flow Strip */}
          <section className="w-full bg-[#128C7E]/10 py-16 relative overflow-hidden" id="whatsapp">
            <div className="max-w-7xl mx-auto px-6 lg:px-12">
              <div className="rounded-2xl bg-gradient-to-r from-[#075E54] to-[#128C7E] text-white p-8 lg:p-12 shadow-xl flex flex-col lg:flex-row items-center justify-between gap-10">
                <div className="max-w-xl">
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md mb-4 text-emerald-100">
                    <span className="material-symbols-outlined text-[18px]">chat</span>
                    <span className="font-label-md text-label-md font-semibold tracking-wide">
                      Zero Friction Onboarding
                    </span>
                  </div>
                  <h2 className="font-headline-lg text-headline-lg text-white mb-3 font-bold">
                    Candidates join through WhatsApp
                  </h2>
                  <p className="font-body-lg text-body-lg text-emerald-100 leading-relaxed mb-6">
                    Frictionless, conversational screening and challenge submissions directly via WhatsApp chat flow—no
                    lengthy portals or tedious resumes.
                  </p>
                  <div className="flex flex-wrap items-center gap-4 text-emerald-100 font-body-sm text-body-sm">
                    <div className="flex items-center gap-1.5">
                      <span className="material-symbols-outlined text-[16px] text-white">speed</span>
                      <span>Sub-3 minute onboarding</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <span className="material-symbols-outlined text-[16px] text-white">mic</span>
                      <span>Audio answers supported</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <span className="material-symbols-outlined text-[16px] text-white">code</span>
                      <span>Git repo linking</span>
                    </div>
                  </div>
                </div>

                {/* WhatsApp Chat simulation */}
                <div className="w-full lg:w-[420px] rounded-xl bg-[#EFEAE2] p-4 shadow-2xl text-stone-800">
                  <div className="flex items-center justify-between pb-3 mb-3 border-b border-stone-300">
                    <div className="flex items-center gap-2.5">
                      <div className="w-9 h-9 rounded-full bg-[#075E54] flex items-center justify-center text-white">
                        <span className="material-symbols-outlined text-[18px]">smart_toy</span>
                      </div>
                      <div>
                        <div className="font-title-md text-title-md text-stone-900 leading-tight font-semibold">
                          VentureForge Bot
                        </div>
                        <div className="font-code-sm text-[11px] text-[#128C7E] font-medium flex items-center gap-1">
                          <span className="w-1.5 h-1.5 rounded-full bg-[#25D366]"></span> Online • Verified Engine
                        </div>
                      </div>
                    </div>
                    <span className="material-symbols-outlined text-stone-500 text-[20px]">more_vert</span>
                  </div>

                  <div className="space-y-3">
                    <div className="max-w-[85%] rounded-lg rounded-tl-none bg-white p-3.5 shadow-sm text-left">
                      <p className="font-body-sm text-body-sm text-stone-800 leading-snug">
                        👋 <strong>VentureForge Bot:</strong> Welcome Alex! Your 48h Team Arena challenge scenario is
                        ready. Tap to accept.
                      </p>
                      <div className="flex items-center justify-between mt-2 pt-1 text-[10px] text-stone-400 font-code-sm">
                        <span>Vector: Distributed Systems #702</span>
                        <span>10:42 AM</span>
                      </div>
                    </div>

                    <div className="flex flex-col gap-1.5 pl-2">
                      <Link
                        to="/auth?role=worker"
                        className="w-full py-2 px-3 rounded-md bg-white hover:bg-stone-50 text-[#00a884] font-title-md text-[13px] font-semibold text-center shadow-sm border border-stone-200 transition-colors flex items-center justify-center gap-1"
                      >
                        <span className="material-symbols-outlined text-[16px]">check_circle</span>
                        Accept Challenge (48h Clock)
                      </Link>
                      <button className="w-full py-1.5 px-3 rounded-md bg-white/70 hover:bg-white text-stone-600 font-body-sm text-[12px] text-center shadow-xs transition-colors">
                        Preview Challenge Constraints
                      </button>
                    </div>

                    <div className="max-w-[80%] ml-auto rounded-lg rounded-tr-none bg-[#D9FDD3] p-2.5 shadow-sm text-left">
                      <p className="font-body-sm text-body-sm text-stone-800">
                        Accepted! Syncing GitHub token and joining private arena chamber.
                      </p>
                      <div className="flex items-center justify-end gap-1 mt-1 text-[10px] text-stone-400 font-code-sm">
                        <span>10:43 AM</span>
                        <span className="material-symbols-outlined text-[13px] text-[#53bdeb]">done_all</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* 5. Live Cohort Ticker */}
          <section className="max-w-7xl mx-auto px-6 lg:px-12 py-16 w-full">
            <div className="rounded-xl bg-surface-container-low p-6 lg:p-8 flex flex-col md:flex-row items-center justify-between gap-6 shadow-sm">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-lg bg-surface-container-lowest flex items-center justify-center text-primary shadow-xs">
                  <span className="material-symbols-outlined text-[26px]">model_training</span>
                </div>
                <div>
                  <h4 className="font-title-md text-title-md text-primary font-semibold">Live Arena Cohort Status</h4>
                  <p className="font-body-sm text-body-sm text-on-surface-variant">
                    Real-time venture forming nodes across 14 geographic zones.
                  </p>
                </div>
              </div>
              <div className="flex flex-wrap items-center gap-6">
                <div className="text-right">
                  <div className="font-headline-sm text-headline-sm text-primary font-bold">184</div>
                  <div className="font-label-sm text-label-sm text-on-surface-variant">Active Sprints</div>
                </div>
                <div className="w-px h-8 bg-surface-container-highest"></div>
                <div className="text-right">
                  <div className="font-headline-sm text-headline-sm text-secondary font-bold">$12.4M</div>
                  <div className="font-label-sm text-label-sm text-on-surface-variant">Syndicate Capital Committed</div>
                </div>
                <div className="w-px h-8 bg-surface-container-highest"></div>
                <Link
                  to="/auth"
                  className="px-4 py-2 rounded-lg bg-primary text-on-primary font-label-md text-label-md hover:bg-primary-container transition-colors shadow-xs"
                >
                  Enter Arena
                </Link>
              </div>
            </div>
          </section>

          {/* Footer */}
          <footer className="w-full bg-surface-container-lowest border-t border-surface-container py-12">
            <div className="max-w-7xl mx-auto px-6 lg:px-12 flex flex-col md:flex-row items-center justify-between gap-8">
              <div className="flex flex-col items-center md:items-start gap-2">
                <div className="flex items-center gap-3">
                  <img
                    alt="VentureForge AI Logo"
                    className="w-8 h-8 rounded-md object-contain"
                    src="https://lh3.googleusercontent.com/aida/AEtjO1UFGfu5Xb2n4cvQa09mVmUxLW2NXOMyJIZibjDBXaBIcdR3BFaFg04_p49080Tb4xi6EIRQFTKFc6QnPtw9uxJwaBqQwoK1K2NkFKQreqVlSWGs0znR_2OPX25UQZZ3LcnlfbGsRkoaIdb12hFfIaP6lEGbMxaI9JZHoA_syD-aVxcKROl3Is-0ePC57cHtn18ghJQ5zbDeC1SU5mOze0yxgAiy6OXTdWaN2PzJoYjeNUsQwggJwkHY2ID_"
                  />
                  <span className="font-title-md text-title-md text-primary font-bold tracking-tight">
                    VentureForge AI
                  </span>
                </div>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Where Ideas Become Ventures</p>
              </div>

              <div className="flex flex-wrap items-center justify-center gap-6 text-on-surface-variant font-body-sm text-body-sm">
                <a className="hover:text-primary transition-colors" href="#flywheel">
                  How it Works
                </a>
                <a className="hover:text-primary transition-colors" href="#arena-preview">
                  Challenge Arena
                </a>
                <Link className="hover:text-primary transition-colors" to="/investor/dashboard">
                  Investor Network
                </Link>
                <Link className="hover:text-primary transition-colors" to="/worker/dashboard">
                  Talent Network
                </Link>
                <Link className="hover:text-primary transition-colors" to="/founder/dashboard">
                  Founders
                </Link>
              </div>

              <div className="font-body-sm text-body-sm text-on-surface-variant text-center md:text-right">
                <span>© 2025 VentureForge AI Inc. All rights reserved.</span>
              </div>
            </div>
          </footer>
        </div>
      </main>
    </div>
  );
};
