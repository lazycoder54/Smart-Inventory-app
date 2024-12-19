<template>
  <div class="container">
    <h1 class="title">Customers</h1>
    <p class="description">View and manage customer information.</p>

    <input
      v-model="searchQuery"
      @input="filterCustomers"
      class="search-input"
      type="text"
      placeholder="Search customers..."
    />

    <button
      @click="showAddCustomerForm = !showAddCustomerForm"
      class="add-button"
    >
      {{ showAddCustomerForm ? "Cancel" : "Add Customer" }}
    </button>

    <div v-if="showAddCustomerForm" class="form-container">
      <input v-model="newCustomer.name" type="text" placeholder="Name" />
      <input v-model="newCustomer.email" type="email" placeholder="Email" />
      <button @click="addCustomer">Add Customer</button>
    </div>

    <!-- Customer List -->
    <ul v-if="filteredCustomers.length" class="customer-list">
      <li
        v-for="(customer, index) in filteredCustomers"
        :key="index"
        class="customer-item"
      >
        <div>
          <strong>{{ customer.name }}</strong> - {{ customer.email }}
        </div>
        <button @click="deleteCustomer(index)" class="delete-button">
          Delete
        </button>
      </li>
    </ul>
    <p v-else>No customers found.</p>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
  name: "Customers",
  data() {
    return {
      customers: [
        { name: "John Doe", email: "john@example.com" },
        { name: "Jane Smith", email: "jane@example.com" },
      ],
      searchQuery: "",
      filteredCustomers: [],
      newCustomer: { name: "", email: "" },
      showAddCustomerForm: false,
    };
  },
  mounted() {
    this.filteredCustomers = this.customers;
  },
  methods: {
    filterCustomers() {
      this.filteredCustomers = this.customers.filter((customer) =>
        customer.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    addCustomer() {
      const toast = useToast();

      if (this.newCustomer.name && this.newCustomer.email) {
        this.customers.push({ ...this.newCustomer });
        this.newCustomer.name = "";
        this.newCustomer.email = "";
        this.showAddCustomerForm = false;
        this.filterCustomers();
      } else {
        toast.error("Please enter valid name and email");
      }
    },
    deleteCustomer(index) {
      this.customers.splice(index, 1);
      this.filterCustomers();
    },
  },
};
</script>

<style scoped>
/* Full-screen layout */
.container {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: 1rem;
  background-color: #eef2ff;
  box-sizing: border-box;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #3730a3;
  margin-bottom: 1rem;
}

.description {
  font-size: 1rem;
  color: #4f46e5;
  margin-bottom: 2rem;
}

.search-input {
  width: 100%;
  max-width: 400px;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #c7d2fe;
  border-radius: 0.25rem;
}

.add-button {
  background-color: #4f46e5;
  color: #fff;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  margin-bottom: 1rem;
}

.add-button:hover {
  background-color: #3730a3;
}

.form-container {
  width: 100%;
  max-width: 400px;
  margin-bottom: 1rem;
}

.form-container input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  border: 1px solid #c7d2fe;
  border-radius: 0.25rem;
}

.customer-list {
  width: 100%;
  max-width: 600px;
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.customer-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background-color: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
}

.delete-button {
  background-color: #ef4444;
  color: #fff;
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #b91c1c;
}

@media (max-width: 600px) {
  .title {
    font-size: 1.5rem;
  }
  .description {
    font-size: 0.875rem;
  }
  .search-input {
    max-width: 100%;
  }
  .customer-item {
    flex-direction: column;
    align-items: flex-start;
  }
  .delete-button {
    align-self: flex-end;
    margin-top: 0.5rem;
  }
}
</style>
