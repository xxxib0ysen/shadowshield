import axios from 'axios';

const API = axios.create({
    baseURL: 'http://127.0.0.1:5000/api', // 远程 Flask API
    timeout: 10000
});

export default API;
