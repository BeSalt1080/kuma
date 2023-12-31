import axios from "axios";

const authService = axios.create({
  baseURL: "http://127.0.0.1:5000",
  withCredentials: true,
  xsrfCookieName: "csrf_access_token",
});
export { authService };

const COOKIE_EXPIRED_MSG = "Token has expired";
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
            return authService(error.config);
          }
          break;
        case 404:
          router.push("/404");
          break;
        case 422:
          return error.response.data;
        default:
          break;
      }
      return error.response;
    } catch (e) {
      throw e
    }
  }
);
