<template>
  <v-menu
    ref="date_picker"
    v-model="datePickerOpen"
    :close-on-content-click="false"
    offset-y
    max-width="290px"
    min-width="auto"
  >
    <template #activator="{ on, attrs }">
      <v-text-field
        id="dateRangeTextField"
        v-model="dateRangeText"
        :label="$t('dateRange')"
        prepend-icon="mdi-calendar"
        v-bind="attrs"
        dense
        readonly
        v-on="on"
      ></v-text-field>
    </template>
    <v-date-picker
      id="dateRangePicker"
      v-model="dateRange"
      range
      :max="maxDate"
      @change="dateUpdateEventReceiver"
    ></v-date-picker>
  </v-menu>
</template>

<script>
import moment from 'moment';
import dayjs from 'dayjs';
import _ from 'lodash';

export default {
  props: {
    initialDateRange: {
      type: Array,
      default: () => [],
    },
    afterDatePicked: {
      type: Function,
      default: () => {},
    },
    maxDate: {
      type: String,
      default: '',
    },
    daysLimit: {
      type: Number,
      default: null,
    },
  },
  data: () => ({
    datePickerOpen: false,
    dateRange: [],
  }),
  computed: {
    dateRangeText() {
      return `${this.dateRange[0]} - ${this.dateRange[1]}`;
    },
  },
  watch: {
    datePickerOpen() {
      if (this.dateRange[1] === undefined && this.datePickerOpen === false) {
        // If the user only selects one date and closes the menu, this selects a default 'end' date.
        this.dateRange = [
          this.dateRange[0],
          moment(this.dateRange[0]).add(7, 'days').format('YYYY-MM-DD'),
        ];
        this.dateUpdateEventReceiver(this.dateRange);
      }
    },
  },
  async created() {
    if (this.$route.query.from_date && this.$route.query.to_date) {
      // No need to re-route if these are both already set.
      this.dateRange = [this.$route.query.from_date, this.$route.query.to_date];
      this.dateUpdateEventReceiver(this.dateRange);
    } else {
      this.dateRange = this.initialDateRange;
      this.dateUpdateEventReceiver(this.dateRange);
    }
  },
  methods: {
    moment,
    dayjs,
    setQueryParam(params) {
      const newQuery = {
        ...this.$route.query,
        ...(params || undefined),
      };

      if (_.isEqual(this.$route.query, newQuery)) {
        return;
      }

      this.$router.replace({
        query: newQuery,
      });
    },
    async dateUpdated(dateRange) {
      this.dateRange = dateRange;
    },
    dateUpdateEventReceiver(dateRange) {
      const [fromDate, toDate] = dateRange.sort().map(dayjs);
      let newToDate = toDate;
      const newFromDate = fromDate;
      const daysDiff = newToDate.diff(newFromDate, 'days');

      if (this.daysLimit && daysDiff >= this.daysLimit) {
        newToDate = newFromDate.add(this.daysLimit - 1, 'days');

        this.pickedDates = [
          newFromDate.format('YYYY-MM-DD'),
          newToDate.format('YYYY-MM-DD'),
        ];

        /**
         * First change the query param and after show the message
         * because of clearing system messages on each route change
         */
        this.setQueryParam({
          from_date: this.pickedDates[0],
          to_date: this.pickedDates[1],
        });

        this.dateUpdated(this.pickedDates);
      } else {
        this.setQueryParam({
          from_date: fromDate.format('YYYY-MM-DD'),
          to_date: toDate.format('YYYY-MM-DD'),
        });
      }
      this.afterDatePicked(this.dateRange);
    },
  },
};
</script>
