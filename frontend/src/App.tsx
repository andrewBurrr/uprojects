import React, {useContext, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import {ApiContext} from "contexts/api";

const App = () => {

  const api = useContext(ApiContext);

  useEffect(() => {
    const username = 'andrew.burton@ucalgary.ca';
    const password = 'admin1234';

    api?.login(username, password)
        .then(() => {
          console.log('Login Successful');
          const accessToken = api?.getAccessToken();
          console.log('Access Token:', accessToken);
        })
        .catch(error => {
          console.error('Login failed:', error)
        });
  }, [api]);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export { App };
