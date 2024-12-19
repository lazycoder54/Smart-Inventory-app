import { defineStore } from "pinia";
import { jwtDecode } from "jwt-decode";

export const useUserStore = defineStore("user", {
  state: () => ({
    username: "",
  }),
  actions: {
    initializeFromToken() {
      const token = localStorage.getItem("jwt_token");
      if (token) {
        try {
          const decoded = jwtDecode(token);
          if (decoded && decoded.username) {
            this.username = decoded.username;
          } else {
            throw new Error("Invalid token payload");
          }
        } catch (error) {
          this.username = "";
        }
      } else {
        this.username = "";
      }
    },

    setUsername(name) {
      this.username = name;
    },
  },
});
