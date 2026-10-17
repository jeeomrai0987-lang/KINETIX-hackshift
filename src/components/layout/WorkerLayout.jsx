import React, { useState } from 'react';
import { NavLink, Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const WorkerLayout = () => {
  const { user, switchRole, logout } = useAuth();
  const [profileOpen, setProfileOpen] = useState(false);
  const navigate = useNavigate();

  const navItems = [
    { name: 'Dashboard', path: '/worker/dashboard', icon: 'grid_view' },
    { name: 'My Profile', path: '/worker/profile', icon: 'person' },
    { name: 'Opportunities', path: '/worker/opportunities', icon: 'explore' },
    { name: 'Invitations', path: '/worker/invitations', icon: 'mail' },
    { name: 'Proof-of-Work Reports', path: '/worker/proof-of-work', icon: 'fact_check' },
    { name: 'Settings', path: '/worker/settings', icon: 'settings' },
  ];

  const handleRoleChange = (role) => {
    switchRole(role);
    setProfileOpen(false);
    if (role === 'founder') navigate('/founder/dashboard');
    else if (role === 'investor') navigate('/investor/dashboard');
  };

  return (
    <div className="bg-surface min-h-screen font-body-md text-body-md text-on-surface antialiased">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 h-full w-64 bg-surface-container-lowest shadow-[0_1px_8px_rgba(0,0,0,0.04)] z-50 flex flex-col justify-between">
        <div className="flex flex-col">
          <Link to="/" className="h-16 px-space-lg flex items-center gap-space-sm group">
            <div className="w-8 h-8 rounded-lg bg-primary-container flex items-center justify-center text-on-primary shadow-sm group-hover:scale-105 transition-transform">
              <span className="material-symbols-outlined text-[20px]">hub</span>
            </div>
            <div className="flex flex-col">
              <span className="font-title-md text-title-md text-on-surface tracking-tight font-bold leading-none">
                VentureForge
              </span>
              <span className="font-label-sm text-label-sm text-secondary font-medium tracking-tight mt-0.5">
                AI WORKER PORTAL
              </span>
            </div>
          </Link>

          <div className="px-space-md py-space-sm">
            <nav className="flex flex-col gap-space-xs">
              {navItems.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-space-sm px-space-md py-space-sm rounded-lg transition-colors ${
                      isActive
                        ? 'bg-primary-container text-on-primary font-title-md shadow-sm'
                        : 'text-on-surface-variant hover:bg-surface-container-low hover:text-on-surface'
                    }`
                  }
                >
                  <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
                  <span className="font-title-md text-title-md">{item.name}</span>
                </NavLink>
              ))}
            </nav>
          </div>
        </div>

        <div className="p-space-md m-space-md rounded-xl bg-surface-container-low">
          <div className="flex items-center gap-space-xs text-secondary mb-space-xs">
            <span className="material-symbols-outlined text-[16px]">military_tech</span>
            <span className="font-label-sm text-label-sm uppercase tracking-wider font-semibold">Venture Cohort</span>
          </div>
          <div className="font-title-md text-title-md text-on-surface font-semibold">Alpha Batch '25</div>
          <div className="font-body-sm text-body-sm text-on-surface-variant mt-0.5">Active Sprint Cycle</div>
        </div>
      </aside>

      {/* Top Header */}
      <div className="pl-64">
        <header className="fixed top-0 left-64 right-0 h-16 bg-surface-container-lowest/90 backdrop-blur-xl shadow-[0_1px_8px_rgba(0,0,0,0.04)] z-40 flex items-center justify-between px-space-lg gap-space-md">
          <div className="flex items-center gap-space-lg flex-1">
            <div className="hidden xl:flex flex-col">
              <span className="font-body-sm text-body-sm text-on-surface-variant font-medium">
                Where Ideas Become Ventures
              </span>
            </div>
            <div className="relative flex-1 max-w-md">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-[18px]">
                search
              </span>
              <input
                className="w-full h-10 pl-9 pr-4 bg-surface rounded-lg font-body-sm text-body-sm text-on-surface placeholder:text-on-surface-variant outline-none focus:bg-surface-container-lowest transition-all"
                placeholder="Search challenges, startups, invitations..."
                type="text"
              />
            </div>
          </div>

          <div className="flex items-center gap-space-md">
            <div className="hidden sm:flex items-center gap-space-xs px-2.5 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label-sm text-label-sm">
              <span className="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
              Cohort Status: Live
            </div>
            <div className="hidden md:flex items-center px-2.5 py-1 rounded-full bg-surface-container-high text-on-surface-variant font-label-sm text-label-sm uppercase tracking-wide">
              Demo data
            </div>

            <button className="relative p-2 rounded-lg text-on-surface-variant hover:bg-surface-container-low hover:text-on-surface transition-colors">
              <span className="material-symbols-outlined text-[20px]">notifications</span>
              <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-error"></span>
            </button>

            {/* Profile Dropdown */}
            <div className="relative">
              <button
                onClick={() => setProfileOpen(!profileOpen)}
                className="flex items-center gap-space-sm pl-space-xs p-1 rounded-lg hover:bg-surface-container-low transition-colors"
              >
                <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-on-primary">
                  <span className="material-symbols-outlined text-[18px]">person</span>
                </div>
                <div className="hidden lg:flex flex-col text-left">
                  <span className="font-title-md text-title-md text-on-surface leading-tight font-semibold">
                    {user?.name || 'Alex Mercer'}
                  </span>
                  <span className="font-label-sm text-label-sm text-secondary font-medium">Worker / Cohort Alpha</span>
                </div>
              </button>

              {profileOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-xl bg-surface-container-lowest shadow-xl border border-surface-container-high py-2 z-50">
                  <div className="px-4 py-2 border-b border-surface-container">
                    <p className="font-label-md text-label-md font-semibold text-on-surface">{user?.name}</p>
                    <p className="font-body-sm text-body-sm text-on-surface-variant truncate">{user?.email}</p>
                    <span className="inline-block mt-1 px-2 py-0.5 rounded bg-secondary-container text-on-secondary-container text-[11px] font-semibold">
                      Worker / Talent Mode
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
                      onClick={() => handleRoleChange('investor')}
                      className="w-full text-left px-4 py-2 text-body-sm hover:bg-surface-container flex items-center gap-2"
                    >
                      <span className="material-symbols-outlined text-[18px] text-secondary">trending_up</span>
                      <span>Investor Portal</span>
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
        <main className="relative pt-16 bg-surface min-h-screen">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
