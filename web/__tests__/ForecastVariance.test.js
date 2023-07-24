import { createLocalVue, mount } from '@vue/test-utils';
import Vuetify from 'vuetify';
import Vue from 'vue';
import i18n from '@/plugins/i18n';
import services_axios from '@/services/axios';
import ForecastVariance from '@/pages/ForecastVariance.vue';
import router from '@/router';
import Vuex from 'vuex';
import { flushPromises } from '../utils';

describe('sending partners forecast variance page test', () => {
  const localVue = createLocalVue();
  Vue.use(Vuetify);
  localVue.use(Vuex);
  let vuetify;
  let actions;
  let getters;

  beforeEach(() => {
    vuetify = new Vuetify();
  });

  afterEach(() => {
    actions.fetchBalances.mockClear();
  });

  const instantiateStore = () => {
    actions = {
      fetchBalances: jest.fn(() =>
        Promise.resolve({
          balances: [],
      })),
    };
    getters = {
      balances: () => [],
    };
    return new Vuex.Store({
      actions,
      getters,
    });
  };

  const getWrapper = () => {
    // Set original route - usually this would be done by stubbed DateRangeFilter
    router.push({
      path: '/',
      query: {
        from_date: '2021-06-08',
        to_date: '2021-06-10',
      },
    });
    const store = instantiateStore();
    return mount(ForecastVariance, {
      localVue,
      vuetify,
      router,
      store,
      i18n,
      stubs: {
        DateRangeFilter: {
          template: '<div id="stubbed_date_filter"/>',
        },
        BalanceFilter: {
          template: '<div id="stubbed_partner_filter"/>',
        },
        ForecastVarianceTable: {
          template: '<div id="stubbed_table"/>',
        },
      },
    });
  };

  const rawVarianceData = {
    balance_id: 213,
    from_date: '2023-07-17',
    to_date: '2023-07-24',
    data: [
      {
        dt: '2022-01-01',
        actual_amount: 10,
        forecasted_amount: 11,
        variance: 1,
        mape: 10.0,
      },
      {
        dt: '2022-01-02',
        actual_amount: 15,
        forecasted_amount: 16,
        variance: 1,
        mape: 8.0,
      }
    ],
  };

  it('makes calls expected upon render', async () => {
    const mockAxiosGet = jest.fn(() =>
      Promise.resolve({ data: rawVarianceData })
    );
    services_axios.get = mockAxiosGet;

    const wrapper = getWrapper();
    await flushPromises();

    const testaggregateType = 'daily';
    const testBalanceId = 1;

    await wrapper.vm.setAggregateType(testaggregateType);
    await wrapper.vm.setSelectedBalanceId(testBalanceId);

    expect(wrapper.vm.$router.history.current.query).toStrictEqual({
      from_date: '2021-06-08',
      to_date: '2021-06-10',
      aggregateType: testaggregateType,
      balanceId: testBalanceId.toString(),
    });

    expect(mockAxiosGet).toHaveBeenCalledWith(
      `/api/v1/forecast_variance/${testBalanceId}`,
      {
        signal: wrapper.vm.controller.signal,
        params: {
          from_date: '2021-06-08',
          to_date: '2021-06-10',
        },
      }
    );
  });
});
