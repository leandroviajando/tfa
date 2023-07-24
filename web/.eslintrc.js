module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es2020: true,
    jest: true,
  },
  extends: [
    'airbnb-base',
    'plugin:vue/recommended',
    'plugin:jest/all',
    'plugin:jest-dom/recommended',
    '@vue/prettier',
    'plugin:prettier/recommended',
    'plugin:vue-pug/vue3-recommended',
  ],
  parserOptions: {
    parser: 'babel-eslint',
  },
  settings: {
    'import/resolver': {
      webpack: {
        config: 'node_modules/@vue/cli-service/webpack.config.js',
      },
    },
  },
  rules: {
    'prettier/prettier': process.env.ESLINT_PRETTIER_RULE
      ? process.env.ESLINT_PRETTIER_RULE
      : 'error',
    'spaced-comment': process.env.ESLINT_SPACED_COMMENT_RULE
      ? process.env.ESLINT_SPACED_COMMENT_RULE
      : 'error',
    'vue/valid-v-slot': ['error', { allowModifiers: true }],
    'no-param-reassign': ['error', { props: false }],
    'import/no-extraneous-dependencies': ['error', { devDependencies: true }],
    camelcase: 'off',
    'import/prefer-default-export': 'off',
    'jest/no-hooks': 'off',
    'jest/prefer-expect-assertions': 'off',
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-else-return': 'off',
  },
};
