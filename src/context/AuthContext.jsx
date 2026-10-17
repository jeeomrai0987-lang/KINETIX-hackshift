import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const DEMO_USERS = {
  founder: {
    id: 'usr_founder_01',
    name: 'Alex Mercer',
    email: 'alex.mercer@synthetix.ai',
    role: 'founder',
    title: 'Founder / Cohort Alpha',
    entity: 'Synthetix AI',
    cohort: "Alpha Batch '25",
    nodeId: 'NODE-TX-9042A',
    verified: true,
    avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCrFd9FXpH1DVp90x6QYI3kcBlABNYtgFYxaa-elUwjSWxyV56HX1Uir3Bo-JqKk3TkfehwV64tbjsMvhw9FVCYgdY2H_bGj_WUycEQb8Dik8Hw6UG-DAyLKzDMeTucfRCt_DgSFD6L_pCOl0A8YFS_ujCydDFtmuuoeY7hOIu_gb7QgAuFUQWPIUNLCYl78krYPxXqb-rVILLe9UGsKUdf2HDshK8T-ZrUTNmAMRphT1t5VEKD26jNtQ',
  },
  investor: {
    id: 'usr_investor_02',
    name: 'Marcus Vance',
    email: 'marcus.vance@angelsyndicate.vc',
    role: 'investor',
    title: 'Investor / Angel Syndicate',
    entity: 'Syndicate Alpha',
    cohort: "Alpha Batch '25",
    nodeId: 'NODE-INV-8841Z',
    verified: true,
    tier: 'Syndicate Tier 1',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=256&q=80',
  },
  worker: {
    id: 'usr_worker_03',
    name: 'Elena Vance',
    email: 'elena.vance@startup.io',
    role: 'worker',
    title: 'Worker / Cohort Alpha',
    entity: 'Talent Pool #Alpha',
    cohort: "Alpha Batch '25",
    nodeId: 'TX-5512B',
    verified: true,
    skills: ['Distributed Systems', 'Rust', 'Go', 'System Architecture'],
    avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAXDAn8ZFbqaXgUtAZFPSAMimDjdAoYUtHj9L77g4tSh_dzBGXy6q7ARHBvvPaEiQBevjgoVWtUl1CPRgJcoZ_Gyr1x8Zo7gNTBlUQObPUZdavCilarTN6yVjeMbRs58962jPDHojUKOmZ_bPn3g6RPFzhAkTcS32gCbsLDrLoGoPt23xW2bo98EiFz6_G89_dt-TciA5PCjPGcobNbxFBrua1O80BXj8xC1JSaqoZGvJJLCVcC2Qyt0g',
  },
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('ventureforge_auth_user');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.error('Failed to parse saved user', e);
      }
    }
    return DEMO_USERS.founder;
  });

  const [toastMessage, setToastMessage] = useState(null);

  useEffect(() => {
    if (user) {
      localStorage.setItem('ventureforge_auth_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('ventureforge_auth_user');
    }
  }, [user]);

  const showToast = (message, duration = 3000) => {
    setToastMessage(message);
    setTimeout(() => {
      setToastMessage((prev) => (prev === message ? null : prev));
    }, duration);
  };

  const login = (email, password, role = 'founder') => {
    const base = DEMO_USERS[role] || DEMO_USERS.founder;
    const authenticatedUser = {
      ...base,
      email: email || base.email,
    };
    setUser(authenticatedUser);
    showToast(`Welcome back, ${authenticatedUser.name}! Signed in as ${role.toUpperCase()}`);
    return authenticatedUser;
  };

  const signup = (userData) => {
    const role = userData.role || 'founder';
    const base = DEMO_USERS[role] || DEMO_USERS.founder;
    const newUser = {
      ...base,
      id: `usr_${Date.now()}`,
      name: userData.name || base.name,
      email: userData.email || base.email,
      role: role,
      skills: userData.skills || base.skills || [],
      portfolioUrl: userData.portfolioUrl || '',
    };
    setUser(newUser);
    showToast(`Account created successfully! Welcome to VentureForge AI.`);
    return newUser;
  };

  const logout = () => {
    setUser(null);
    showToast('Logged out of VentureForge session.');
  };

  const switchRole = (newRole) => {
    if (DEMO_USERS[newRole]) {
      setUser(DEMO_USERS[newRole]);
      showToast(`Switched active portal to ${newRole.toUpperCase()} mode.`);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        login,
        signup,
        logout,
        switchRole,
        showToast,
        toastMessage,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
