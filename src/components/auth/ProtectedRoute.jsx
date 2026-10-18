import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const ProtectedRoute = ({ allowedRole, children }) => {
  const { user, isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center gap-4">
        <div className="w-10 h-10 border-4 border-secondary/20 border-t-secondary rounded-full animate-spin" />
        <span className="font-label-md text-label-md text-on-surface-variant font-medium">
          Verifying cryptographic credentials...
        </span>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return <Navigate to="/auth" replace />;
  }

  if (allowedRole && user.role !== allowedRole) {
    const portalPath =
      user.role === 'founder'
        ? '/founder/dashboard'
        : user.role === 'investor'
        ? '/investor/dashboard'
        : user.role === 'worker'
        ? '/worker/dashboard'
        : '/auth';

    return <Navigate to={portalPath} replace />;
  }

  return children ? children : <Outlet />;
};

export default ProtectedRoute;
