import axios, { AxiosInstance } from 'axios';
import Cookies from "js-cookie";

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

        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
            accept: 'application/json',
        };

        if (localStorage.getItem('access_token')) {
            headers.Authorization = `JWT ${localStorage.getItem('access_token')}`;
        }

        this.axiosInstance = axios.create({
            baseURL: baseURL,
            timeout: 5000,
            headers: headers
        })

        this.axiosInstance.interceptors.response.use(
            response => response,
            error => {
                console.log(error);
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
        const csrf = Cookies.get('csrftoken');
        const response = await this.axiosInstance.post('/token/', {
            email: email,
            password: password,
            csrfmiddlewaretoken: csrf}, {withCredentials: true});
        const {access, refresh} = response.data;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    }

    /**
     * Use the refresh token to retrieve a new access token
     *
     * @param {string} refreshToken - refr
     */
    refreshAccessToken = async (refreshToken: string): Promise<void> => {
        const response = await this.axiosInstance.post('/token/refresh/', {refresh: refreshToken});
        const { access } = response.data;
        localStorage.setItem('access_token', access);
    }

    getData = async <T>(endpoint: string): Promise<T> => {
        const response = await this.axiosInstance.get(endpoint);
        return response.data as T;
    }

    postData = async <T>(data: any, endpoint: string): Promise<T> => {
        const response = await this.axiosInstance.post(endpoint, data);
        return response.data as T;
    }

    getAccessToken() {
        return localStorage.getItem('access_token');
    }

    setAccessToken(token :string) {
        localStorage.setItem('access_token', token);
    }

    removeAccessToken() {
        localStorage.removeItem('access_token');
    }
}

export { API };
