import { createApp } from 'vue'
import { FrappeUI, Button, FeatherIcon } from 'frappe-ui'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './index.css'

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(FrappeUI)
app.use(pinia)

app.component('Button', Button)
app.component('FeatherIcon', FeatherIcon)

app.mount('#app')