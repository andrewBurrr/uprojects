import {ReactNode} from "react";
import { Dashboard as DashboardIcon, ImportContacts as AboutIcon, Home as HomeIcon } from "@mui/icons-material";
import {AppLayout} from "layouts/AppLayout";
import {About} from "views/about-page/About";
import {Home} from "views/home-page/Home";
import {Login} from "views/login-page/Login"
import {PasswordReset} from "views/password-reset-page/PasswordReset";
import {Register} from "views/register-page/Register";
import {ProtectedRoute} from "helpers/ProtectedRoute";
import {Dashboard} from "views/dashboard-page/Dashboard";

import { OrgPage } from "views/org-page/OrgPage";
import { Teampage } from "views/team-page/Teampage";
import { Eventpage } from "views/event-page/Eventpage";

type CustomRoute = {
    title: string;
    path: string;
    element: ReactNode;
    icon?: ReactNode;
    children?: CustomRoute[];
}

const publicRoutes: CustomRoute[] = [
    {
        title: "About",
        path: "/about",
        element:
            <AppLayout>
                <About />
            </AppLayout>,
        icon: <AboutIcon />
    },
];

const authOnlyRoutes: CustomRoute[] = [
    {
        title: "Dashboard",
        path: "/user/:user_id",
        element: <ProtectedRoute />,
        icon: <DashboardIcon />,
        children: [
            {
                title: "Dashboard",
                path: "/user/:user_id",
                element:
                    <AppLayout>
                        <Dashboard />
                    </AppLayout>,
                icon: <DashboardIcon />
            },
        ]
    },
];

const unauthOnlyRoutes: CustomRoute[] = [
    {
        title: "Home",
        path: "/",
        element:
            <AppLayout>
                <Home />
            </AppLayout>,
        icon: <HomeIcon />
    },
    {
        title: "Login",
        path: "/login",
        element:
            <AppLayout>
                <Login />
            </AppLayout>,
    },
    {
        title: "Register",
        path: "/register",
        element:
            <AppLayout>
                <Register />
            </AppLayout>,
    },
    {
        title: "Reset Password",
        path: "/reset-password",
        element:
            <AppLayout>
                <PasswordReset />
            </AppLayout>,
    },
];

export { publicRoutes, authOnlyRoutes, unauthOnlyRoutes };