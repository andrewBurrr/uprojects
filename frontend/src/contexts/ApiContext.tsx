import React, {createContext, ReactNode, useContext} from 'react';
import { API } from "apis/axios";

const ApiContext = createContext({
    api: new API("http://localhost:8000"),
    getData: (endpoint: string) => {},
    postData: (endpoint: string, data: any) => {}
});

interface ApiProviderProps {
    children: ReactNode;
}

export const useApi = () => {
    return useContext(ApiContext);
}

const ApiProvider: React.FC<ApiProviderProps> = ({ children }: ApiProviderProps) => {
    const api = new API('http://localhost:8000');

    const getData = (endpoint: string) => {
        return api.getData(endpoint);
    }

    const postData = (endpoint: string, data: any) => {
        return api.postData(endpoint, data);
    }

    return (
        <ApiContext.Provider value={{ api, getData, postData }}>
            {children}
        </ApiContext.Provider>
    );
}

export { ApiProvider, ApiContext };