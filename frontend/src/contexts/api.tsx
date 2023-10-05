import React, {createContext, ReactNode} from 'react';
import { API } from "apis/axios";

const ApiContext = createContext<API | undefined>(undefined);

interface ApiProviderProps {
    children: ReactNode;
}

const ApiProvider: React.FC<ApiProviderProps> = ({ children }: ApiProviderProps) => {
    const api = new API('http://localhost:8000');

    return (
        <ApiContext.Provider value={api}>
            {children}
        </ApiContext.Provider>
    );
}

export { ApiProvider, ApiContext };