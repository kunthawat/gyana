module.exports = {
  purge: [
    './assets/**/*.js',
    './assets/**/*.vue',
    './templates/**/*.html',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
    container: {
      center: true,
      // padding: '2rem',
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
