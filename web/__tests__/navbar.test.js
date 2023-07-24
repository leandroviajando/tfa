import { shallowMount, createLocalVue } from '@vue/test-utils';
import Vuetify from 'vuetify';
import Vue from 'vue';
import VueRouter from 'vue-router';
import Navbar from '../src/components/Navbar.vue';
import Menu from '../src/components/Menu.vue';

describe('navbar component', () => {
  const localVue = createLocalVue();

  Vue.use(Vuetify);
  Vue.use(VueRouter);
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('displays navigation', () => {
    const wrapper = shallowMount(Navbar, {
      localVue,
      vuetify,
    });
    expect(wrapper.getComponent(Menu)).toBeDefined();
  });
});
