import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import { authApi, TOKEN_STORAGE_KEY } from '../api';

const AuthContext = createContext(null);

// Preserved for backwards compatibility with un-rewired views; will be removed in C3
export const DEMO_USERS = {
  founder: {
    id: 'usr_founder_01',
    name: 'Alex Mercer',
    email: 'alex.mercer@synthetix.ai',
    role: 'founder',
    title: 'Founder / Cohort Alpha',
    entity: 'Synthetix AI',
    cohort: "Alpha Batch '25",
    nodeId: 'NODE-FND-0001',
    verified: true,
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
  },
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('ventureforge_auth_user');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.error('Failed to parse cached user', e);
      }
    }
    return null; // No silent founder default user
  });

  const [isLoading, setIsLoading] = useState(true);
  const [toastMessage, setToastMessage] = useState(null);
  const toastTimeoutRef = useRef(null);

  // Sync user changes to localStorage
  useEffect(() => {
    if (user) {
      localStorage.setItem('ventureforge_auth_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('ventureforge_auth_user');
    }
  }, [user]);

  // Initial session hydration from backend
  useEffect(() => {
    const hydrateSession = async () => {
      const token = localStorage.getItem(TOKEN_STORAGE_KEY);
      if (!token) {
        setUser(null);
        setIsLoading(false);
        return;
      }

      try {
        const verifiedUser = await authApi.getMe();
        setUser(verifiedUser);
      } catch (err) {
        console.warn('Session verification failed, clearing stale auth', err);
        localStorage.removeItem(TOKEN_STORAGE_KEY);
        localStorage.removeItem('ventureforge_auth_user');
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    hydrateSession();
  }, []);

  const showToast = (message, duration = 3000) => {
    if (toastTimeoutRef.current) {
      clearTimeout(toastTimeoutRef.current);
    }
    setToastMessage(message);
    toastTimeoutRef.current = setTimeout(() => {
      setToastMessage(null);
      toastTimeoutRef.current = null;
    }, duration);
  };

  const login = async (email, password, role = 'founder') => {
    // If password indicates quick demo bypass, route through demoLogin
    if (password === 'demo-token-bypass') {
      return demoLogin(role);
    }

    try {
      const res = await authApi.login({ email, password });
      if (res?.token) {
        localStorage.setItem(TOKEN_STORAGE_KEY, res.token);
      }
      const authenticatedUser = res?.user || null;
      setUser(authenticatedUser);
      showToast(`Welcome back, ${authenticatedUser?.name || 'User'}!`);
      return authenticatedUser;
    } catch (err) {
      const msg = err.message || 'Login failed';
      showToast(msg);
      throw err;
    }
  };

  const signup = async (userData) => {
    try {
      const payload = {
        name: userData.name,
        email: userData.email,
        password: userData.password || 'Demo#2026',
        role: userData.role || 'founder',
        skills: userData.skills,
        portfolioUrl: userData.portfolioUrl,
        githubUrl: userData.githubUrl,
        experienceLevel: userData.experienceLevel || userData.experience,
        whatsappEnabled: userData.whatsappEnabled,
      };

      const res = await authApi.register(payload);
      if (res?.token) {
        localStorage.setItem(TOKEN_STORAGE_KEY, res.token);
      }
      const registeredUser = res?.user || null;
      setUser(registeredUser);
      showToast('Account created successfully! Welcome to VentureForge AI.');
      return registeredUser;
    } catch (err) {
      const msg = err.message || 'Signup failed';
      showToast(msg);
      throw err;
    }
  };

  const demoLogin = async (role = 'founder') => {
    try {
      const res = await authApi.demoLogin(role);
      if (res?.token) {
        localStorage.setItem(TOKEN_STORAGE_KEY, res.token);
      }
      const demoUser = res?.user || null;
      setUser(demoUser);
      showToast(`Signed in as Demo ${role.toUpperCase()}: ${demoUser?.name || ''}`);
      return demoUser;
    } catch (err) {
      const msg = err.message || 'Demo login failed';
      showToast(msg);
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem('ventureforge_auth_user');
    setUser(null);
    showToast('Logged out of VentureForge session.');
  };

  const switchRole = async (newRole) => {
    try {
      await demoLogin(newRole);
    } catch {
      showToast(`Unable to switch role to ${newRole}`);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        signup,
        demoLogin,
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

export default AuthContext;
