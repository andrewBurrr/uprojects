import React, {useContext, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';
import {ApiContext} from "contexts/api";

import Home from "./views/home-page/Home"
import About from "./views/about-page/About"
import Register from "./views/register-page/Register"
import { Route,Routes } from 'react-router-dom';

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
  <div>
<Routes>
  <Route path="/" element={<Home/>}/>
  <Route path="/about" element={<About/>}/>
  <Route path="/register" element={<Register/>}/>
  </Routes>
</div>
  );
}

export { App };
