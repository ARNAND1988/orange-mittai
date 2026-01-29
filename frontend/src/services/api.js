import axios from "axios";
import { API_BASE_URL } from "../config/api";
import { showGlobalToast } from "@/utils/toast";


/**
 * Axios instance
 */
const axiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

/**
 * REQUEST INTERCEPTOR
 * - Attaches JWT token if present
 */
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

/**
 * RESPONSE INTERCEPTOR
 * - Returns response.data by default
 * - Handles auth & errors safely
 */
axiosInstance.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.config?.method === "options") {
      return Promise.reject(error);
    }
    if (error.response) {
      const { status, data } = error.response;
      const detail = data?.detail;
      const message =
        detail ||
        data?.message ||
        "Something went wrong";

      // Detect real auth failures (token expired / invalid)
      const isAuthFailure =
        typeof detail === "string" &&
        (
          detail.toLowerCase().includes("token") ||
          detail.toLowerCase().includes("credential")
        );

      switch (status) {
        case 401:
          if (isAuthFailure) {
            localStorage.removeItem("access_token");
            showGlobalToast(
              "Session expired. Please log in again.",
              "error"
            );
          } else {
            showGlobalToast(
              "You are not authorized to perform this action.",
              "error"
            );
          }
          break;

        case 403:
          showGlobalToast(
            "You don’t have permission to perform this action.",
            "error"
          );
          break;

        case 404:
          showGlobalToast(
            "Requested resource not found.",
            "error"
          );
          break;

        case 422:
          showGlobalToast(message, "error");
          break;

        case 500:
        case 502:
        case 503:
          showGlobalToast(
            "Server error. Please try again later.",
            "error"
          );
          break;

        default:
          showGlobalToast(message, "error");
      }
    } else {
      // Network / CORS / timeout
      showGlobalToast(
        "Network error. Please check your connection.",
        "error"
      );
    }

    return Promise.reject(error.response?.data || error);
  }
);

/**
 * Export the axios instance directly
 * (all services must import this)
 */
export default axiosInstance;
