<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <Sidebar class="w-64 bg-black shadow-lg" />

    <!-- Main Content -->
    <div class="flex-1 p-6 bg-gray-50 overflow-y-auto">
      <div class="container mx-auto">
        <h1 class="text-3xl font-extrabold text-gray-800 mb-6">Profile</h1>
        <p class="text-lg text-gray-600 mb-6">Manage your profile settings.</p>

        <!-- Change Username Section -->
        <section id="change-username" class="mb-6">
          <h2 class="text-xl font-semibold text-gray-700">Change Username</h2>
          <form
            class="bg-white p-4 rounded-lg shadow-md mt-4"
            @submit.prevent="handleChangeUsername"
          >
            <label for="username" class="block text-gray-700"
              >New Username</label
            >
            <input
              type="text"
              id="username"
              v-model="username"
              class="w-full p-2 border border-gray-300 rounded-md"
              placeholder="Enter your new username"
            />
            <button
              type="submit"
              class="mt-4 w-full p-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Save Username
            </button>
            <p v-if="usernameMessage" class="text-green-600 mt-2">
              {{ usernameMessage }}
            </p>
            <p v-if="usernameError" class="text-red-600 mt-2">
              {{ usernameError }}
            </p>
          </form>
        </section>

        <!-- Change Password Section -->
        <section id="change-password" class="mb-6">
          <h2 class="text-xl font-semibold text-gray-700">Change Password</h2>
          <form
            class="bg-white p-4 rounded-lg shadow-md mt-4"
            @submit.prevent="handleChangePassword"
          >
            <label for="current-password" class="block text-gray-700"
              >Current Password</label
            >
            <input
              type="password"
              id="current-password"
              v-model="currentPassword"
              class="w-full p-2 border border-gray-300 rounded-md"
              placeholder="Enter your current password"
            />
            <label for="new-password" class="block text-gray-700 mt-4"
              >New Password</label
            >
            <input
              type="password"
              id="new-password"
              v-model="newPassword"
              class="w-full p-2 border border-gray-300 rounded-md"
              placeholder="Enter your new password"
            />
            <label for="confirm-password" class="block text-gray-700 mt-4"
              >Confirm New Password</label
            >
            <input
              type="password"
              id="confirm-password"
              v-model="confirmPassword"
              class="w-full p-2 border border-gray-300 rounded-md"
              placeholder="Confirm your new password"
            />
            <button
              type="submit"
              class="mt-4 w-full p-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Change Password
            </button>

            <!-- Display Error or Success Messages -->
            <p v-if="errorMessage" class="text-red-600 mt-2">
              {{ errorMessage }}
            </p>
            <p v-if="successMessage" class="text-green-600 mt-2">
              {{ successMessage }}
            </p>
          </form>
        </section>

        <!-- Email Notifications Section -->
        <section id="email-notifications" class="mb-6">
          <h2 class="text-xl font-semibold text-gray-700">
            Email Notifications
          </h2>
          <form class="bg-white p-4 rounded-lg shadow-md mt-4">
            <label for="email-notifications" class="block text-gray-700"
              >Enable Email Notifications</label
            >
            <input type="checkbox" id="email-notifications" class="mt-2" />
            <p class="text-gray-600 mt-2">
              Receive email notifications for updates and promotions.
            </p>
            <button
              type="submit"
              class="mt-4 w-full p-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Save Settings
            </button>
          </form>
        </section>

        <!-- Account Settings Section -->
        <section id="account-settings" class="mb-6">
          <h2 class="text-xl font-semibold text-gray-700">Account Settings</h2>
          <form class="bg-white p-4 rounded-lg shadow-md mt-4">
            <label for="timezone" class="block text-gray-700">Timezone</label>
            <select
              id="timezone"
              class="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="GMT">GMT</option>
              <option value="PST">PST</option>
            </select>
            <button
              type="submit"
              class="mt-4 w-full p-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Save Account Settings
            </button>
          </form>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar.vue";
import axios from "@/api/inventory";

export default {
  name: "Profile",
  components: {
    Sidebar,
  },
  data() {
    return {
      username: "",
      usernameMessage: "",
      usernameError: "",
      currentPassword: "",
      newPassword: "",
      confirmPassword: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async handleChangeUsername() {
      if (!this.username.trim()) {
        this.usernameError = "New username cannot be empty.";
        return;
      }
      try {
        const response = await axios.post("/auth/update-username", {
          new_username: this.username,
        });
        this.usernameMessage =
          response.data.message || "Username updated successfully.";
        this.usernameError = "";
        this.username = "";
      } catch (error) {
        this.usernameMessage = "";
        this.usernameError =
          error.response?.data?.message || "Failed to update username.";
      }
    },
    async handleChangePassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.errorMessage = "New password and confirm password do not match.";
        return;
      }

      try {
        const response = await axios.post("/auth/change-password", {
          current_password: this.currentPassword,
          new_password: this.newPassword,
        });
        this.successMessage = response.data.message;
        this.errorMessage = "";
        this.currentPassword = "";
        this.newPassword = "";
        this.confirmPassword = "";
      } catch (error) {
        this.successMessage = "";
        this.errorMessage =
          error.response?.data?.message || "Failed to change password.";
      }
    },
  },
};
</script>

<style scoped>
/* Sidebar Styles */
.sidebar {
  background-color: #047857;
  color: white;
  width: 20rem;
  padding: 1rem;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
}
</style>
