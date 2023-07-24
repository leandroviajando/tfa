<template>
  <v-autocomplete
    id="balance-filter"
    :value="selectedBalanceId"
    :label="$t('balance')"
    :items="balances"
    dense
    @change="(value) => $emit('set-selected-balance-id', value)"
  />
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  props: {
    selectedBalanceId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {};
  },
  computed: {
    ...mapGetters(['balances']),
  },
  async created() {
    await this.fetchBalances();
  },
  methods: {
    ...mapActions(['fetchBalances']),
  },
};
</script>
