module.exports = {
  // Exit the test suite immediately upon first failed test.
  bail: 1,
  collectCoverageFrom: ['**/*.{js,vue}', '!**/node_modules/**'],
  coverageReporters: ['cobertura', 'text', 'text-summary'],
  coverageDirectory: './coverage',
  preset: '@vue/cli-plugin-unit-jest',
  // Use only one worker to avoid overload on GitLab runner.
  maxWorkers: 2,
  moduleFileExtensions: ['js', 'jsx', 'json', 'vue'],
  setupFilesAfterEnv: ['./jest.setup.js'],
  transformIgnorePatterns: ['node_modules/(?!(vuetify|axios))/'],
  transform: {
    '.*\\.(vue)$': 'vue-jest',
    '.*\\.(js)$': 'babel-jest',
  },
};
