import React, { useState } from 'react';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
import { useAuth, DEMO_USERS } from '../../context/AuthContext';

export const AuthPage = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const initialMode = searchParams.get('mode') === 'login' ? 'login' : 'register';

  const [mode, setMode] = useState(initialMode); // 'login' | 'register'
  const [selectedRole, setSelectedRole] = useState('worker'); // 'founder' | 'worker' | 'investor'
  const [showPassword, setShowPassword] = useState(false);

  // Form states
  const [name, setName] = useState('Elena Vance');
  const [email, setEmail] = useState('elena.vance@startup.io');
  const [password, setPassword] = useState('VentureTitan#2025!');
  const [portfolioUrl, setPortfolioUrl] = useState('https://github.com/elena-vance-dist');
  const [experience, setExperience] = useState('Senior');
  const [whatsappEnabled, setWhatsappEnabled] = useState(true);
  const [termsAccepted, setTermsAccepted] = useState(true);

  // Skills tag manager
  const [skills, setSkills] = useState(['Distributed Systems', 'Rust', 'Go', 'System Architecture']);
  const [skillInput, setSkillInput] = useState('');

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const { login, signup, showToast } = useAuth();

  const handleAddSkill = (e) => {
    if (e.key === 'Enter' && skillInput.trim()) {
      e.preventDefault();
      if (!skills.includes(skillInput.trim())) {
        setSkills([...skills, skillInput.trim()]);
      }
      setSkillInput('');
    }
  };

  const handleRemoveSkill = (skillToRemove) => {
    setSkills(skills.filter((s) => s !== skillToRemove));
  };

  const calculateStrength = (pwd) => {
    if (!pwd) return 0;
    let score = 0;
    if (pwd.length >= 8) score += 25;
    if (/[A-Z]/.test(pwd)) score += 25;
    if (/[0-9]/.test(pwd)) score += 25;
    if (/[^A-Za-z0-9]/.test(pwd)) score += 25;
    return score;
  };

  const pwdStrength = calculateStrength(password);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please fill in email and password.');
      return;
    }

    if (mode === 'register' && !termsAccepted) {
      setError('Please accept the VentureForge Blind Protocol Terms to proceed.');
      return;
    }

    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
      if (mode === 'login') {
        login(email, password, selectedRole);
      } else {
        signup({
          name,
          email,
          role: selectedRole,
          skills,
          portfolioUrl,
          experience,
          whatsappEnabled,
        });
      }

      // Redirect to appropriate role dashboard
      if (selectedRole === 'founder') {
        navigate('/founder/dashboard');
      } else if (selectedRole === 'investor') {
        navigate('/investor/dashboard');
      } else {
        navigate('/worker/dashboard');
      }
    }, 600);
  };

  const handleQuickDemoLogin = (role) => {
    setSelectedRole(role);
    const demo = DEMO_USERS[role];
    setName(demo.name);
    setEmail(demo.email);
    login(demo.email, 'demo-token-bypass', role);

    if (role === 'founder') {
      navigate('/founder/dashboard');
    } else if (role === 'investor') {
      navigate('/investor/dashboard');
    } else {
      navigate('/worker/dashboard');
    }
  };

  return (
    <div className="bg-background font-body-md text-body-md text-on-surface antialiased min-h-screen flex flex-col justify-between">
      {/* Header */}
      <header className="fixed top-0 w-full z-50 bg-surface/80 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)]">
        <div className="h-16 max-w-7xl mx-auto px-6 lg:px-12 flex items-center justify-between gap-space-lg">
          <Link to="/" className="flex items-center gap-space-md group">
            <img
              alt="VentureForge AI Logo"
              className="h-8 w-auto object-contain group-hover:scale-105 transition-transform"
              src="https://lh3.googleusercontent.com/aida/AEtjO1UFGfu5Xb2n4cvQa09mVmUxLW2NXOMyJIZibjDBXaBIcdR3BFaFg04_p49080Tb4xi6EIRQFTKFc6QnPtw9uxJwaBqQwoK1K2NkFKQreqVlSWGs0znR_2OPX25UQZZ3LcnlfbGsRkoaIdb12hFfIaP6lEGbMxaI9JZHoA_syD-aVxcKROl3Is-0ePC57cHtn18ghJQ5zbDeC1SU5mOze0yxgAiy6OXTdWaN2PzJoYjeNUsQwggJwkHY2ID_"
            />
            <span className="font-title-md text-title-md text-on-surface tracking-tight font-semibold">
              VentureForge AI
            </span>
          </Link>
          <div className="flex items-center gap-space-md text-on-surface-variant font-body-sm text-body-sm">
            <span className="hidden sm:inline">Need assistance?</span>
            <a
              className="font-label-md text-label-md text-secondary hover:underline transition-colors"
              href="mailto:support@ventureforge.ai"
            >
              Contact Support
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="w-full pt-16 min-h-screen flex flex-col justify-between bg-background">
        <div className="flex flex-col w-full">
          <div className="relative w-full overflow-hidden py-space-xl px-6 lg:px-12 flex justify-center items-start">
            {/* Ambient Precision Glows */}
            <div className="pointer-events-none absolute -top-24 left-1/2 -translate-x-1/2 w-[720px] h-[360px] bg-gradient-to-b from-secondary/10 via-surface-variant/40 to-transparent blur-3xl opacity-60"></div>
            <div className="pointer-events-none absolute top-1/3 -right-48 w-96 h-96 bg-primary-fixed/30 rounded-full blur-3xl"></div>
            <div className="pointer-events-none absolute bottom-12 -left-48 w-96 h-96 bg-secondary-fixed/20 rounded-full blur-3xl"></div>

            <div className="relative w-full max-w-4xl flex flex-col gap-space-lg">
              {/* Quick 1-Click Demo Bar */}
              <div className="bg-surface-container-lowest p-3 sm:p-4 rounded-xl shadow-sm border border-secondary/20 flex flex-col sm:flex-row items-center justify-between gap-3">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-secondary text-[20px]">bolt</span>
                  <span className="font-label-md text-label-md font-semibold text-on-surface">
                    One-Click Demo Evaluator Access:
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => handleQuickDemoLogin('founder')}
                    className="px-3 py-1.5 rounded-lg bg-surface-container hover:bg-surface-container-high text-primary font-label-sm text-label-sm font-semibold flex items-center gap-1.5 transition-all shadow-xs"
                    type="button"
                  >
                    <span className="material-symbols-outlined text-[15px] text-secondary">rocket_launch</span>
                    <span>As Founder</span>
                  </button>
                  <button
                    onClick={() => handleQuickDemoLogin('investor')}
                    className="px-3 py-1.5 rounded-lg bg-surface-container hover:bg-surface-container-high text-primary font-label-sm text-label-sm font-semibold flex items-center gap-1.5 transition-all shadow-xs"
                    type="button"
                  >
                    <span className="material-symbols-outlined text-[15px] text-secondary">trending_up</span>
                    <span>As Investor</span>
                  </button>
                  <button
                    onClick={() => handleQuickDemoLogin('worker')}
                    className="px-3 py-1.5 rounded-lg bg-secondary text-on-secondary hover:opacity-90 font-label-sm text-label-sm font-semibold flex items-center gap-1.5 transition-all shadow-xs"
                    type="button"
                  >
                    <span className="material-symbols-outlined text-[15px]">badge</span>
                    <span>As Talent / Worker</span>
                  </button>
                </div>
              </div>

              {/* Mode Toggle (Sign In vs Register) & Stepper Badge */}
              <div className="flex flex-col md:flex-row md:items-end justify-between gap-space-md">
                <div>
                  <div className="flex items-center gap-space-sm mb-space-xs">
                    <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-secondary/10 text-secondary font-label-sm text-label-sm uppercase tracking-wider">
                      <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
                      {mode === 'register' ? 'Step 1 of 2: Formation' : 'Identity Verification'}
                    </span>
                    <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm">
                      Zero-Knowledge Auth
                    </span>
                  </div>
                  <h1 className="font-headline-lg text-headline-lg text-on-surface tracking-tight font-bold">
                    {mode === 'register' ? 'Create your VentureForge account' : 'Welcome back to VentureForge'}
                  </h1>
                  <p className="font-body-md text-body-md text-on-surface-variant mt-0.5">
                    {mode === 'register'
                      ? 'Join the autonomous co-founder & venture formation network.'
                      : 'Access your active cohort sprint arena and venture dossiers.'}
                  </p>
                </div>

                {/* Tab switch between Register & Login */}
                <div className="inline-flex p-1 rounded-xl bg-surface-container-low shadow-sm shrink-0 self-start md:self-auto">
                  <button
                    type="button"
                    onClick={() => setMode('register')}
                    className={`px-4 py-2 rounded-lg font-label-md text-label-md font-semibold transition-all ${
                      mode === 'register'
                        ? 'bg-surface-container-lowest text-primary shadow-sm'
                        : 'text-on-surface-variant hover:text-on-surface'
                    }`}
                  >
                    Register / Sign Up
                  </button>
                  <button
                    type="button"
                    onClick={() => setMode('login')}
                    className={`px-4 py-2 rounded-lg font-label-md text-label-md font-semibold transition-all ${
                      mode === 'login'
                        ? 'bg-surface-container-lowest text-primary shadow-sm'
                        : 'text-on-surface-variant hover:text-on-surface'
                    }`}
                  >
                    Sign In
                  </button>
                </div>
              </div>

              {/* Main Registration / Login Canvas */}
              <form
                onSubmit={handleSubmit}
                className="bg-surface-container-lowest rounded-xl p-6 sm:p-8 md:p-10 shadow-sm flex flex-col gap-space-xl"
              >
                {error && (
                  <div className="p-3.5 rounded-lg bg-error-container text-on-error-container font-body-sm text-body-sm flex items-center gap-2">
                    <span className="material-symbols-outlined text-[18px]">error</span>
                    <span>{error}</span>
                  </div>
                )}

                {/* SECTION 1: Credentials Form */}
                <section className="flex flex-col gap-space-md">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded-md bg-primary-container text-on-primary flex items-center justify-center font-label-sm text-label-sm font-semibold">
                        01
                      </span>
                      <h2 className="font-title-md text-title-md text-on-surface tracking-tight font-semibold">
                        Account Credentials
                      </h2>
                    </div>
                    <span className="font-code-sm text-code-sm text-on-surface-variant hidden sm:inline">
                      SSO & Web3 Auth available next
                    </span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md">
                    {/* Full Name (shown if registering) */}
                    {mode === 'register' && (
                      <div className="flex flex-col gap-1.5">
                        <label className="font-label-md text-label-md text-on-surface flex items-center justify-between">
                          <span>Full Legal Name</span>
                          <span className="text-secondary font-label-sm text-label-sm">Verified ID Ready</span>
                        </label>
                        <div className="relative flex items-center">
                          <span className="material-symbols-outlined absolute left-3.5 text-on-surface-variant pointer-events-none text-lg">
                            person
                          </span>
                          <input
                            className="w-full h-10 pl-10 pr-3.5 rounded-lg bg-surface-container-low text-on-surface font-body-md text-body-md shadow-sm focus:outline-none focus:ring-2 focus:ring-secondary/40"
                            placeholder="Elena Vance"
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                          />
                        </div>
                      </div>
                    )}

                    {/* Email Address */}
                    <div className={`flex flex-col gap-1.5 ${mode === 'login' ? 'md:col-span-2' : ''}`}>
                      <label className="font-label-md text-label-md text-on-surface">
                        Institutional / Work Email
                      </label>
                      <div className="relative flex items-center">
                        <span className="material-symbols-outlined absolute left-3.5 text-on-surface-variant pointer-events-none text-lg">
                          mail
                        </span>
                        <input
                          className="w-full h-10 pl-10 pr-3.5 rounded-lg bg-surface-container-low text-on-surface font-body-md text-body-md shadow-sm focus:outline-none focus:ring-2 focus:ring-secondary/40"
                          placeholder="elena.vance@startup.io"
                          type="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          required
                        />
                      </div>
                    </div>

                    {/* Password with Show/Hide & Strength */}
                    <div className="flex flex-col gap-1.5 md:col-span-2">
                      <div className="flex items-center justify-between">
                        <label className="font-label-md text-label-md text-on-surface">
                          Account Passkey / Password
                        </label>
                        {mode === 'register' && (
                          <span className="font-label-sm text-label-sm text-secondary font-medium">
                            Enterprise Strength: {pwdStrength}%
                          </span>
                        )}
                      </div>
                      <div className="relative flex items-center">
                        <span className="material-symbols-outlined absolute left-3.5 text-on-surface-variant pointer-events-none text-lg">
                          lock
                        </span>
                        <input
                          className="w-full h-10 pl-10 pr-10 rounded-lg bg-surface-container-low text-on-surface font-body-md text-body-md shadow-sm focus:outline-none focus:ring-2 focus:ring-secondary/40 tracking-wider"
                          placeholder="••••••••••••"
                          type={showPassword ? 'text' : 'password'}
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          required
                        />
                        <button
                          aria-label="Toggle password visibility"
                          className="absolute right-3 text-on-surface-variant hover:text-on-surface flex items-center p-1 rounded transition-colors"
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                        >
                          <span className="material-symbols-outlined text-lg">
                            {showPassword ? 'visibility_off' : 'visibility'}
                          </span>
                        </button>
                      </div>

                      {mode === 'register' && (
                        <>
                          {/* Password Strength Meter */}
                          <div className="grid grid-cols-4 gap-1.5 pt-1">
                            <div
                              className={`h-1.5 rounded-full ${
                                pwdStrength >= 25 ? 'bg-secondary' : 'bg-surface-container-high'
                              }`}
                            ></div>
                            <div
                              className={`h-1.5 rounded-full ${
                                pwdStrength >= 50 ? 'bg-secondary' : 'bg-surface-container-high'
                              }`}
                            ></div>
                            <div
                              className={`h-1.5 rounded-full ${
                                pwdStrength >= 75 ? 'bg-secondary' : 'bg-surface-container-high'
                              }`}
                            ></div>
                            <div
                              className={`h-1.5 rounded-full ${
                                pwdStrength === 100 ? 'bg-secondary' : 'bg-surface-container-high'
                              }`}
                            ></div>
                          </div>
                          <p className="font-body-sm text-body-sm text-on-surface-variant">
                            Includes uppercase, special character, numeral, and 8+ characters for blind key security.
                          </p>
                        </>
                      )}
                    </div>
                  </div>
                </section>

                {/* SECTION 2: Role Selection */}
                <section className="flex flex-col gap-space-md">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-6 h-6 rounded-md bg-primary-container text-on-primary flex items-center justify-center font-label-sm text-label-sm font-semibold">
                        02
                      </span>
                      <h2 className="font-title-md text-title-md text-on-surface tracking-tight font-semibold">
                        Select your primary ecosystem role
                      </h2>
                    </div>
                    <span className="font-label-sm text-label-sm text-on-surface-variant">
                      Changeable anytime in settings
                    </span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-space-md">
                    {/* 1. Founder Card */}
                    <div
                      onClick={() => setSelectedRole('founder')}
                      className={`role-card group relative p-space-md rounded-xl transition-all cursor-pointer flex flex-col justify-between shadow-sm min-h-[200px] border-2 ${
                        selectedRole === 'founder'
                          ? 'border-secondary bg-secondary/5 ring-1 ring-secondary shadow-md'
                          : 'border-transparent bg-surface-container-low hover:bg-surface-container'
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between mb-space-sm">
                          <div className="w-9 h-9 rounded-lg bg-surface-container-lowest text-primary flex items-center justify-center shadow-sm">
                            <span className="material-symbols-outlined text-xl">rocket_launch</span>
                          </div>
                          {selectedRole === 'founder' ? (
                            <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2 py-0.5 rounded-full bg-secondary text-on-secondary font-semibold">
                              <span className="material-symbols-outlined text-xs">check</span>Selected
                            </span>
                          ) : (
                            <div className="w-5 h-5 rounded-full bg-surface-container-highest flex items-center justify-center">
                              <span className="w-2 h-2 rounded-full bg-transparent"></span>
                            </div>
                          )}
                        </div>
                        <h3 className="font-title-md text-title-md text-on-surface mb-1 font-semibold">Founder</h3>
                        <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed mb-3">
                          Build a startup, assemble an aligned team, and discover verified early-stage funding.
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-1 mt-auto pt-2">
                        <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container-lowest text-on-surface-variant">
                          Idea to Venture
                        </span>
                        <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container-lowest text-on-surface-variant">
                          Cap Table
                        </span>
                      </div>
                    </div>

                    {/* 2. Worker / Talent Card */}
                    <div
                      onClick={() => setSelectedRole('worker')}
                      className={`role-card group relative p-space-md rounded-xl transition-all cursor-pointer flex flex-col justify-between shadow-sm min-h-[200px] border-2 ${
                        selectedRole === 'worker'
                          ? 'border-secondary bg-secondary/5 ring-1 ring-secondary shadow-md'
                          : 'border-transparent bg-surface-container-low hover:bg-surface-container'
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between mb-space-sm">
                          <div className="w-9 h-9 rounded-lg bg-surface-container-lowest text-secondary flex items-center justify-center shadow-sm">
                            <span className="material-symbols-outlined text-xl">badge</span>
                          </div>
                          {selectedRole === 'worker' ? (
                            <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2 py-0.5 rounded-full bg-secondary text-on-secondary font-semibold">
                              <span className="material-symbols-outlined text-xs">check</span>Selected
                            </span>
                          ) : (
                            <div className="w-5 h-5 rounded-full bg-surface-container-highest flex items-center justify-center">
                              <span className="w-2 h-2 rounded-full bg-transparent"></span>
                            </div>
                          )}
                        </div>
                        <h3 className="font-title-md text-title-md text-on-surface mb-1 font-semibold">
                          Worker / Talent
                        </h3>
                        <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed mb-3">
                          Build skills profile, join high-conviction teams, and prove abilities through blind
                          challenges.
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-1 mt-auto pt-2">
                        <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container-lowest text-on-surface-variant">
                          Blind Trials
                        </span>
                        <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container-lowest text-on-surface-variant">
                          Algorithmic Fit
                        </span>
                      </div>
                    </div>

                    {/* 3. Investor Card */}
                    <div
                      onClick={() => setSelectedRole('investor')}
                      className={`role-card group relative p-space-md rounded-xl transition-all cursor-pointer flex flex-col justify-between shadow-sm min-h-[200px] border-2 ${
                        selectedRole === 'investor'
                          ? 'border-secondary bg-secondary/5 ring-1 ring-secondary shadow-md'
                          : 'border-transparent bg-surface-container-low hover:bg-surface-container'
                      }`}
                    >
                      <div>
                        <div className="flex items-center justify-between mb-space-sm">
                          <div className="w-9 h-9 rounded-lg bg-surface-container-lowest text-primary flex items-center justify-center shadow-sm">
                            <span className="material-symbols-outlined text-xl">trending_up</span>
                          </div>
                          {selectedRole === 'investor' ? (
                            <span className="inline-flex items-center gap-1 font-label-sm text-label-sm px-2 py-0.5 rounded-full bg-secondary text-on-secondary font-semibold">
                              <span className="material-symbols-outlined text-xs">check</span>Selected
                            </span>
                          ) : (
                            <div className="w-5 h-5 rounded-full bg-surface-container-highest flex items-center justify-center">
                              <span className="w-2 h-2 rounded-full bg-transparent"></span>
                            </div>
                          )}
                        </div>
                        <h3 className="font-title-md text-title-md text-on-surface mb-1 font-semibold">Investor</h3>
                        <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed mb-3">
                          Follow authorized cohort updates, inspect blind audit scores, and syndicate term sheets.
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-1 mt-auto pt-2">
                        <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container-lowest text-on-surface-variant">
                          Verified Telemetry
                        </span>
                        <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-surface-container-lowest text-on-surface-variant">
                          Pre-seed Syndicates
                        </span>
                      </div>
                    </div>
                  </div>
                </section>

                {/* SECTION 3: Conditional Worker Profile Fields (shown if talent role) */}
                {selectedRole === 'worker' && mode === 'register' && (
                  <section className="flex flex-col gap-space-md p-space-lg rounded-xl bg-surface-container-low shadow-sm transition-all border border-secondary/20">
                    <div className="flex items-center justify-between pb-1">
                      <div className="flex items-center gap-2">
                        <span className="material-symbols-outlined text-secondary text-xl">badge</span>
                        <h3 className="font-title-md text-title-md text-on-surface font-semibold">
                          Worker Profile Details
                        </h3>
                        <span className="font-label-sm text-label-sm px-2 py-0.5 rounded bg-secondary/10 text-secondary font-medium">
                          Revealed for Talent Role
                        </span>
                      </div>
                      <span className="font-code-sm text-code-sm text-secondary font-medium hidden sm:inline-block">
                        Blind Fit Engine v4.2
                      </span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md">
                      {/* Skills Input with Interactive Chip Tags */}
                      <div className="flex flex-col gap-1.5 md:col-span-2">
                        <label className="font-label-md text-label-md text-on-surface flex items-center justify-between">
                          <span>Verified Core Competencies & Skills</span>
                          <span className="font-body-sm text-body-sm text-on-surface-variant">
                            Press Enter to add tags
                          </span>
                        </label>
                        <div className="min-h-12 p-2 rounded-lg bg-surface-container-lowest shadow-sm flex flex-wrap items-center gap-1.5 focus-within:ring-2 focus-within:ring-secondary/40">
                          {skills.map((skill) => (
                            <span
                              key={skill}
                              className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md bg-surface-container-high text-on-surface font-label-md text-label-md"
                            >
                              {skill}
                              <button
                                onClick={() => handleRemoveSkill(skill)}
                                className="text-on-surface-variant hover:text-error transition-colors flex items-center"
                                type="button"
                              >
                                <span className="material-symbols-outlined text-sm">close</span>
                              </button>
                            </span>
                          ))}
                          <input
                            className="flex-1 min-w-[120px] bg-transparent text-on-surface font-body-md text-body-md focus:outline-none px-2 py-1"
                            placeholder="Add skill and press enter..."
                            type="text"
                            value={skillInput}
                            onChange={(e) => setSkillInput(e.target.value)}
                            onKeyDown={handleAddSkill}
                          />
                        </div>
                      </div>

                      {/* Experience Level Segmented */}
                      <div className="flex flex-col gap-1.5">
                        <label className="font-label-md text-label-md text-on-surface">Experience Bracket</label>
                        <div className="grid grid-cols-4 gap-1 p-1 rounded-lg bg-surface-container-lowest shadow-sm h-10 items-center">
                          {['Junior', 'Mid', 'Senior', 'Founding'].map((lvl) => (
                            <button
                              key={lvl}
                              type="button"
                              onClick={() => setExperience(lvl)}
                              className={`h-8 rounded font-label-sm text-label-sm font-semibold flex items-center justify-center transition-all ${
                                experience === lvl
                                  ? 'bg-primary-container text-on-primary shadow-xs'
                                  : 'text-on-surface-variant hover:text-on-surface'
                              }`}
                            >
                              {lvl}
                            </button>
                          ))}
                        </div>
                        <span className="font-code-sm text-code-sm text-on-surface-variant">
                          5-8 yrs verifiable production experience
                        </span>
                      </div>

                      {/* Portfolio / GitHub URL */}
                      <div className="flex flex-col gap-1.5">
                        <label className="font-label-md text-label-md text-on-surface">
                          Portfolio / Proof of Work URL
                        </label>
                        <div className="relative flex items-center">
                          <span className="material-symbols-outlined absolute left-3.5 text-on-surface-variant pointer-events-none text-lg">
                            link
                          </span>
                          <input
                            className="w-full h-10 pl-10 pr-3.5 rounded-lg bg-surface-container-lowest text-on-surface font-body-md text-body-md shadow-sm focus:outline-none focus:ring-2 focus:ring-secondary/40"
                            placeholder="https://github.com/..."
                            type="url"
                            value={portfolioUrl}
                            onChange={(e) => setPortfolioUrl(e.target.value)}
                          />
                        </div>
                        <span className="font-code-sm text-code-sm text-on-surface-variant">
                          Direct repo analysis runs sandboxed blind review
                        </span>
                      </div>

                      {/* WhatsApp Sync Dispatch Integration */}
                      <div className="flex flex-col gap-2 md:col-span-2 pt-1">
                        <div className="p-3.5 rounded-lg bg-surface-container-lowest shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-surface-container-high flex items-center justify-center text-secondary">
                              <span className="material-symbols-outlined text-lg">chat</span>
                            </div>
                            <div>
                              <div className="flex items-center gap-2">
                                <span className="font-title-md text-title-md text-on-surface font-medium">
                                  Enable WhatsApp Challenge Screening Dispatch
                                </span>
                                <span className="w-2 h-2 rounded-full bg-secondary"></span>
                              </div>
                              <p className="font-body-sm text-body-sm text-on-surface-variant">
                                Receive automated 15-minute asynchronous async blind trials directly in chat.
                              </p>
                            </div>
                          </div>
                          <label className="relative inline-flex items-center cursor-pointer shrink-0">
                            <input
                              checked={whatsappEnabled}
                              onChange={(e) => setWhatsappEnabled(e.target.checked)}
                              className="sr-only peer"
                              type="checkbox"
                            />
                            <div className="w-11 h-6 bg-surface-container-highest peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-secondary"></div>
                          </label>
                        </div>
                      </div>
                    </div>
                  </section>
                )}

                {/* SECTION 4: Action Area & Compliance */}
                <section className="flex flex-col gap-space-md pt-2">
                  {/* Terms Agreement */}
                  {mode === 'register' && (
                    <div className="flex items-start gap-3">
                      <input
                        checked={termsAccepted}
                        onChange={(e) => setTermsAccepted(e.target.checked)}
                        className="w-4 h-4 mt-1 rounded text-primary focus:ring-secondary/40 cursor-pointer accent-primary"
                        id="terms-checkbox"
                        type="checkbox"
                      />
                      <label
                        className="font-body-sm text-body-sm text-on-surface cursor-pointer select-none"
                        for="terms-checkbox"
                      >
                        I agree to the{' '}
                        <a className="text-secondary font-semibold hover:underline" href="#">
                          VentureForge Blind Protocol Terms
                        </a>{' '}
                        and{' '}
                        <a className="text-secondary font-semibold hover:underline" href="#">
                          Privacy Charter
                        </a>
                        . Talent telemetry is processed via cryptographic zero-knowledge proofs before venture
                        presentation.
                      </label>
                    </div>
                  )}

                  {/* CTAs */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-space-md pt-2">
                    <button
                      type="button"
                      onClick={() => setMode(mode === 'register' ? 'login' : 'register')}
                      className="order-2 sm:order-1 font-label-md text-label-md text-on-surface-variant hover:text-on-surface transition-colors flex items-center gap-1"
                    >
                      {mode === 'register' ? (
                        <>
                          Already have an account?{' '}
                          <span className="text-secondary font-semibold hover:underline">Sign in</span>
                        </>
                      ) : (
                        <>
                          Don't have an account yet?{' '}
                          <span className="text-secondary font-semibold hover:underline">Create account</span>
                        </>
                      )}
                    </button>

                    <button
                      className="order-1 sm:order-2 px-6 h-11 rounded-lg bg-primary-container text-on-primary font-title-md text-title-md font-semibold hover:bg-on-background transition-all flex items-center justify-center gap-2 shadow-sm group active:scale-[0.99] disabled:opacity-50"
                      type="submit"
                      disabled={isLoading}
                    >
                      {isLoading ? (
                        <>
                          <span className="material-symbols-outlined text-lg animate-spin">progress_activity</span>
                          <span>Verifying Identity...</span>
                        </>
                      ) : mode === 'register' ? (
                        <>
                          <span>Continue to Onboarding Arena</span>
                          <span className="material-symbols-outlined text-lg transition-transform group-hover:translate-x-1">
                            arrow_forward
                          </span>
                        </>
                      ) : (
                        <>
                          <span>Sign In to {selectedRole.toUpperCase()} Workspace</span>
                          <span className="material-symbols-outlined text-lg transition-transform group-hover:translate-x-1">
                            arrow_forward
                          </span>
                        </>
                      )}
                    </button>
                  </div>
                </section>
              </form>

              {/* Trust Badges & Institutional Footnote */}
              <div className="flex flex-wrap items-center justify-center gap-x-space-lg gap-y-space-xs text-on-surface-variant font-label-sm text-label-sm py-space-sm opacity-80">
                <span className="flex items-center gap-1.5">
                  <span className="material-symbols-outlined text-sm text-secondary">verified_user</span>
                  SOC2 Type II Ready
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="material-symbols-outlined text-sm text-secondary">lock</span>
                  Zero-Knowledge Talent Audit
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="material-symbols-outlined text-sm text-secondary">sync</span>
                  Sub-second Formation Sync
                </span>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full bg-surface-container-low shadow-[0_1px_8px_rgba(0,0,0,0.02)] py-space-xl">
        <div className="max-w-7xl mx-auto px-6 lg:px-12 flex flex-col md:flex-row items-center justify-between gap-space-md text-on-surface-variant font-body-sm text-body-sm">
          <div className="flex items-center gap-space-sm">
            <span className="font-label-md text-label-md font-semibold text-on-surface">VentureForge AI</span>
            <span>© 2025 All rights reserved. Precision venture intelligence.</span>
          </div>
          <div className="flex items-center gap-space-lg">
            <a className="hover:text-on-surface transition-colors" href="#">
              Privacy Policy
            </a>
            <a className="hover:text-on-surface transition-colors" href="#">
              Terms of Service
            </a>
            <a className="hover:text-on-surface transition-colors" href="#">
              Security & Compliance
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};
