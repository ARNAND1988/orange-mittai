// tailwind.config.js
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
  extend: {
    colors: {
      brand: {
        orange: '#F97316',
        orangeDark: '#EA580C',
        red: '#C2410C',
        gold: '#FACC15',
        green: '#166534',
      },
      surface: {
        page: '#FFF7ED',
        card: '#FFFFFF',
        border: '#E5E7EB',
      },
      text: {
        primary: '#1F2937',
        secondary: '#6B7280',
        muted: '#9CA3AF',
      },
    },
  },



//    extend: {
//      colors: {
//          brand: {
//            softer: '#ffe4b3',
//            strong: '#e67300',
//          },
//          'fg-brand': {
//            strong: '#e67300',
//          },
//        orangeMittai: {
//          50:  '#fff8f1',
//          100: '#ffe4b3',
//          200: '#ffc680',
//          300: '#ffa64d',
//          400: '#ff8c1a',   // NEW – primary button
//          500: '#e67300',   // NEW – hover / emphasis
//        },
//
//        /* Optional semantic aliases (HIGHLY recommended) */
//        brand: {
//          DEFAULT: '#ff8c1a',
//          strong: '#e67300',
//          soft: '#ffe4b3',
//        },
//      },
//    },
  },
  plugins: [require("flowbite/plugin")],
};
