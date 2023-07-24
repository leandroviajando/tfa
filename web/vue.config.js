const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
const createCSPConfig = require('./csp');

const cspConfig = createCSPConfig(process.env.NODE_ENV);

const cspContent = Object.keys(cspConfig)
  .map((key) => {
    const valueList = cspConfig[key];
    return `${key} ${valueList.join(' ')}`;
  })
  .join(';');

process.env.VUE_APP_CSP_CONTENT = cspContent;

const webpackPlugins = [];

if (process.env.PERF) {
  webpackPlugins.push(new BundleAnalyzerPlugin());
}

module.exports = {
  transpileDependencies: [
    'vuetify',
    /\/node_modules\/vue-echarts\//,
    /\/node_modules\/resize-detector\//,
  ],
  publicPath: '/',
  productionSourceMap: process.env.NODE_ENV !== 'production',
  devServer: {
    disableHostCheck: true,
  },
  configureWebpack: {
    plugins: webpackPlugins,
    optimization: {
      splitChunks: {
        maxInitialRequests: 4,
        maxAsyncRequests: 6,
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/](vuetify)[\\/]/,
            name: 'vendor',
            chunks: 'all',
          },
          commons: {
            name: 'commons',
            chunks: 'initial',
            minChunks: 2,
          },
        },
      },
    },
  },
  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      args[0].title = 'Treasury Automation';
      return args;
    });
    config.plugin('prefetch').tap((options) => {
      options[0].fileBlacklist = options[0].fileBlacklist || [];
      options[0].fileBlacklist.push(/pdfmake(\.[^.]+)?\.js$/);
      options[0].fileBlacklist.push(/xlsx(\.[^.]+)?\.js$/);
      options[0].fileBlacklist.push(/canvg(\.[^.]+)?\.js$/);
      options[0].fileBlacklist.push(/coverage(\.[^.]+)?\.js$/);
      options[0].fileBlacklist.push(/editor(\.[^.]+)?\.js$/);
      return options;
    });
  },
};
//   options.fileBlackList.push([/myasyncRoute(.)+?\.js$/]);
