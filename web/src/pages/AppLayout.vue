<template>
  <div>
    <v-app-bar
      app
      dark
      elevation="2"
      :clipped-right="!$vuetify.rtl"
      :clipped-left="!$vuetify.rtl"
      fixed
    >
      <v-app-bar-nav-icon
        color="primary"
        @click.stop="TOGGLE_NAVBAR($vuetify.breakpoint.mdAndDown)"
      />
      <v-toolbar-title>
        <span class="primary--text title text-capitalize">
          {{ $t('treasuryForecasts') }}{{ $route.meta.title ? ' — ' : '' }}
          <span>
            {{
              $route.meta.longTitle
                ? $t($route.meta.longTitle)
                : $t($route.meta.title)
            }}</span
          >
        </span>
      </v-toolbar-title>
      <v-spacer />
      <v-menu offset-y top>
        <template #activator="{ on, attrs }">
          <v-btn
            id="profile-menu-button"
            color="primary"
            small
            fab
            v-bind="attrs"
            v-on="on"
            >{{ user.firstname[0] + user.lastname[0] }}</v-btn
          >
        </template>
        <v-card>
          <v-divider></v-divider>
          <v-list>
            <v-list-item link to="/signout">
              <v-list-item-icon>
                <v-icon>mdi-logout</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                {{ $t('signout') }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
          <v-card-actions>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-menu>
    </v-app-bar>
    <Navbar />
    <PageContainer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import PageContainer from '@/components/PageContainer.vue';
import { mapMutations } from 'vuex';

export default {
  components: { Navbar, PageContainer },
  data: () => ({
    user: {
      firstname: 'Treasury',
      lastname: 'Automation',
    },
  }),
  computed: {},
  created() {},
  methods: {
    ...mapMutations(['TOGGLE_NAVBAR']),
  },
};
</script>
