import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { useAuth } from "contexts/AuthContext";
import { publicRoutes, authOnlyRoutes, unauthOnlyRoutes} from "helpers/RouteConfig";

const Routes = () => {
    const { isAuthenticated } = useAuth();

    const router = createBrowserRouter([
        ...publicRoutes,
        ...(isAuthenticated ? authOnlyRoutes : unauthOnlyRoutes),
    ]);

    return (
        <RouterProvider router={router} />
    );
}

export { Routes };