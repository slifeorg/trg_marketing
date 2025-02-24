import colors from 'tailwindcss/colors'
import frappeUIPreset from 'frappe-ui/src/tailwind/preset'

export default {
  presets: [frappeUIPreset],
  content: [
    './index.html',
    './src/**/*.{vue,js,jsx,tsx}',
    './node_modules/frappe-ui/src/components/**/*.{vue,js,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: colors.blue
      }
    }
  }
}