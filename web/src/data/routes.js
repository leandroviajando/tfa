import AppLayout from '@/pages/AppLayout.vue';
import ForecastVariance from '@/pages/ForecastVariance.vue';
// All main navigation routes are defined here as children to the dashboard route.
// Note: Children are not used in the navigation, as children in vue-router are for nesting layouts within one another.
export default [
  {
    name: 'dashboard',
    path: '/',
    redirect: '/forecast-variance',
    component: AppLayout,
    meta: { title: 'dashboard' },
    children: [
      {
        name: 'forecast-variance',
        path: '/forecast-variance',
        icon: 'mdi-chart-areaspline',
        component: ForecastVariance,
        meta: {
          title: 'forecastVariance',
        },
      },
    ],
  },
  {
    path: '*',
    redirect: '/',
    meta: { hidden: true },
  },
];
