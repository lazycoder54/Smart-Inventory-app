import { createRouter, createWebHistory } from "vue-router";
import Login from "./views/Login.vue";
import AddItemPage from "./views/AddItemPage.vue";
import UpdateItemPage from "./views/UpdateItemPage.vue";
import ListItemsPage from "./views/ListItemsPage.vue";
import AddNLPPage from "./views/AddNLPPage.vue";
import AddVoicePage from "./views/AddVoicePage.vue";
import Dashboard from "./views/Dashboard.vue";
import Register from "./views/Register.vue";
import ForgotPassword from "./views/ForgotPassword.vue";
import ManageUsers from "./views/ManageUsers.vue";
import Reports from "./views/Reports.vue";
import Analytics from "./views/Analytics.vue";
import Sales from "./views/Sales.vue";
import Customers from "./views/Customers.vue";
import Notifications from "./views/Notifications.vue";
import Help from "./views/Help.vue";
import Support from "./views/Support.vue";
import ActivityLog from "./views/ActivityLog.vue";
import Orders from "./views/Orders.vue";
import MoveItem from "./views/MoveItem.vue";
import ShowSearch from "./views/ShowSearch.vue";
import Profile from "./views/Profile.vue";

const routes = [
  { path: "/register", component: Register },
  { path: "/login", component: Login },
  { path: "/", redirect: "/login" },
  { path: "/forgot-password", component: ForgotPassword },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },

  { path: "/add-item", component: AddItemPage, meta: { requiresAuth: true } },
  {
    path: "/update-item/:itemId",
    component: UpdateItemPage,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: "/list-items",
    component: ListItemsPage,
    meta: { requiresAuth: true },
  },
  { path: "/add-nlp", component: AddNLPPage, meta: { requiresAuth: true } },
  { path: "/add-voice", component: AddVoicePage, meta: { requiresAuth: true } },
  {
    path: "/manage-users",
    component: ManageUsers,
    meta: { requiresAuth: true },
  },
  { path: "/reports", component: Reports, meta: { requiresAuth: true } },
  { path: "/analytics", component: Analytics, meta: { requiresAuth: true } },
  { path: "/sales", component: Sales, meta: { requiresAuth: true } },
  { path: "/customers", component: Customers, meta: { requiresAuth: true } },
  { path: "/orders", component: Orders, meta: { requiresAuth: true } },
  {
    path: "/notifications",
    component: Notifications,
    meta: { requiresAuth: true },
  },
  { path: "/help", component: Help, meta: { requiresAuth: true } },
  { path: "/support", component: Support, meta: { requiresAuth: true } },
  { path: "/profile", component: Profile, meta: { requiresAuth: true } },
  { path: "/move", component: MoveItem, meta: { requiresAuth: true } },
  { path: "/show", component: ShowSearch, meta: { requiresAuth: true } },

  {
    path: "/activity-log",
    component: ActivityLog,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to protect routes that require authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("jwt_token");
  if (to.matched.some((record) => record.meta.requiresAuth) && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;
