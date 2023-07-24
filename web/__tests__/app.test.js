import { shallowMount, createLocalVue } from '@vue/test-utils';
import VueRouter from 'vue-router';
import Vue from 'vue';
import Vuetify from 'vuetify';
import router from '../src/router';
import App from '../src/App.vue';

Vue.use(Vuetify);
Vue.use(VueRouter);

const localVue = createLocalVue();

describe('app', () => {
  let vuetify;
  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('renders the correct markup', () => {
    const wrapper = shallowMount(App, {
      localVue,
      vuetify,
      router,
      stubs: ['router-view', 'router-link'],
    });

    expect(wrapper.html()).toContain(
      '<router-view-stub name="default"></router-view-stub>'
    );
  });
});
