import { createLocalVue, mount } from '@vue/test-utils';
import Vuetify from 'vuetify';
import Vue from 'vue';
import Vuex from 'vuex';
import i18n from '@/plugins/i18n';
import BalanceFilter from '@/components/BalanceFilter';
import services_axios from '@/services/axios';
import { flushPromises } from '../utils';

describe('receiving partner filter component test', () => {
  const localVue = createLocalVue();
  Vue.use(Vuetify);
  localVue.use(Vuex);
  let vuetify;
  let getters;
  let state;
  let actions;

  const testBalances = [
    { value: null, text: 'All' },
    { value: 12, text: 'Default USD - Dahabshiil' },
    { value: 13, text: 'Commission - USD - Dahabshiil' },
    { value: 14, text: 'Fees Western Union - MTN Uganda' },
  ];

  const instantiateState = () => {
    // Set initial state
    state = {
      balances: testBalances,
    };
    getters = {
      balances: () => state.balances,
    };
    actions = {
      fetchBalances: jest.fn(),
    };
    return new Vuex.Store({
      state,
      getters,
      actions,
    });
  };

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  const emitMock = jest.fn();

  const getWrapper = (selectedBalanceId = null) => {
    const store = instantiateState();
    const wrapper = mount(BalanceFilter, {
      propsData: {
        selectedBalanceId,
      },
      localVue,
      vuetify,
      store,
      i18n,
    });

    wrapper.vm.$emit = emitMock;

    return wrapper;
  };

  it('renders as expected, using balances from state', async () => {
    services_axios.get = jest.fn(() => Promise.resolve({ data: testBalances }));
    const wrapper = await getWrapper();
    await flushPromises();
    expect(wrapper.html()).toMatchSnapshot();
  });

  it('sets selected balance if provided', async () => {
    services_axios.get = jest.fn(() => Promise.resolve({ data: testBalances }));
    const wrapper = await getWrapper(12);
    await flushPromises();
    const filter = wrapper.find('#balance-filter');
    expect(filter.element.value).toBe('Default USD - Dahabshiil');
  });
});
