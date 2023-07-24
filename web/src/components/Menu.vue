<template>
  <v-navigation-drawer
    v-model="navBar.show"
    :expand-on-hover="navBar.minify"
    app
    clipped
    dark
    :right="$vuetify.rtl"
    :hide-overlay="true"
  >
    <v-list dense nav>
      <template v-for="route in navElements">
        <v-list-item
          :key="route.path"
          color="primary"
          class="v-list-item--doc"
          link
          ripple
          :to="route.path"
        >
          <v-list-item-icon v-if="route.icon">
            <v-icon v-text="route.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="$t(route.meta.title)" />
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>
<script>
import { mapState } from 'vuex';

export default {
  props: {
    routes: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    ...mapState(['navBar']),
    navElements: (vm) => {
      return vm.$props.routes.filter(({ meta: { hidden, secret } }) => {
        if (hidden) {
          return false;
        }
        if (secret) {
          if (vm.$store.getters.showSecretOptions === true) {
            return true;
          }
          return false;
        }
        return true;
      });
    },
  },
};
</script>
