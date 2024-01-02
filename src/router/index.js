import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import PolicyView from "../views/PolicyView.vue";
import TermsView from "../views/TermsView.vue";
import ContactView from "../views/ContactView.vue";
import ProductView from "../views/Product/ProductView.vue";
import { useAuthStore } from "../stores/auth";
import DetailedView from "../views/Product/DetailedView.vue";
import OrderDetailedView from "../views/User/Order/DetailedView.vue";
import CartView from "../views/CartView.vue";
import CheckoutView from "../views/CheckoutView.vue";
import PaymentView from "../views/PaymentView.vue";
import OrderView from "@/views/User/Order/OrderView.vue";
import AccountInfoView from "@/views/User/AccountInfoView.vue";
import AccountView from "@/views/User/AccountView.vue";
import AddressView from "@/views/User/AddressView.vue";
import WishlistView from "@/views/User/WishlistView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: {
        isGuest: true,
      },
    },
    {
      path: "/register",
      name: "register",
      component: RegisterView,
      meta: {
        isGuest: true,
      },
    },
    {
      path: "/policy",
      name: "policy",
      component: PolicyView,
    },
    {
      path: "/terms",
      name: "terms",
      component: TermsView,
    },
    {
      path: "/contact",
      name: "contact",
      component: ContactView,
    },
    {
      path: "/product/:id",
      name: "product.show",
      component: DetailedView,
    },
    {
      path: "/latest",
      name: "latest",
      component: ProductView,
      props: { category: "Latest" },
    },
    {
      path: "/sale",
      name: "sale",
      component: ProductView,
      props: { category: "Sale" },
    },
    {
      path: "/wishlist",
      name: "wishlist",
      component: WishlistView,
    },
    {
      path: "/account",
      name: "account",
      component: AccountView,
    },
    {
      path: "/account/info",
      name: "account.info",
      component: AccountInfoView,
    },
    {
      path: "/address",
      name: "address",
      component: AddressView,
    },

    {
      path: "/accessory",
      name: "accessory",
      component: ProductView,
      props: { category: "Accessory" },
    },
    {
      path: "/brand/:categories",
      name: "brand",
      component: ProductView,
      props: { category: "Brand" },
    },
    {
      path: "/men/:categories",
      name: "men",
      component: ProductView,
      props: { category: "Men" },
    },
    {
      path: "/women/:categories",
      name: "women",
      component: ProductView,
      props: { category: "Women" },
    },
    {
      path: "/kids/:categories",
      name: "kids",
      component: ProductView,
      props: { category: "Kids" },
    },
    {
      path: "/cart",
      name: "cart",
      component: CartView,
      meta: { requiresAuth: true}
    },
    {
      path: "/order",
      name: "order",
      component: OrderView,
    },
    {
      path: "/order/detail",
      name: "order.detail",
      component: OrderDetailedView,
    },
    {
      path: "/order/checkout",
      name: "order.checkout",
      component: CheckoutView,
    },
    {
      path: "/order/payment",
      name: "order.payment",
      component: PaymentView,
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: () => import("../views/Admin/Dashboard.vue"),
      meta: {
        isAdmin: true,
      },
      props: { admin: "hello world" },
      children: [
        {
          path: "product",
          name: "product",
          component: () => import("../views/Admin/Product/Index.vue"),
        },
        {
          path: "product/create",
          name: "product.create",
          component: () => import("../views/Admin/Product/Create.vue"),
        },
        {
          path: "product/edit/:id",
          name: "product.edit",
          component: () => import("../views/Admin/Product/Edit.vue"),
        },
        {
          path: "banner",
          name: "banner",
          component: () => import("../views/Admin/Banner/Index.vue"),
        },
        {
          path: "banner/create",
          name: "banner.create",
          component: () => import("../views/Admin/Banner/Create.vue"),
        },
        {
          path: "banner/edit/:id",
          name: "banner.edit",
          component: () => import("../views/Admin/Banner/Edit.vue"),
        },
        {
          path: "shipping",
          name: "shipping",
          component: () => import("../views/Admin/Shipping/Index.vue"),
          
        },
        {
          path: "shipping/create",
          name: "shipping.create",
          component: () => import("../views/Admin/Shipping/Create.vue"),
        },
        {
          path: "shipping/edit/:id",
          name: "shipping.edit",
          component: () => import("../views/Admin/Shipping/Edit.vue"),
        },
        {
          path: "brand",
          name: "brand",
          component: () => import("../views/Admin/Brand/Index.vue"),
        },
        {
          path: "brand/create",
          name: "brand.create",
          component: () => import("../views/Admin/Brand/Create.vue"),
        },
        {
          path: "brand/edit/:id",
          name: "brand.edit",
          component: () => import("../views/Admin/Brand/Edit.vue"),
        },
        {
          path: "category",
          name: "category",
          component: () => import("../views/Admin/Category/Index.vue"),
        },
        {
          path: "category/create",
          name: "category.create",
          component: () => import("../views/Admin/Category/Create.vue"),
        },
        {
          path: "category/edit/:id",
          name: "category.edit",
          component: () => import("../views/Admin/Category/Edit.vue"),
        },
        {
          path: "gender",
          name: "gender",
          component: () => import("../views/Admin/Gender/Index.vue"),
        },
        {
          path: "gender/create",
          name: "gender.create",
          component: () => import("../views/Admin/Gender/Create.vue"),
        },
        {
          path: "gender/edit/:id",
          name: "gender.edit",
          component: () => import("../views/Admin/Gender/Edit.vue"),
        },
        {
          path: "order",
          name: "order.index",
          component: () => import("../views/Admin/Order/Index.vue"),
        },
        {
          path: "order/show/:id",
          name: "order.show",
          component: () => import("../views/Admin/Order/Create.vue"),
        },
        {
          path: "order/edit/:id",
          name: "order.edit",
          component: () => import("../views/Admin/Order/Edit.vue"),
        },
        {
          path: "payment",
          name: "payment",
          component: () => import("../views/Admin/Payment/Index.vue"),
        },
        {
          path: "payment/create",
          name: "payment.create",
          component: () => import("../views/Admin/Payment/Create.vue"),
        },
        {
          path: "payment/edit/:id",
          name: "payment.edit",
          component: () => import("../views/Admin/Payment/Edit.vue"),
        },
        {
          path: "size",
          name: "size",
          component: () => import("../views/Admin/Size/Index.vue"),
        },
        {
          path: "size/create",
          name: "size.create",
          component: () => import("../views/Admin/Size/Create.vue"),
        },
        {
          path: "size/edit/:id",
          name: "size.edit",
          component: () => import("../views/Admin/Size/Edit.vue"),
        },
      ],
    },
  ],
});

export default router;

router.beforeEach(async (to, from, next) => {
  const store = useAuthStore();
  await store.fetchUser();
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!store.isLoggedIn) {
      next({ name: "login" });
    } else {
      next();
    }
  }
  if (to.matched.some((record) => record.meta.isGuest)) {
    if (store.isLoggedIn) {
      next({ name: "home" });
    } else {
      next();
    }
  }
  if (to.matched.some((record) => record.meta.isAdmin)) {
    if (store.user.role != undefined) {
      if (store.user.role == 1) {
        next();
      }
    }
    next({ name: "home" });
  }
  next();
});
