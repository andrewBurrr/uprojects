import React, {createContext, ReactNode, useContext} from 'react';
import { API } from "apis/axios";

const ApiContext = createContext({
    api: new API("http://api.uprojects.ca"),
});

interface ApiProviderProps {
    children: ReactNode;
}

export const useApi = () => {
    return useContext(ApiContext);
}

const ApiProvider: React.FC<ApiProviderProps> = ({ children }: ApiProviderProps) => {
    const api = new API('http://api.uprojects.ca');

    return (
        <ApiContext.Provider value={{ api }}>
            {children}
        </ApiContext.Provider>
    );
}

export { ApiProvider, ApiContext };
