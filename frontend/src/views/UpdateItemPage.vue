<template>
  <div>
    <h1>Update Item Quantity</h1>
    <form @submit.prevent="updateItem">
      <input
        v-model="quantity"
        type="number"
        placeholder="New Quantity"
        required
      />
      <button type="submit">Update Item</button>
    </form>
  </div>
</template>

<script>
import axios from "../api/inventory";
import { useToast } from "vue-toastification";

export default {
  props: ["itemId"],
  data() {
    return {
      quantity: "",
    };
  },
  methods: {
    async updateItem() {
      const toast = useToast();
      try {
        await axios.put(`/inventory/update/${this.itemId}`, {
          quantity: this.quantity,
        });
        toast.success(`Item updated successfully`);
        this.quantity = "";
      } catch (error) {
        toast.error("Failed to update item");
      }
    },
  },
};
</script>
