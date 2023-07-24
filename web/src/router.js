import VueRouter from 'vue-router';
import Vue from 'vue';
import routes from './data/routes';

Vue.use(VueRouter);

const instance = new VueRouter({
  mode: 'history',
  routes,
});

instance.registerStore = (store) => {
  instance.store = store;
};

instance.beforeEach((to, from, next) => {
  next();
});

export default instance;
