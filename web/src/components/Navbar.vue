<template>
  <nav dark>
    <Menu :routes="mainRoutes"></Menu>
  </nav>
</template>

<script>
import routes from '@/data/routes';
import Menu from '@/components/Menu.vue';

export default {
  components: { Menu },
  computed: {
    mainRoutes() {
      return routes.find((r) => r.name === 'dashboard').children;
    },
  },
};
</script>
