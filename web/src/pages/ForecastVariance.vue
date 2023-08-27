<template>
  <v-container fluid>
    <v-row text-xs-center wrap no-gutters dense>
      <v-card width="100%" flat>
        <v-card-text>
          <v-row justify="start" align="center" dense>
            <v-col cols="4">
              <BalanceFilter
                :selected-balance-id="selectedBalanceId"
                @set-selected-balance-id="setSelectedBalanceId"
              />
            </v-col>
            <v-col cols="4">
              <v-autocomplete
                id="aggregate-type-filter"
                :value="aggregateType"
                dense
                :label="$t('variance.scale')"
                :items="[
                  { value: 'daily', text: $t('variance.daily') },
                  { value: 'weekly', text: $t('variance.weekly') },
                  { value: 'monthly', text: $t('variance.monthly') },
                ]"
                @change="setAggregateType"
              />
            </v-col>
            <v-col cols="4">
              <date-range-filter
                :initial-date-range="initialDateRange"
                :after-date-picked="fetchVariances"
                :max-date="moment().format('YYYY-MM-DD')"
                :days-limit="365"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-container fluid>
              <v-tabs v-model="tabs" centered>
                <v-tab id="tab_chart" key="tab-chart">{{
                  $t('variance.chart')
                }}</v-tab>
                <v-tab id="tab_table" key="tab-table">{{
                  $t('variance.table')
                }}</v-tab>
              </v-tabs>
              <v-tabs-items v-model="tabs">
                <v-tab-item key="tab-chart">
                  <SPForecastVarianceChart :variance-data="varianceData.data" />
                </v-tab-item>
                <v-tab-item key="tab-table">
                  <v-container fluid>
                    <SPForecastVarianceTable
                      :variance-data="varianceData.data"
                    />
                  </v-container>
                </v-tab-item>
              </v-tabs-items>
            </v-container>
          </v-row>
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import BalanceFilter from '@/components/BalanceFilter.vue';
import DateRangeFilter from '@/components/DateRangeFilter';
import SPForecastVarianceChart from '@/components/ForecastVarianceChart.vue';
import SPForecastVarianceTable from '@/components/ForecastVarianceTable.vue';
import axios from '@/services/axios';
import moment from 'moment';

export default {
  components: {
    SPForecastVarianceChart,
    SPForecastVarianceTable,
    BalanceFilter,
    DateRangeFilter,
  },
  data() {
    return {
      tabs: null,
      loadingData: false,
      varianceData: [],
      initialDateRange: [
        moment().subtract(7, 'days').format('YYYY-MM-DD'),
        moment().format('YYYY-MM-DD'),
      ],
      controller: new AbortController(),
    };
  },
  computed: {
    aggregateType() {
      return this.$route.query.aggregateType;
    },
    selectedBalanceId() {
      return this.$route.query.balanceId
        ? parseInt(this.$route.query.balanceId, 10)
        : null;
    },
  },
  methods: {
    moment,
    async fetchVariances() {
      if (this.aggregateType) {
        this.loadingData = true;
        // aborting pending request and creating new controller for a new request
        this.controller.abort();
        this.controller = new AbortController();
        const resp = await axios.get(
          `/api/v1/forecast_variance/${this.$route.query.balanceId}`,
          {
            signal: this.controller.signal,
            params: {
              from_date: this.$route.query.from_date,
              to_date: this.$route.query.to_date,
            },
          }
        );

        this.varianceData = resp.data;
        this.loadingData = false;
      }
    },
    async setQueryParam(type, value) {
      this.$router.replace({
        query: {
          ...this.$route.query,
          [type]: value || undefined,
        },
      });
    },
    async setAggregateType(value) {
      await this.setQueryParam('aggregateType', value);
      if (this.$route.query.from_date && this.$route.query.to_date) {
        this.fetchVariances();
      }
    },
    async setSelectedBalanceId(balanceId) {
      await this.setQueryParam('balanceId', balanceId);
      await this.fetchVariances();
    },
  },
};
</script>
