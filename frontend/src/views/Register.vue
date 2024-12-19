<template>
  <div class="full-screen-register">
    <div class="register-container">
      <h2 class="text-3xl font-bold mb-8 text-center">Register</h2>
      <form @submit.prevent="register" class="space-y-6">
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
            type="email"
            v-model="email"
            placeholder="Email"
            class="input-field"
            required
          />
        </div>
        <div class="input-group">
          <input
            type="password"
            v-model="password"
            placeholder="Password"
            class="input-field"
            required
          />
        </div>
        <button type="submit" class="register-button w-full">Register</button>
      </form>
      <div class="mt-12 text-center">
        <button
          @click="goToLogin"
          class="text-blue-500 hover:underline back-to-login"
        >
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
    const email = ref(router.currentRoute.value.query.email || "");
    const password = ref("");

    const register = async () => {
      try {
        const response = await axios.post("/auth/register", {
          username: username.value,
          email: email.value,
          password: password.value,
          uid: router.currentRoute.value.query.uid,
        });

        toast.success(response.data.message || "Registration successful!");
        router.push("/login");
      } catch (error) {
        const message = error.response?.data?.message || "Registration failed.";
        toast.error(message);

        if (error.response?.data?.message.includes("EMAIL_EXISTS")) {
          toast.error("This email is already registered. Please log in.");
          router.push("/login");
        }
      }
    };

    const goToLogin = () => {
      router.push("/login");
    };

    return {
      username,
      email,
      password,
      register,
      goToLogin,
    };
  },
};
</script>

<style scoped>
.full-screen-register {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  background-color: #f7f7f7;
}

.register-container {
  padding: 60px;
  border-radius: 12px;
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.25);
  width: 100%;
  max-width: 500px;
  background-color: white;
}

.input-group {
  margin-bottom: 20px;
}

.input-field {
  width: 100%;
  padding: 18px;
  font-size: 18px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.register-button {
  background-color: #4caf50;
  color: white;
  padding: 18px;
  font-size: 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 15px;
}

.back-to-login {
  color: blue;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  padding: 12px;
}

h2 {
  font-size: 32px;
}
</style>
