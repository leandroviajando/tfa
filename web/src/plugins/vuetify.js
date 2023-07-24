import config from '@/config';
import Vue from 'vue';
import Vuetify from 'vuetify';

const themes = {
  local: {
    primary: '#FF9800',
  },
  staging: {
    primary: '#FF9801',
  },
  preproduction: {
    primary: '#9C27B0',
  },
  production: {
    primary: '#46E696',
  },
};

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: { light: themes[config.TFA_ENV] },
    options: {
      customProperties: true,
    },
  },
  icons: {
    iconfont: 'mdiSvg',
  },
});
