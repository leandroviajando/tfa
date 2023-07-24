<template>
  <v-main
    :class="{
      navbarMinified: navbarMinified && navbarShow,
      navbarNotMinified: !navbarMinified && navbarShow,
      navbarClosed: !navbarShow,
    }"
  >
    <div class="page-wrpper">
      <div class="page-wrapper">
        <v-container fluid fill-height grid-list-md>
          <transition name="fade-transform" mode="out-in" fill-height>
            <router-view :key="$route.path" />
          </transition>
        </v-container>
      </div>
    </div>
    <v-footer height="auto" class="white pa-3 ml-6 app--footer">
      <span class="caption">
        TFA &copy; {{ new Date().getFullYear() }} - {{ environment }} - App
        version: {{ version }}
      </span>
    </v-footer>
  </v-main>
</template>

<script>
import config from '@/config';
import { mapGetters } from 'vuex';

export default {
  components: {},
  data: () => ({
    environment: config.TFA_ENV,
    version: config.TFA_VERSION,
    console,
  }),
  computed: {
    showTitle() {
      if (this.$route.meta.showTitle === false) {
        return false;
      }

      return !!this.$route.meta.title;
    },
    ...mapGetters(['navbarShow', 'navbarMinified']),
  },
};
</script>

<style scoped>
.page-wrapper {
  min-height: calc(100vh - 8vh);
}

.navbarNotMinified {
  padding-left: 236px !important;
}

.navbarClosed {
  margin-left: -20px !important;
}

.navbarMinified {
  padding-left: 36px !important;
}

/* fade-transform */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all 0.5s;
}

.fade-transform-enter {
  opacity: 0;
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
