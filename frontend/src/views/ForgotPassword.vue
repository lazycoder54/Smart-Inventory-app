<template>
  <div class="full-screen-forgot-password">
    <div class="forgot-password-container">
      <h2 class="text-2xl font-bold mb-6 text-center">Reset Password</h2>
      <form @submit.prevent="resetPassword" class="space-y-4">
        <div class="input-group">
          <input
            type="text"
            v-model="username"
            placeholder="Username"
            class="input-field"
            required
          />
        </div>
        <div class="input-group">
          <input
            type="password"
            v-model="newPassword"
            placeholder="New Password"
            class="input-field"
            required
          />
        </div>
        <button type="submit" class="reset-button w-full">
          Reset Password
        </button>
      </form>
      <div class="mt-4 text-center">
        <button @click="goToLogin" class="text-blue-500 hover:underline">
          Back to Login
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";
import { ref } from "vue";
import axios from "../api/inventory";

export default {
  setup() {
    const toast = useToast();
    const router = useRouter();

    const username = ref("");
    const newPassword = ref("");

    const resetPassword = async () => {
      try {
        const response = await axios.post("/auth/forgot-password", {
          username: username.value,
          new_password: newPassword.value,
        });

        toast.success(response.data.message || "Password reset successful!");

        router.push("/login");
      } catch (error) {
        const message =
          error.response?.data?.message || "Failed to reset password.";

        toast.error(message);
        console.error("Password reset failed:", error);
      }
    };

    const goToLogin = () => {
      router.push("/login");
    };

    return {
      username,
      newPassword,
      resetPassword,
      goToLogin,
    };
  },
};
</script>

<style scoped>
body {
  overflow: hidden;
  margin: 0;
}

.full-screen-forgot-password {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background-size: cover;
  background-position: center;
}

.forgot-password-container {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  height: 50vh;
  width: 40vw;
}

.input-group {
  margin-bottom: 20px;
}

.input-field {
  width: 100%;
  padding: 15px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.reset-button {
  background-color: #4caf50;
  color: white;
  padding: 15px 30px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.reset-button:hover {
  background-color: #45a049;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

.text-blue-500 {
  font-size: 14px;
  color: #3490dc;
  text-decoration: none;
  margin-top: 10px;
}

.text-blue-500:hover {
  text-decoration: underline;
}
</style>
