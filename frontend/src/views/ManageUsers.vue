<template>
  <div class="flex h-full w-full">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-grow bg-gray-50 p-8 overflow-auto">
      <div class="w-full h-full bg-white shadow-xl rounded-lg">
        <!-- Header -->
        <div
          class="bg-blue-600 text-white px-6 py-4 flex items-center justify-between"
        >
          <h1 class="text-3xl font-bold flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-8 w-8 mr-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 14v6m-3-3h6M6 10h2a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v2a2 2 0 002 2zm10 0h2a2 2 0 002-2V6a2 2 0 00-2-2h-2a2 2 0 00-2 2v2a2 2 0 002 2zM6 20h2a2 2 0 002-2v-2a2 2 0 00-2-2H6a2 2 0 00-2 2v2a2 2 0 002 2z"
              />
            </svg>
            Manage Users
          </h1>
        </div>

        <!-- Content -->
        <div class="p-8 h-[calc(100%-72px)] overflow-auto">
          <!-- Users Table -->
          <table class="w-full table-auto border-collapse mb-8">
            <thead>
              <tr class="bg-gray-100">
                <th class="border px-4 py-2">Username</th>
                <th class="border px-4 py-2">Email</th>
                <th class="border px-4 py-2">Role</th>
                <th class="border px-4 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td class="border px-4 py-2">{{ user.username }}</td>
                <td class="border px-4 py-2">{{ user.email }}</td>
                <td class="border px-4 py-2">{{ user.role }}</td>
                <td class="border px-4 py-2">
                  <button
                    @click="selectUser(user)"
                    class="bg-blue-500 text-white px-3 py-1 rounded mr-2"
                  >
                    Edit
                  </button>
                  <button
                    v-if="selectedUser.id === user.id"
                    @click="deleteUser(user.id)"
                    class="bg-red-500 text-white px-3 py-1 rounded"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Edit User Form -->
          <div v-if="selectedUser.id" class="mt-8">
            <h2 class="text-lg font-bold mb-4">Edit User</h2>
            <form @submit.prevent="updateUser" class="space-y-4">
              <div>
                <label class="block text-gray-700 font-semibold mb-2"
                  >Username:</label
                >
                <input
                  v-model="selectedUser.username"
                  class="w-full border px-3 py-2 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label class="block text-gray-700 font-semibold mb-2"
                  >Role:</label
                >
                <select
                  v-model="selectedUser.role"
                  class="w-full border px-3 py-2 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="admin">Admin</option>
                  <option value="user">User</option>
                </select>
              </div>
              <button
                type="submit"
                class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition duration-300"
              >
                Save Changes
              </button>
              <button
                type="button"
                @click="deleteUser(selectedUser.id)"
                class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition duration-300 mt-2"
              >
                Delete User
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar.vue";
import axios from "../api/inventory";

export default {
  components: {
    Sidebar,
  },
  data() {
    return {
      users: [],
      selectedUser: {
        id: null,
        username: "",
        role: "",
      },
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get("/auth/users");
        this.users = response.data.users;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    async updateUser() {
      try {
        await axios.put(
          `/auth/users/${this.selectedUser.id}`,
          this.selectedUser
        );
        this.fetchUsers();
      } catch (error) {
        console.error("Error updating user:", error);
      }
    },
    async deleteUser(userId) {
      try {
        await axios.delete(`/auth/users/delete/${userId}`);
        this.fetchUsers();
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    },
    selectUser(user) {
      this.selectedUser = { ...user };
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
input:focus,
select:focus {
  @apply ring-2 ring-blue-500 border-transparent;
}
</style>
