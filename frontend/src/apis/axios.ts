import axios, {AxiosInstance} from 'axios';
import Cookies from "js-cookie";
import jwtDecode from "jwt-decode";

/**
 * API class for making HTTP requests
 */
class API {
    private axiosInstance: AxiosInstance;

    /**
     *
     * @param baseURL
     */
    constructor(baseURL: string) {
        const csrf = Cookies.get('csrftoken');
        let headers = {
            'Content-Type': 'application/json',
            accept: 'application/json',
            'Authorization': '',
            'X-CSRFToken': csrf,
        };

        if (localStorage.getItem('access_token')) {
            headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`;
        }

        this.axiosInstance = axios.create({
            baseURL: baseURL,
            timeout: 5000,
            headers: headers
        })

        this.axiosInstance.interceptors.response.use(
            response => response,
            error => {
                if (error.response.status === 401) {
                    const refreshToken = localStorage.getItem('refresh_token');
                    if (!refreshToken) {
                        return Promise.reject(error);
                    }
                    return this.refreshAccessToken(refreshToken)
                        .then(() => {
                            const config = error.config;
                            config.headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
                            return this.axiosInstance.request(config);
                        })
                        .catch(refreshError => {
                            console.error('Failed to refresh access token: ', refreshError);
                            localStorage.removeItem('access_token');
                            localStorage.removeItem('refresh_token');

                            return Promise.reject(refreshError);
                        });
                }
                return Promise.reject(error);
            }
        );
    }

    /**
     * Submit a login request to the backend apis
     *
     * @param {string} email - The email of the user
     * @param  {string} password - The password of the user
     * @returns {Promise<void>} - A Promise that resolves when the login is successful.
     */
    login = async (email: string, password: string): Promise<void> => {
        try {
            const response = await this.axiosInstance.post('/users/login/', {
                email: email,
                password: password,
            }, { withCredentials: true });
            const { access, refresh } = response.data;
            localStorage.setItem('access_token', access);
            localStorage.setItem('refresh_token', refresh);
            return jwtDecode(response.data.access);
        } catch (error) {
            throw error;
        }
    }

    logout = async (): Promise<void> => {
        await this.axiosInstance.post('/users/logout/', {
            refresh_token: localStorage.getItem('refresh_token'),
        });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        this.axiosInstance.defaults.headers['Authorization'] = null;
    }

    register = async (email: string, first_name: string, last_name: string, password: string): Promise<void> => {
        try {
            await this.axiosInstance.post("/users/register/", {
                first_name: first_name,
                last_name: last_name,
                email: email,
                password: password,
            }, { withCredentials: true });
        } catch (error) {
            throw error;
        }
    }

    /**
     * Use the refresh token to retrieve a new access token
     *
     * @param {string} refreshToken - refr
     */
    refreshAccessToken = async (refreshToken: string): Promise<void> => {
        const response = await this.axiosInstance.post('/users/refresh/', {refresh: refreshToken});
        const { access } = response.data;
        localStorage.setItem('access_token', access);
    }

    getData = async <T>(endpoint: string): Promise<T> => {
        const response = await this.axiosInstance.get(endpoint);
        return response.data as T;
    }
    
    postData = async <T>(endpoint: string, data: any): Promise<T> => {
        const response = await this.axiosInstance.post(endpoint, data);
        return response.data as T;
    }
}

export { API };
