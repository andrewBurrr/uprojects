import React, {useState, useEffect, useContext, ReactNode} from "react";
import jwtDecode from "jwt-decode";
import { useApi } from "contexts/ApiContext";

interface User {
    first_name: string;
    last_name: string;
    profile_image: string;
}

interface AuthProviderProps {
    children: ReactNode;
}

const initialUser: User = {
    first_name: '',
    last_name: '',
    profile_image: '',
};

const AuthContext = React.createContext({
    user: initialUser,
    isAuthenticated: false,
    login: (email: string, password: string) => {},
    logout: () => {},
    register: (email: string, first_name: string, last_name: string, password: string) => {}
});

const useAuth = () => {
    return useContext(AuthContext);
}


const AuthProvider: React.FC<AuthProviderProps> = ({ children }: AuthProviderProps) => {
    const [user, setUser] = useState(initialUser);
    const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem("access_token") !== null);
    const { api } = useApi();

    useEffect(() => {
        if (isAuthenticated) {
            const token = localStorage.getItem('access_token');
            if (token) {
                const decodedToken: User = jwtDecode(token);
                setUser({
                    first_name: decodedToken.first_name,
                    last_name: decodedToken.last_name,
                    profile_image: `${process.env.REACT_APP_BASE_URL}${decodedToken.profile_image}`,
                });
            }
        } else {
            setUser(initialUser);
        }
    }, [isAuthenticated, user.profile_image]);

    const login = async (email: string, password: string) => {
        try {
            await api.login(email, password);
            setIsAuthenticated(true);
        } catch (error) {
            throw error;
        }
    }

    const logout = async () => {
        await api.logout();
        setIsAuthenticated(false);
    }

    const register = async (email: string, first_name: string, last_name: string, password: string) => {
        try {
            await api.register(email, first_name, last_name, password);
        } catch (error) {
            throw error;
        }
    }

    useEffect(() => {
        const checkIsAuthenticated = () => {
            const status = localStorage.getItem('access_token');
            if (status) {
                setIsAuthenticated(true);
            } else {
                setIsAuthenticated(false);
            }
        }
        window.addEventListener('storage', checkIsAuthenticated);

        return () => {
            window.removeEventListener('storage', checkIsAuthenticated);
        }
    }, []);

    return(
        <AuthContext.Provider value={{ user, isAuthenticated, login, logout, register }}>
            { children }
        </AuthContext.Provider>
    )
}

export { AuthProvider, useAuth };