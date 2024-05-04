import '../../css/cast_vue/styles.css';
import '../../css/cast_vue/pygments.css';
import 'vite/modulepreload-polyfill';  // recommended by django-vite, dunno why

import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { createRouter, createWebHistory } from "vue-router";
import config from './config';
import LoadPostList from "./components/LoadPostList.vue";
import PostDetail from "./components/PostDetail.vue";

import App from './App.vue';

const routes = [
    {
        path: "/",
        name: "PostList",
        component: LoadPostList,
    },
    {
        path: "/:slug/",
        name: "PostDetail",
        component: PostDetail,
    },
];

console.log("blog detail url: ", config.blogDetailUrl);
console.log("vue route name: ", config.vueRouteName);
const router = createRouter({
    history: createWebHistory(config.blogUrl),
    routes,
  });

const app = createApp(App)
app.use(router);

const pinia = createPinia()
app.use(pinia);

app.mount("#app")
