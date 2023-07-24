<template>
  <chart
    ref="lineData"
    :options="lineData"
    :init-options="initOptions"
    style="width: 80%; margin-left: 10%; min-height: 300px"
    auto-resize
  />
</template>

<script>
import ECharts from 'vue-echarts';
import 'echarts/lib/chart/line';
import 'echarts/lib/component/legend';
import 'echarts/lib/component/tooltip';

export default {
  components: {
    chart: ECharts,
  },
  props: {
    varianceData: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      initOptions: {
        renderer: 'canvas',
      },
    };
  },
  computed: {
    varianceDates() {
      return this.varianceData.map((i) => i.dt);
    },
    actualAmount() {
      return this.varianceData.map((i) => i.actual_amount);
    },
    forecastedAmount() {
      return this.varianceData.map((i) => i.forecasted_amount);
    },
    lineData() {
      return {
        title: {
          text: 'Variance',
        },
        legend: {
          data: [this.$t('variance.actual'), this.$t('variance.forecast')],
        },
        tooltip: {
          trigger: 'axis',
          formatter: this.formatTooltip,
          axisPointer: {
            type: 'cross',
            label: {
              backgroundColor: '#505765',
            },
          },
        },
        xAxis: {
          type: 'category',
          data: this.varianceDates,
        },
        yAxis: [
          {
            type: 'value',
            axisLabel: {
              formatter: '$ {value}',
            },
            yAxisIndex: 0,
            splitLine: {
              show: false,
            },
          },
        ],
        series: [
          {
            id: 'actual_amount',
            name: this.$t('variance.actual'),
            data: this.actualAmount,
            type: 'line',
            yAxisIndex: 0,
          },
          {
            id: 'forecasted_amount',
            name: this.$t('variance.forecast'),
            data: this.forecastedAmount,
            type: 'line',
            yAxisIndex: 0,
          },
        ],
      };
    },
  },
  methods: {
    formatTooltip(args) {
      const pointDate = args[0].axisValue;
      const dataPoint = this.varianceData.find((d) => d.dt === pointDate);
      const regularTooltip = args
        .map((a) => `${a.marker} ${a.seriesName}: ${dataPoint[a.seriesId]}`)
        .join('<br />');
      return [
        pointDate,
        regularTooltip,
        `${this.$t('variance.variance')}: ${dataPoint.variance}`,
        `${this.$t('variance.mape')}: ${dataPoint.mape}`,
      ].join('<br />');
    },
  },
};
</script>
