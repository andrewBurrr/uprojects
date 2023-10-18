import React from 'react';

import { Routes } from "helpers/Routes";
import { AuthProvider } from "contexts/AuthContext";
import { ApiProvider } from "contexts/ApiContext";

/**
 * AuthProvider gives all child components access to authentication context objects through the use of useAuth()
 * ApiProvider gives all child components access to api context objects (to make api calls) through the use of useApi()
 * Routes is a helper component that manages protected routes and permissions for other available routes
 */
const App = () => {
    return (
        <AuthProvider>
            <ApiProvider>
                <Routes />
            </ApiProvider>
        </AuthProvider>
    );
}

export { App };
