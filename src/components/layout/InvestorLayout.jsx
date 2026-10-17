import React, { useState } from 'react';
import { NavLink, Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const InvestorLayout = () => {
  const { user, switchRole, logout } = useAuth();
  const [profileOpen, setProfileOpen] = useState(false);
  const navigate = useNavigate();

  const navItems = [
    { name: 'Dashboard', path: '/investor/dashboard', icon: 'grid_view' },
    { name: 'Portfolio', path: '/investor/portfolio', icon: 'pie_chart' },
    { name: 'Startup Updates', path: '/investor/startup', icon: 'campaign' },
    { name: 'Financial Reports', path: '/investor/financial-report', icon: 'query_stats' },
    { name: 'Investment Terms', path: '/investor/investment-terms', icon: 'description' },
    { name: 'Discover Startups', path: '/investor/discover-startups', icon: 'explore' },
    { name: 'Settings', path: '/investor/settings', icon: 'settings' },
  ];

  const handleRoleChange = (role) => {
    switchRole(role);
    setProfileOpen(false);
    if (role === 'founder') navigate('/founder/dashboard');
    else if (role === 'worker') navigate('/worker/dashboard');
  };

  return (
    <div className="bg-background min-h-screen font-body-md text-body-md text-on-surface antialiased">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-screen w-64 bg-surface-container-low flex flex-col z-50 shadow-[0_1px_8px_rgba(0,0,0,0.04)] justify-between">
        <div className="flex flex-col">
          <Link to="/" className="h-16 flex items-center px-space-lg gap-space-sm group">
            <div className="w-9 h-9 rounded-lg bg-primary-container flex items-center justify-center group-hover:scale-105 transition-transform">
              <span className="material-symbols-outlined text-secondary text-[22px]">insights</span>
            </div>
            <div className="flex flex-col">
              <span className="font-title-md text-title-md text-on-surface leading-none tracking-tight font-semibold">
                VentureForge
              </span>
              <span className="font-label-sm text-label-sm text-secondary uppercase tracking-wider font-semibold mt-0.5">
                AI Intelligence
              </span>
            </div>
          </Link>

          <div className="px-space-md py-space-sm">
            <div className="bg-surface-container-high rounded-lg p-space-sm flex items-center justify-between">
              <div className="flex items-center gap-space-xs">
                <span className="material-symbols-outlined text-secondary text-[16px]">corporate_fare</span>
                <span className="font-label-sm text-label-sm text-on-surface font-semibold">
                  {user?.entity || 'Syndicate Alpha'}
                </span>
              </div>
              <span className="font-label-sm text-label-sm text-secondary font-semibold bg-surface-container-lowest px-1.5 py-0.5 rounded-full">
                Active
              </span>
            </div>
          </div>

          <nav className="flex-1 px-space-md py-space-sm space-y-1 overflow-y-auto">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-space-sm px-space-md py-2.5 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-primary-container text-on-primary font-semibold shadow-sm'
                      : 'text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface'
                  }`
                }
              >
                <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
                <span className="font-body-md text-body-md">{item.name}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="p-space-md bg-surface-container">
          <div className="bg-surface-container-lowest p-space-sm rounded-lg flex items-center justify-between">
            <div className="flex flex-col">
              <span className="font-label-sm text-label-sm text-on-surface-variant">Portfolio Engine</span>
              <span className="font-body-sm text-body-sm text-on-surface font-semibold">v2.4.8 Neural</span>
            </div>
            <span className="material-symbols-outlined text-secondary text-[20px]">auto_awesome</span>
          </div>
        </div>
      </aside>

      {/* Top Header */}
      <div className="pl-64">
        <header className="fixed top-0 left-64 right-0 h-16 bg-surface-container-lowest/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)] z-40 flex items-center justify-between px-space-lg">
          <div className="flex items-center gap-space-md flex-1 max-w-xl">
            <div className="relative w-full">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-outline text-[20px]">
                search
              </span>
              <input
                className="w-full h-10 pl-10 pr-space-md bg-surface-container-low rounded-lg font-body-sm text-body-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-secondary/30"
                placeholder="Search portfolio, startups, reports..."
                type="text"
              />
            </div>
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-surface-container-high text-on-surface font-label-sm text-label-sm whitespace-nowrap">
              <span className="w-1.5 h-1.5 rounded-full bg-secondary"></span>
              Demo Data
            </span>
          </div>

          <div className="flex items-center gap-space-md">
            <button
              className="relative p-2 rounded-lg text-on-surface-variant hover:bg-surface-container-low hover:text-on-surface transition-colors"
              type="button"
            >
              <span className="material-symbols-outlined text-[22px]">notifications</span>
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-error"></span>
            </button>
            <div className="h-6 w-px bg-surface-container-high"></div>

            {/* Profile Dropdown */}
            <div className="relative">
              <button
                onClick={() => setProfileOpen(!profileOpen)}
                className="flex items-center gap-space-sm pl-space-xs p-1 rounded-lg hover:bg-surface-container-low transition-colors"
              >
                <div className="flex flex-col text-right hidden sm:flex">
                  <span className="font-title-md text-body-md text-on-surface font-semibold leading-tight">
                    {user?.name || 'Marcus Vance'}
                  </span>
                  <div className="flex items-center justify-end gap-1 mt-0.5">
                    <span className="inline-block px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm font-semibold">
                      Investor / Angel Syndicate
                    </span>
                  </div>
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
                    <span className="inline-block mt-1 px-2 py-0.5 rounded bg-secondary-container text-on-secondary-container text-[11px] font-semibold">
                      Investor Mode
                    </span>
                  </div>
                  <div className="py-1">
                    <span className="px-4 py-1 text-[11px] font-semibold text-outline uppercase tracking-wider block">
                      Switch Role View
                    </span>
                    <button
                      onClick={() => handleRoleChange('founder')}
                      className="w-full text-left px-4 py-2 text-body-sm hover:bg-surface-container flex items-center gap-2"
                    >
                      <span className="material-symbols-outlined text-[18px] text-secondary">rocket_launch</span>
                      <span>Founder Portal</span>
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
        <main className="relative pt-16 bg-background w-full px-space-lg py-space-lg min-h-screen">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
