import axios, { AxiosRequestConfig } from 'axios';
import { config } from "@/common/config";

// https://www.npmjs.com/package/nock#axios
// axios.defaults.adapter = require('axios/lib/adapters/http');

export class HTTPClientService{
    public static async fetchData<T>(path: string, axiosConfig?: AxiosRequestConfig){
        const client = axios.create({ baseURL: config.API_BASE_URL });
        const resp = await client.get<T>(path, axiosConfig);
        return resp.data as T;
    }
}
