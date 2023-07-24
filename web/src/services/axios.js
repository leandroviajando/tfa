import axios from 'axios';
import config from '@/config';
import axiosRetry from 'axios-retry';

const instance = axios.create({
  baseURL: parseInt(config.TESTING_MODE, 10) ? undefined : config.TFA_API_URL,
  withCredentials: true,
  maxRedirects: 0,
  headers: {
    'X-Requested-With': 'XMLHttpRequest',
  },
  validateStatus: (status) => {
    return status <= 400;
  },
});

instance.registerErrorHandler = (func) => {
  instance.errorHandler = func;
};

instance.interceptors.response.use(
  async function okResponse(response) {
    if (response.status > 400) {
      instance.errorHandler({ response, request: response.request });
    }
    return response;
  },
  async function errorHandler(error) {
    instance.errorHandler(error);
    return Promise.reject(error);
  }
);

axiosRetry(instance, {
  retries: 3,
  retryDelay: (retryCount) => {
    return retryCount ** 2 * 1000;
  },
});

export default instance;
