import React, { useState } from 'react';
import { NavLink, Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const FounderLayout = () => {
  const { user, switchRole, logout } = useAuth();
  const [profileOpen, setProfileOpen] = useState(false);
  const navigate = useNavigate();

  const navItems = [
    { name: 'Dashboard', path: '/founder/dashboard', icon: 'space_dashboard' },
    { name: 'Startup', path: '/founder/startup', icon: 'domain' },
    { name: 'Team Arena', path: '/founder/arena', icon: 'groups' },
    { name: 'Challenge', path: '/founder/challenge', icon: 'flag' },
    { name: 'Restructuring', path: '/founder/restructuring', icon: 'schema' },
    { name: 'Funding', path: '/founder/funding', icon: 'payments' },
    { name: 'Financials', path: '/founder/financial', icon: 'account_balance_wallet' },
    { name: 'Proof of Work', path: '/founder/proofwork', icon: 'fact_check' },
  ];

  const handleRoleChange = async (role) => {
    await switchRole(role);
    setProfileOpen(false);
    if (role === 'investor') navigate('/investor/dashboard');
    else if (role === 'worker') navigate('/worker/dashboard');
  };

  return (
    <div className="bg-background min-h-screen font-body-md text-body-md text-on-surface antialiased">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-72 bg-surface-container-lowest shadow-[0_1px_8px_rgba(0,0,0,0.04)] z-50 flex flex-col justify-between py-space-lg">
        <div className="flex flex-col gap-space-lg px-space-lg">
          <Link to="/" className="flex flex-col gap-space-xs group">
            <div className="flex items-center gap-space-sm">
              <div className="w-8 h-8 rounded-lg bg-primary-container flex items-center justify-center text-on-primary shadow-sm group-hover:scale-105 transition-transform">
                <span className="material-symbols-outlined text-[20px]">rocket_launch</span>
              </div>
              <span className="font-headline-sm text-headline-sm text-on-surface tracking-tight font-bold">
                VentureForge AI
              </span>
            </div>
            <p className="font-label-sm text-label-sm text-on-surface-variant pl-10 leading-tight">
              Where Ideas Become Ventures
            </p>
          </Link>

          <nav className="flex flex-col gap-space-xs pt-space-sm">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-space-sm px-space-md py-space-sm rounded-lg transition-colors ${
                    isActive
                      ? 'bg-primary-container text-on-primary font-title-md shadow-sm'
                      : 'text-on-surface-variant font-label-md text-label-md hover:bg-surface-container-high hover:text-on-surface'
                  }`
                }
              >
                <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
                <span>{item.name}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="px-space-lg flex flex-col gap-space-sm">
          <div className="p-space-md bg-surface-container-low rounded-xl flex items-center justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm text-on-surface-variant">Active Cohort</span>
              <span className="font-label-md text-label-md text-on-surface font-semibold">
                {user?.cohort || "Alpha Batch '25"}
              </span>
            </div>
            <span className="w-2.5 h-2.5 rounded-full bg-secondary animate-pulse" title="Connected"></span>
          </div>
        </div>
      </aside>

      {/* Top Header */}
      <div className="pl-72">
        <header className="fixed top-0 left-72 right-0 h-16 bg-surface-container-lowest/80 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)] z-40 flex items-center justify-between px-space-gutter">
          <div className="flex items-center gap-space-md flex-1 max-w-md">
            <div className="relative w-full">
              <span className="material-symbols-outlined absolute left-space-sm top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px]">
                search
              </span>
              <input
                className="w-full h-10 pl-9 pr-space-md rounded-lg bg-surface-container-low text-on-surface placeholder:text-outline text-body-sm font-body-sm focus:outline-none focus:ring-1 focus:ring-secondary transition-all"
                placeholder="Search cohort, ventures, metrics..."
                type="text"
              />
            </div>
            <div className="hidden sm:flex items-center gap-space-xs px-space-sm py-1 rounded-full bg-surface-container text-on-surface-variant font-label-sm text-label-sm shrink-0">
              <span className="material-symbols-outlined text-[14px] text-secondary">sync_alt</span>
              <span>Cohort Status: Live</span>
            </div>
          </div>

          <div className="flex items-center gap-space-md">
            <div className="px-space-sm py-1 rounded-full bg-tertiary-fixed text-on-tertiary-fixed-variant font-label-sm text-label-sm flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-on-tertiary-container"></span>
              <span>Demo data</span>
            </div>

            <button
              aria-label="Notifications"
              className="w-9 h-9 rounded-lg flex items-center justify-center text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-colors relative"
              type="button"
            >
              <span className="material-symbols-outlined text-[20px]">notifications</span>
              <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-error"></span>
            </button>

            {/* User pill & Role dropdown */}
            <div className="relative">
              <button
                onClick={() => setProfileOpen(!profileOpen)}
                className="flex items-center gap-space-sm pl-space-xs p-1 rounded-lg hover:bg-surface-container-low transition-colors"
              >
                <div className="flex flex-col items-end hidden md:flex">
                  <span className="font-label-md text-label-md text-on-surface font-semibold leading-tight">
                    {user?.name || 'Alex Mercer'}
                  </span>
                  <span className="font-label-sm text-label-sm text-on-surface-variant">Founder / Cohort Alpha</span>
                </div>
                <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-on-primary">
                  <span className="material-symbols-outlined text-[18px]">person</span>
                </div>
              </button>

              {profileOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-xl bg-surface-container-lowest shadow-xl border border-surface-container-high py-2 z-50">
                  <div className="px-4 py-2 border-b border-surface-container">
                    <p className="font-label-md text-label-md font-semibold text-on-surface">{user?.name}</p>
                    <p className="font-body-sm text-body-sm text-on-surface-variant truncate">{user?.email}</p>
                    <span className="inline-block mt-1 px-2 py-0.5 rounded bg-primary-container text-on-primary text-[11px] font-semibold">
                      Founder Mode
                    </span>
                  </div>
                  <div className="py-1">
                    <span className="px-4 py-1 text-[11px] font-semibold text-outline uppercase tracking-wider block">
                      Switch Role View
                    </span>
                    <button
                      onClick={() => handleRoleChange('investor')}
                      className="w-full text-left px-4 py-2 text-body-sm hover:bg-surface-container flex items-center gap-2"
                    >
                      <span className="material-symbols-outlined text-[18px] text-secondary">trending_up</span>
                      <span>Investor Portal</span>
                    </button>
                    <button
                      onClick={() => handleRoleChange('worker')}
                      className="w-full text-left px-4 py-2 text-body-sm hover:bg-surface-container flex items-center gap-2"
                    >
                      <span className="material-symbols-outlined text-[18px] text-secondary">badge</span>
                      <span>Worker / Talent Portal</span>
                    </button>
                  </div>
                  <div className="border-t border-surface-container pt-1">
                    <Link
                      to="/auth"
                      className="w-full text-left px-4 py-2 text-body-sm hover:bg-surface-container flex items-center gap-2 text-primary"
                    >
                      <span className="material-symbols-outlined text-[18px]">key</span>
                      <span>Auth & Account</span>
                    </Link>
                    <button
                      onClick={() => {
                        logout();
                        navigate('/auth');
                      }}
                      className="w-full text-left px-4 py-2 text-body-sm text-error hover:bg-error-container/20 flex items-center gap-2"
                    >
                      <span className="material-symbols-outlined text-[18px]">logout</span>
                      <span>Sign Out</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Content Area */}
        <main className="w-full pt-16 px-space-gutter pb-space-xl bg-background min-h-screen">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
