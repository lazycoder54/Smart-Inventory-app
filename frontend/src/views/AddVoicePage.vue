<template>
  <div class="flex min-h-screen relative">
    <Sidebar class="w-1/4 bg-gray-800 p-4" />
    <div class="flex-1 bg-gray-100 flex flex-col p-6">
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
            v-model="command"
            placeholder="e.g., Add 100kg of apples"
            class="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            @click="startVoiceInput"
            class="ml-3 p-3 bg-blue-500 text-white rounded-lg shadow hover:bg-blue-600 transition-transform transform hover:scale-110"
          >
            🎤
          </button>
        </div>

        <button
          @click="submitCommand"
          class="mt-4 p-3 bg-green-500 text-white rounded-lg shadow hover:bg-green-600 transition-transform transform hover:scale-110 w-full sm:w-1/3"
        >
          Execute Command
        </button>

        <div
          v-if="confirmationMessage"
          class="mt-4 p-3 bg-gray-200 text-gray-800 border border-gray-300 rounded-lg shadow"
        >
          <p class="text-center">{{ confirmationMessage }}</p>
        </div>

        <div class="mt-8 w-full">
          <p class="text-lg font-semibold text-gray-700 mb-2">
            Try saying or typing:
          </p>
          <div class="flex flex-wrap gap-4">
            <button
              v-for="(suggestion, index) in suggestions"
              :key="index"
              @click="useSuggestion(suggestion)"
              class="px-4 py-2 bg-gray-200 text-gray-800 border border-gray-300 rounded-lg shadow hover:bg-gray-300 transition"
            >
              {{ suggestion }}
            </button>
          </div>
        </div>
      </div>

      <div
        v-if="showInventoryTable"
        class="relative mt-8 bg-white shadow-lg rounded-lg p-4"
      >
        <button
          @click="hideInventoryTable"
          class="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full shadow hover:bg-red-600 transition"
        >
          ✖
        </button>
        <InventoryTable :items="stockList" :showActions="false" />
      </div>

      <!-- Listening Overlay -->
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
            class="p-3 bg-red-500 text-white rounded-lg shadow hover:bg-red-600 transition-transform transform hover:scale-110"
          >
            Stop
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/Sidebar.vue";
import InventoryTable from "@/components/InventoryTable.vue";
import axios from "../api/inventory";

export default {
  components: {
    Sidebar,
    InventoryTable,
  },
  data() {
    return {
      command: "",
      stockList: [],
      showInventoryTable: false,
      isListening: false,
      confirmationMessage: "",
      suggestions: [
        "Add 10 kg of apples",
        "Remove 5 kg of apples",
        "Update 20kg stock of sugar",
        "Show stock",
      ],
      listeningMessage: "",
    };
  },
  methods: {
    async startVoiceInput() {
      this.isListening = true;
      this.listeningMessage = "Preparing to listen...";

      await new Promise((resolve) => setTimeout(resolve, 2000));

      this.listeningMessage = "Listening for your command...";
      try {
        const response = await axios.post("/inventory/add-voice");

        if (response.data && response.data.message) {
          this.command = response.data.message;
          this.confirmationMessage = `You said: "${this.command}"`;
          this.speak(this.confirmationMessage);

          this.isListening = false;

          if (this.command.toLowerCase().includes("show stock")) {
            const stockResponse = await axios.get("/inventory/show-stock");
            if (stockResponse.data && stockResponse.data.stock_list) {
              this.stockList = stockResponse.data.stock_list;
              this.showInventoryTable = true;
              this.confirmationMessage =
                "Inventory stock retrieved successfully!";
              this.speak(this.confirmationMessage);
            } else {
              this.confirmationMessage =
                stockResponse.data.message || "No items in inventory.";
              this.speak(this.confirmationMessage);
            }
          }
        } else {
          throw new Error("Failed to process voice command. Please try again.");
        }
      } catch (error) {
        let errorDetails;
        if (error.response?.data?.error) {
          errorDetails = error.response.data.error;
        } else if (error.message) {
          errorDetails = error.message;
        } else {
          errorDetails = "An unexpected error occurred.";
        }
        if (this.isListening === false) {
          errorDetails = "You stopped listening.";
        }
        this.confirmationMessage = `Error: ${errorDetails}`;
        this.speak(this.confirmationMessage);
        this.isListening = false;
      }
    },

    async submitCommand() {
      if (!this.command) {
        const errorMessage = "Please enter a command!";
        this.speak(errorMessage);
        
        return;
      }
      if (this.command.toLowerCase().includes("show stock")) {
        await this.fetchStock();
        return;
      }
      try {
        const response = await axios.post("inventory/process-command", {
          command: this.command,
        });
        this.confirmationMessage = `You wrote: ${this.command}`;
        this.speak(this.confirmationMessage);
      } catch (error) {
        const errorDetails =
          error.response?.data?.error ||
          error.message ||
          "Unexpected error occurred.";
        this.confirmationMessage = `Error: ${errorDetails}`;
        this.speak(this.confirmationMessage);
      }
    },
    async fetchStock() {
      try {
        const response = await axios.get("/inventory/list");
        if (response.status === 200 && response.data.items) {
          this.stockList = response.data.items;
          this.showInventoryTable = true;
          this.confirmationMessage = "Inventory stock retrieved successfully!";
          this.speak(this.confirmationMessage);
        } else {
          this.stockList = [];
          this.confirmationMessage =
            response.data.message || "No items in inventory.";
          this.speak(this.confirmationMessage);
        }
      } catch (error) {
        const errorDetails =
          error.response?.data?.error || "Failed to fetch inventory stock.";
        this.confirmationMessage = `Error: ${errorDetails}`;
        this.speak(this.confirmationMessage);
      }
    },

    stopListening() {
      this.isListening = false;
      this.listeningMessage = "Stopped listening.";
      this.speak("Listening stopped");

      axios
        .post(
          "/inventory/stop-listening",
          { timeout: 1000 },
          {},
          { headers: { "Content-Type": "application/json" } }
        )
        .then((response) => {
          console.log(response.data.message);
        })
        .catch(() => {
          console.error(
            "Error stopping the backend recognition:",
            error.response || error.message
          );
        });
    },
    hideInventoryTable() {
      this.showInventoryTable = false;
    },
    useSuggestion(suggestion) {
      this.command = suggestion;
    },

    speak(message) {
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.lang = "en-US";
      speechSynthesis.speak(utterance);
    },
  },
};
</script>

<style scoped>
body {
  font-family: "Inter", sans-serif;
}
.relative {
  position: relative;
}
.absolute {
  position: absolute;
}
</style>
