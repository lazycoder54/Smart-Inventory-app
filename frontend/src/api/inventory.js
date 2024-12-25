import axios from "axios";
import { useUserStore } from "@/store/store";

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 20000,
});

// Request interceptor to add the token to every request
axiosInstance.interceptors.request.use(
  async (config) => {
    const token = localStorage.getItem("jwt_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh if expired
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 401) {
      const refreshToken = localStorage.getItem("refresh_token");
      const userStore = useUserStore();

      if (refreshToken) {
        try {
          const response = await axios.post(
            `${import.meta.env.VITE_API_BASE_URL}/auth/refresh`, 
            {},
            {
              headers: {
                Authorization: `Bearer ${refreshToken}`,
              },
            }
          );

          const newAccessToken = response.data.access_token;
          localStorage.setItem("jwt_token", newAccessToken);
          error.config.headers["Authorization"] = `Bearer ${newAccessToken}`;
          return axios(error.config);
        } catch (err) {
          console.error("Refresh token failed", err);
          window.location.href = "/login";
        }
      } else {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
