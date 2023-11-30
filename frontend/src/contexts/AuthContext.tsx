import React, {useState, useEffect, useContext, ReactNode} from "react";
import jwtDecode from "jwt-decode";
import { useApi } from "contexts/ApiContext";

type User = {
    user_id: string;
    first_name: string;
    last_name: string;
    profile_image: string;
} | null;

interface AuthProviderProps {
    children: ReactNode;
}

interface AuthContextProps {
    user: User;
    isAuthenticated: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    register: (email: string, first_name: string, last_name: string, password: string) => Promise<void>;
}

const AuthContext = React.createContext<AuthContextProps>({
    user: null,
    isAuthenticated: false,
    login: async (email: string, password: string) => {},
    logout: async () => {},
    register: async (email: string, first_name: string, last_name: string, password: string) => {}
});

const useAuth = () => {
    return useContext(AuthContext);
}


const AuthProvider: React.FC<AuthProviderProps> = ({ children }: AuthProviderProps) => {
    const [user, setUser] = useState<User>(null);
    const [isAuthenticated, setIsAuthenticated] = useState(localStorage.getItem("access_token") !== null);
    const { api } = useApi();

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

    useEffect(() => {
        const decodeToken = () => {
            if (isAuthenticated) {
                const token = localStorage.getItem('access_token');
                if (token) {
                    let user_id: string, first_name: string, last_name: string, profile_image: string;
                    ({user_id, first_name, last_name, profile_image} = jwtDecode(token));
                    setUser({
                        user_id: user_id,
                        first_name: first_name,
                        last_name: last_name,
                        profile_image: `${process.env.REACT_APP_BASE_URL}${profile_image}`,
                    });
                }
            } else {
                setUser(null);
            }
        };
        decodeToken();
    }, [isAuthenticated]);

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

    return(
        <AuthContext.Provider value={{ user, isAuthenticated, login, logout, register }}>
            { children }
        </AuthContext.Provider>
    )
}

export { AuthProvider, useAuth };