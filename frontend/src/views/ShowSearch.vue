<template>
  <div class="flex min-h-screen relative">
    <Sidebar class="w-1/4 bg-gray-800 p-4 text-white" />

    <div class="flex-1 bg-gray-100 flex flex-col p-6">
      <!-- Header Section -->
      <div class="flex flex-col items-center justify-center w-full h-full">
        <h1 class="text-4xl font-bold text-gray-800 mb-4">
          Manage Your Inventory
        </h1>
        <p class="text-lg text-gray-600 mb-8">
          Use your voice or type to execute command to your inventory.
        </p>

        <div class="flex w-full mb-4 relative">
          <input
            type="text"
            v-model="searchQuery"
            @input="handleSearch"
            placeholder="Search by item name."
            class="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div class="absolute top-0 right-0 flex space-x-2 mt-4 mr-4">
            <button
              @click="clearSearch"
              v-if="searchQuery"
              class="p-2 bg-red-500 text-white rounded-lg shadow hover:bg-red-600 transition-transform transform hover:scale-110"
            >
              Clear
            </button>

            <button
              @click="startVoiceCommand"
              class="p-2 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 transition-transform transform hover:scale-110"
            >
              🎤
            </button>
          </div>
        </div>

        <!-- Suggestions Section -->
        <div class="mt-8 w-full">
          <p class="text-lg font-semibold text-gray-700 mb-2">
            Try saying or typing:
          </p>
          <div class="flex flex-wrap gap-4 mb-5">
            <button
              v-for="(suggestion, index) in suggestions"
              :key="index"
              class="px-4 py-2 bg-gray-200 text-gray-800 border border-gray-300 rounded-lg shadow hover:bg-gray-300 transition"
            >
              {{ suggestion }}
            </button>
          </div>
        </div>

        <!-- Inventory Table -->
        <div
          v-if="showTable"
          class="w-full relative overflow-x-auto bg-gray-100 p-4"
        >
          <!-- Close Button -->
          <button
            @click="hideTable"
            class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 text-xs"
          >
            ✖
          </button>

          <table
            class="table-auto w-full max-w-screen-lg mx-auto bg-white border border-gray-300 rounded-lg shadow-md"
          >
            <thead
              class="bg-gradient-to-r from-blue-500 to-blue-400 text-white"
            >
              <tr>
                <th
                  class="px-6 py-3 text-left text-sm font-semibold text-gray-100"
                >
                  ID
                </th>
                <th
                  class="px-6 py-3 text-left text-sm font-semibold text-gray-100"
                >
                  Name
                </th>
                <th
                  class="px-6 py-3 text-left text-sm font-semibold text-gray-100"
                >
                  Quantity
                </th>
                <th
                  class="px-6 py-3 text-left text-sm font-semibold text-gray-100"
                >
                  Unit
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="!filteredStock.length">
                <td
                  colspan="4"
                  class="px-6 py-4 text-center text-sm text-gray-500"
                >
                  No items found.
                </td>
              </tr>
              <tr
                v-for="item in filteredStock"
                :key="item.id"
                class="hover:bg-gray-50 transition-all duration-300 ease-in-out"
              >
                <td
                  class="px-6 py-4 text-sm text-gray-700 border-b border-gray-200"
                >
                  {{ item.id }}
                </td>
                <td
                  class="px-6 py-4 text-sm text-gray-700 border-b border-gray-200"
                >
                  {{ item.name }}
                </td>
                <td
                  class="px-6 py-4 text-sm text-gray-700 border-b border-gray-200"
                >
                  {{ item.quantity }}
                </td>
                <td
                  class="px-6 py-4 text-sm text-gray-700 border-b border-gray-200"
                >
                  {{ item.unit }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div
          v-if="isListening"
          class="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50"
        >
          <div class="text-center">
            <div
              class="w-72 h-72 rounded-full bg-white flex items-center justify-center mb-4 animate-pulse"
            >
              <img
                src="../assets/listening.gif"
                alt="Listening"
                class="w-64 h-64 rounded-full object-cover"
              />
            </div>
            <h2 class="text-white text-xl mb-2">{{ listeningMessage }}</h2>
            <button
              @click="stopListening"
              class="p-3 bg-red-500 text-white rounded-lg shadow hover:bg-red-600 transition-transform transform hover:scale-110 mt-4"
            >
              Stop Listening
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="mt-4 text-red-500 text-center">
          {{ errorMessage }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../api/inventory";
import Sidebar from "@/components/Sidebar.vue";

export default {
  name: "InventoryTable",
  components: { Sidebar },
  data() {
    return {
      stockList: [],
      searchQuery: "",
      errorMessage: "",
      showTable: false,
      isListening: false,
      listeningMessage: "Listening for your command...",
      suggestions: ["Show stock", "Search for apple"],
    };
  },
  computed: {
    filteredStock() {
      const query = this.searchQuery.toLowerCase();
      return this.stockList.filter(
        (item) =>
          item.name.toLowerCase().includes(query) ||
          String(item.id).includes(query) ||
          String(item.quantity).includes(query)
      );
    },
  },
  methods: {
    speak(message) {
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.lang = "en-US";
      speechSynthesis.speak(utterance);
    },
    async fetchStock() {
      try {
        const response = await axios.get("/inventory/show-stock");
        if (response.data.stock_list) {
          this.stockList = response.data.stock_list;
          this.errorMessage = ""; // Clear previous errors
        } else {
          this.errorMessage = "Unexpected response format.";
          this.stockList = [];
          this.speak(this.errorMessage);
        }
      } catch (error) {
        this.errorMessage =
          error.response?.data?.message ||
          "Failed to fetch stock. Please try again later.";
        this.speak(this.errorMessage);
      }
    },
    handleSearch() {
      if (!this.searchQuery.trim()) {
        this.clearSearch();
        this.speak("Search cleared.");
      } else {
        this.showTable = true;
        this.speak(`Searching for ${this.searchQuery}`);
      }
    },
    clearSearch() {
      this.searchQuery = "";
    },
    hideTable() {
      this.showTable = false; // Hide the table
    },
    async startVoiceCommand() {
      this.isListening = true;
      this.listeningMessage = "Preparing to listen...";
      this.speak("Preparing to listen...");

      await new Promise((resolve) => setTimeout(resolve, 3000));

      this.listeningMessage = "Listening for your command...";
      try {
        const response = await axios.post("/inventory/process-voice-command");

        if (this.isListening === false) return;
        if (response.data.stock_list) {
          this.stockList = response.data.stock_list;
          this.errorMessage = "";
          this.showTable = true;
          this.speak("Displaying inventory stock.");
        } else if (response.data.results) {
          this.stockList = response.data.results;
          this.errorMessage = "";
          this.showTable = true;
        } else if (response.data.message) {
          this.errorMessage = response.data.message;
          this.speak(this.errorMessage);
          this.stockList = [];
        } else {
          this.errorMessage = "Unexpected response format from the server.";
        }
      } catch (error) {
        this.errorMessage =
          error.response?.data?.message ||
          "Failed to process voice command. Please try again.";
        this.speak(this.errorMessage);
      } finally {
        this.isListening = false;
      }
    },
    async stopListening() {
      this.isListening = false;
      this.listeningMessage = "Stopped listening.";
      this.speak(this.listeningMessage);

      try {
        const response = await axios.post("/inventory/stop-listening");
        if (response.data && response.data.message) {
        } else {
          this.listeningMessage = "Failed to get confirmation from the server.";
          this.speak(this.listeningMessage);
        }
      } catch (error) {
        console.error(
          "Error stopping the backend recognition:",
          error.response?.data?.message || error.message
        );
      }
    },
  },
  created() {
    this.fetchStock();
  },
};
</script>

<style scoped>
html,
body,
#app {
  height: 100%;
  margin: 0;
}

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

.main-content {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  padding-left: 20rem;
}

.input-field {
  padding: 1rem;
}

table {
  width: 100%;
  border-collapse: collapse;
}

button {
  transition: background-color 0.3s ease-in-out;
}

button:hover {
  background-color: #065f46;
}

input,
select {
  padding: 1rem;
  margin-top: 0.5rem;
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
}

input:focus,
select:focus {
  outline: none;
  border-color: #047857;
}

/* Spinner animation */
.spinner-border {
  width: 3rem;
  height: 3rem;
  border-width: 0.25em;
}

/* Quick Stats Cards */
.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradientBG 3s ease infinite;
}

@keyframes gradientBG {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
/* Listening Overlay */
.fixed {
  z-index: 999;
}
</style>
