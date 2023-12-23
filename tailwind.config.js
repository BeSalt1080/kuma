/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/**/*.vue'],
  theme: {
    extend: {
      colors:{
        primary1: '#132A13',
        primary2: '#31572C',
        primary3: '#4F772D',
        primary4: '#90A955',
        surface: '#ECF39E'
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    
  ],
}

