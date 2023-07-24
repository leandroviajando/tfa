const window_api_urls = window.env ? window.env.api_urls : undefined;
const window_env = window.env ? window.env.env : 'local';
const window_version = window.env ? window.env.version : 'dev';

function selectUrl(hostname, apiUrlsString) {
  if (apiUrlsString === undefined) {
    return undefined;
  }
  const apiUrls = apiUrlsString.split(',').map((x) => x.trim());
  const apiUrl = apiUrls
    .filter((x) => x.replace(/\/+$/, '').endsWith(hostname))
    .pop(0);
  return apiUrl;
}

const api_urls_string = process.env.VUE_APP_TFA_API_URLS
  ? process.env.VUE_APP_TFA_API_URLS
  : window_api_urls;

const hostname = window.location.hostname.split('.').slice(1).join('.');
const api_url = selectUrl(hostname, api_urls_string);

export default {
  NODE_ENV: process.env.NODE_ENV,
  TFA_API_URL: api_url,
  TFA_ENV: process.env.VUE_APP_ENV ? process.env.VUE_APP_ENV : window_env,
  TFA_VERSION: window_version,
  TESTING_MODE: process.env.VUE_APP_TESTING_MODE,
  selectUrl,
};
