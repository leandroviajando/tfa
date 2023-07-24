module.exports = () => {
  const cspCommonConfig = {
    'default-src': ["'self'", 'https:'],
    'child-src': ["'none'"],
    'script-src': ["'self'", 'https:'],
    'object-src': ["'none'"],
    'font-src': ["'self'", 'https:', 'https://fonts.gstatic.com'],
    'style-src': ["'self'", 'https:', 'https://fonts.googleapis.com'],
    'connect-src': ["'self'"],
  };

  cspCommonConfig['connect-src'] = ['*'];
  cspCommonConfig['script-src'].push("'unsafe-eval'");
  cspCommonConfig['style-src'].push("'unsafe-inline'");

  return cspCommonConfig;
};
