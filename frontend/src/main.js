import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import 'flowbite'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faUser,
  faUserShield,
  faGear,
  faBoxesStacked,
  faClipboardList,
  faHouse,
  faBars,
  faCartShopping,
} from "@fortawesome/free-solid-svg-icons"

import router from './router' // import router

library.add(
  faUser,
  faUserShield,
  faGear,
  faBoxesStacked,
  faClipboardList,
  faHouse,
  faBars,
  faCartShopping
)


createApp(App)
.use(router)
.component('font-awesome-icon', FontAwesomeIcon)
.mount('#app')


