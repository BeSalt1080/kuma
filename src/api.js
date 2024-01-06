import axios from "axios";
import { useRouter } from "vue-router";

const authService = axios.create({
  baseURL: "http://127.0.0.1:5000",
  withCredentials: true,
  xsrfCookieName: "csrf_access_token",
});
export { authService };

const COOKIE_EXPIRED_MSG = "Token has expired";
const router = useRouter()
authService.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    try {
      const error_message = error.response.data.msg;
      switch (error.response.status) {
        case 401:
          if (!error.config.retry && error_message === COOKIE_EXPIRED_MSG) {
            error.config.retry = true;
            const refreshResponse = await authService.post("/refresh");
            if (refreshResponse.status === 200) {
              return authService(error.config);
            } else {
              router.push("{name:'login'}");
            }
          }
          break;
        case 404:
          // Handle 404 error
          break;
        case 422:
          // Handle 422 error
          return error.response;
        default:
          // Handle other errors
          break;
      }
      return Promise.reject(error);
    } catch (e) {
      throw e;
    }
  }
);
