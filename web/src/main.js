import '@babel/polyfill';
import '@fontsource/dejavu-math';
import 'core-js';
import Vue from 'vue';
import App from './App.vue';
import store from './store';
import router from './router';
import vuetify from './plugins/vuetify';
import i18n from './plugins/i18n';
import axios from './services/axios';
import '@/assets/global.scss';

Vue.use(router);

axios.registerErrorHandler((error) => {
  store.dispatch('handleAPIError', error);
});

router.registerStore(store);

const app = {
  el: '#app',
  render: (h) => h(App),
  store,
  router,
  vuetify,
  i18n,
  beforeCreate() {
    this.$store.commit('initialiseStore');
  },
};

export default new Vue(app);
