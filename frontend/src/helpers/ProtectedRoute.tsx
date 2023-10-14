import React from "react";
import {useAuth} from "contexts/AuthContext";
import {Navigate, Outlet} from "react-router-dom";

const ProtectedRoute = () => {
    const { isAuthenticated } = useAuth();

    if (isAuthenticated) return <Outlet />;
    return <Navigate to="/login" />;
}

export { ProtectedRoute };