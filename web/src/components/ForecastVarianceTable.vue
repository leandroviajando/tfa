<template>
  <v-data-table
    :headers="headers"
    :items="data"
    :items-per-page="10"
  ></v-data-table>
</template>

<script>
export default {
  props: {
    varianceData: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      data: this.varianceData,
      headers: [
        { text: this.$t('variance.date'), value: 'dt' },
        { text: this.$t('variance.actual'), value: 'actual_amount' },
        { text: this.$t('variance.forecast'), value: 'forecast_amount' },
        { text: this.$t('variance.variance'), value: 'variance' },
        { text: this.$t('variance.mape'), value: 'mape' },
      ],
    };
  },
  watch: {
    varianceData(newValue) {
      this.data = newValue;
    },
  },
};
</script>
