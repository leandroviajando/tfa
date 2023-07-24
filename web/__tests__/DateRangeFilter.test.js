import { createLocalVue, mount } from '@vue/test-utils';
import Vuetify from 'vuetify';
import Vue from 'vue';
import store from '@/store';
import i18n from '@/plugins/i18n';
import DateRangeFilter from '@/components/DateRangeFilter';
import moment from 'moment';
import router from '@/router';
import VueRouter from 'vue-router';
import { flushPromises } from '../utils';

describe('date range filter component test', () => {
  const localVue = createLocalVue();
  Vue.use(Vuetify);
  Vue.use(VueRouter);
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
  });
  const initialDateRange = ['2021-03-04', '2021-03-08'];

  const getWrapper = (afterDatePicked) => {
    return mount(DateRangeFilter, {
      propsData: {
        initialDateRange,
        afterDatePicked,
        maxDate: moment('2021-03-20').format('YYYY-MM-DD'),
      },
      localVue,
      vuetify,
      store,
      router,
      i18n,
    });
  };

  it('renders date picker menu with the correct initial values', async () => {
    const afterDatePicked = jest.fn(() => {});
    const wrapper = await getWrapper(afterDatePicked);
    await flushPromises();
    expect(wrapper.vm.$data.dateRange).toStrictEqual(initialDateRange);
    expect(wrapper.vm.$router.history.current.query).toStrictEqual({
      from_date: '2021-03-04',
      to_date: '2021-03-08',
    });

    const textField = wrapper.find('#dateRangeTextField');
    expect(textField.element.value).toBe('2021-03-04 - 2021-03-08');
    expect(afterDatePicked).toHaveBeenCalledTimes(1);
  });

  it('redirects and calls action on select', async () => {
    const afterDatePicked = jest.fn(() => {});
    const wrapper = await getWrapper(afterDatePicked);
    await flushPromises();
    const textField = wrapper.find('#dateRangeTextField');

    // Trigger a click on the text field to open the date picker
    await textField.trigger('click');
    const datePickerAfter = wrapper.find('#dateRangePicker');
    expect(datePickerAfter.exists()).toBe(true);
    const dates = datePickerAfter.findAll('.v-btn__content').wrappers;

    // Select two dates from the picker and check values get updated
    await dates[4].trigger('click'); // Click on 2021-03-03
    await dates[7].trigger('click'); // Click on 2021-03-06
    await flushPromises();
    const textFieldAfterSelect = wrapper.find('#dateRangeTextField');
    expect(textFieldAfterSelect.element.value).toBe('2021-03-03 - 2021-03-06');
    expect(wrapper.vm.$router.history.current.query).toStrictEqual({
      from_date: '2021-03-03',
      to_date: '2021-03-06',
    });
    expect(afterDatePicked).toHaveBeenCalledTimes(2);
  });

  it('sets to_date 7 days ahead if nothing chosen', async () => {
    const afterDatePicked = jest.fn(() => {});
    const wrapper = await getWrapper(afterDatePicked);
    await flushPromises();
    const textField = wrapper.find('#dateRangeTextField');

    // Trigger a click on the text field to open the date picker
    await textField.trigger('click');
    const datePickerAfter = wrapper.find('#dateRangePicker');
    expect(datePickerAfter.exists()).toBe(true);
    const dates = datePickerAfter.findAll('.v-btn__content').wrappers;

    // Select one date from the picker, and close the date picker
    await dates[4].trigger('click'); // Click on 2021-03-03
    await textField.trigger('click');
    await flushPromises();

    // Expect the to_date to be set 7 days ahead as default
    const textFieldAfterSelect = wrapper.find('#dateRangeTextField');
    expect(textFieldAfterSelect.element.value).toBe('2021-03-03 - 2021-03-10');
    expect(wrapper.vm.$router.history.current.query).toStrictEqual({
      from_date: '2021-03-03',
      to_date: '2021-03-10',
    });
    expect(afterDatePicked).toHaveBeenCalledTimes(2);
  });
});
