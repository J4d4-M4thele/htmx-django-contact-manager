/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './contacts/templates/**/*.html',
    './contacts/forms.py'
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
}

