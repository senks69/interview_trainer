import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "auth",
    component: () => import("../components/AuthPage.vue"),
  },
  {
    path: "/home",
    name: "homw",
    component: () => import("../components/MainPage.vue"),
  },
  {
    path: "/interview",
    name: "interview",
    component: () => import("../components/InterviewPage.vue"),
  },
  {
    path: "/feedback",
    name: "feedback",
    component: () => import("../components/FeedbackPage.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
