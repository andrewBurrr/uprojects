import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { useAuth } from "contexts/AuthContext";
import { ProtectedRoute } from "helpers/ProtectedRoute";
import { Login } from "views/login-page/Login";
import { Register } from "views/register-page/Register";
import { Home } from "views/home-page/Home";
import { Dashboard } from "views/dashboard-page/Dashboard";
import {About} from "views/about-page/About";
import {AppLayout} from "../layouts/AppLayout";
import {PasswordReset} from "../views/password-reset-page/PasswordReset";

const Routes = () => {
    const { isAuthenticated } = useAuth();

    const publicRoutes = [
        {
            path: "/about",
            element:
                <AppLayout>
                    <About />
                </AppLayout>,
        },
    ];

    const authOnlyRoutes = [
        {
            path: "/",
            element: <ProtectedRoute />,
            children: [
                {
                    path: "/",
                    element:
                        <AppLayout>
                            <Dashboard />
                        </AppLayout>
                }
            ]
        }
    ];
    const unauthOnlyRoutes = [
        {
            path: "/",
            element:
                <AppLayout>
                    <Home />
                </AppLayout>,
        },
        {
            path: "/login",
            element:
                <AppLayout>
                    <Login />
                </AppLayout>,
        },
        {
            path: "/register",
            element:
                <AppLayout>
                    <Register />
                </AppLayout>,
        },
        {
            path: "/reset-password",
            element:
                <AppLayout>
                    <PasswordReset />
                </AppLayout>
        }
    ];

    const router = createBrowserRouter([
        ...publicRoutes,
        ...(isAuthenticated ? [] : unauthOnlyRoutes),
        ...authOnlyRoutes,
    ]);

    return (
        <RouterProvider router={router} />
    );
}

export { Routes };