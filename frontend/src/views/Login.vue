<template>
  <div class="full-screen-login">
    <div class="login-container">
      <h2 class="text-2xl font-bold mb-6 text-center">Login</h2>
      <form @submit.prevent="login" class="space-y-4">
        <input
          type="email"
          v-model="email"
          placeholder="Email"
          class="w-full p-1rem 1.5rem border rounded-lg focus:outline-none focus:border-gray-900"
          required
        />
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          class="w-full p-1rem 1.5rem border rounded-lg focus:outline-none focus:border-gray-900"
          required
        />
        <button
          type="submit"
          class="w-full bg-blue-500 text-white py-1.2rem px-2rem rounded-lg font-weight: bold hover:bg-blue-700"
        >
          Login
        </button>
      </form>

      <!-- Google Sign-In Button -->
      <button
        @click="googleSignIn"
        class="w-full bg-red-500 text-white py-1.2rem px-2rem rounded-lg font-weight: bold hover:bg-red-700 mt-4"
      >
        Sign in with Google
      </button>

      <!-- Register and Forgot Password Links -->
      <div class="mt-4 text-center">
        <button
          @click="goToRegister"
          class="mr-4 px-6 py-2 font-semibold rounded-lg shadow-md hover:bg-blue-700 hover:text-white transition duration-300 ease-in-out"
        >
          Register
        </button>
        <button
          @click="goToForgotPassword"
          class="px-6 py-2 font-semibold rounded-lg shadow-md hover:bg-blue-700 hover:text-white transition duration-300 ease-in-out"
        >
          Forgot Password?
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { auth } from "../firebase";
import axios from "../api/inventory";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";
import { ref } from "vue";
import { signInWithEmailAndPassword } from "firebase/auth";
import { useUserStore } from "@/store/store";
export default {
  setup() {
    const toast = useToast();
    const router = useRouter();
    const email = ref("");
    const password = ref("");
    const userStore = useUserStore();

    const login = async () => {
      try {
        await signInWithEmailAndPassword(auth, email.value, password.value);

        const response = await axios.post("/auth/login", {
          email: email.value,
          password: password.value,
        });

        localStorage.setItem("jwt_token", response.data.access_token);
        localStorage.setItem("refresh_token", response.data.refresh_token);
        localStorage.setItem("username", response.data.username);

        toast.success("Login successful!");
        userStore.setUsername(response.data.username);
        router.push("/dashboard");
      } catch (error) {
        toast.error(
          error.response?.data?.message || "Login failed. Please try again."
        );
        console.error("Login failed:", error);
      }
    };

    // Google Sign-In function
    const googleSignIn = async () => {
      const provider = new GoogleAuthProvider();
      try {
        const result = await signInWithPopup(auth, provider);

        const user = result.user;

        const token = await user.getIdToken();

        const response = await axios.post("/auth/login", { token });

        localStorage.setItem("jwt_token", response.data.access_token);
        localStorage.setItem("refresh_token", response.data.refresh_token);
        localStorage.setItem("username", response.data.username);
        toast.success("Welcome back!");
        userStore.setUsername(response.data.username);
        router.push("/dashboard");
      } catch (error) {
        console.error("Google Sign-In Error:", error);

        if (error.response?.status === 401) {
          toast.error("Invalid Firebase token. Please try again.");
        } else {
          toast.error("Google Sign-In failed. Please try again.");
        }
      }
    };

    const goToRegister = () => {
      router.push("/register");
    };

    const goToForgotPassword = () => {
      router.push("/forgot-password");
    };

    return {
      email,
      password,
      login,
      googleSignIn,
      goToRegister,
      goToForgotPassword,
    };
  },
};
</script>
<style scoped>
body {
  overflow: hidden;
  margin: 0;
}

.full-screen-login {
  height: 100vh;
  width: 100vw;
  position: relative;
  background-image: url("../assets/background.png");
  background-size: cover;
  background-position: center;
  filter: none;
}
.login-container {
  background-color: rgba(255, 255, 255, 0.8);
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.login-container input {
  filter: none;
}

form {
  padding: 3rem;
  margin: 0 auto;
}

h2 {
  font-size: 2.5rem;
}

input {
  font-size: 1.2rem;
  padding: 1.2rem 1.8rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  transition: border-color 0.3s ease-in-out;
  margin-bottom: 1rem;
  margin-right: 1rem;
}

input:focus {
  outline: none;
  border-color: #337ab7;
}

button {
  font-size: 1.4rem;
  padding: 1.4rem 2.2rem;
  font-weight: bold;
  border-radius: 5px;
  transition: background-color 0.3s ease-in-out;
  margin-right: 1rem;
}

button:hover {
  background-color: #337ab7;
}

.text-blue-500 {
  font-size: 1.2rem;
  margin-top: 1rem;
}

.error-message {
  color: red;
  font-size: 1rem;
  margin-top: 0.5rem;
}
</style>
