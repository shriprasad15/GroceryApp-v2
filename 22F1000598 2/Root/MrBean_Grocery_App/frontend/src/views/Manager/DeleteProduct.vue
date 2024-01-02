<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
    <h2 class="container mb-5">Delete Product</h2>
    <br>
  <div v-if="msg" class="alert alert-success" role="alert">
      {{ msg }}
    </div>
    <div v-if="error" class="alert alert-danger mt-3" role="alert">
      {{ error }}
    </div>
    <div class="container mb-3">
      <div v-if="category_items.length <= 0" class="alert alert-danger">
        No categories available. Please create one
      </div>
      <div v-else class="container mb-3">
      <h4><label for="categorySelect">Select Category to delete Product from</label><br><br></h4>
      <select id="categorySelect" v-model="selectedCategory" @change="fetchProductsByCategory(selectedCategory?selectedCategory:-1)">
        <option value="">Select Category</option>
        <option v-for="item in category_items" :key="item.id" :value="item.id">{{ item.name[0].oldName }}</option>
      </select>

    <br>
    <div v-if="product_items.length <= 0 && selectedCategory" class="alert alert-danger mt-4">
      No products available for this category
    </div>
    <div v-else>
        <br>
        <h4><label for="productSelect">Select Product to delete</label><br><br></h4>
        <select id="productSelect" v-model="selectedProduct">
          <option value="">Select Product</option>
          <option v-for="product in product_items" :key="product.id" :value="product.id">{{ product.name }}</option>
        </select>
      <br><br>
      <div>
        <button @click="showConfirmation" class="btn btn-danger">Delete</button>
      </div>
      </div>

      <div v-if="confirmationBox" class="alert alert-danger mt-3" role="alert">
        Are you sure you want to delete "{{ selectedProductName }}"?
        <button @click="confirmDelete" class="btn btn-danger btn-sm ms-2">Confirm</button>
        <button @click="cancelDelete" class="btn btn-secondary btn-sm ms-2">Cancel</button>
      </div>
    </div>
</div>
</template>

<script>
import { fetchCategories, fetchProductsByCategory, deleteProductById } from "../../../api_helpers/helpers";

export default {
  data() {
    return {
      category_items: [],
      product_items: [],
      selectedCategory: null,
      selectedProduct: null,
      selectedProductName: '',
      confirmationBox: false,
      msg: '',
      error: '',
    };
  },
  async created() {
    await this.assignCategories();
  },
  methods: {
    async assignCategories() {
      try {
        this.category_items = await fetchCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
        this.error = 'Error fetching categories';
      }
    },
    async fetchProductsByCategory(categoryId) {
      try {
        if (categoryId !== -1){
          this.product_items = await fetchProductsByCategory(categoryId);
        }

      } catch (error) {
        console.error('Error fetching products:', error);
        this.error = 'Error fetching products';
      }
    },
    async showConfirmation() {
      if (!this.selectedProduct) {
        alert('Please select a product');
        return;
      }

      const selectedProduct = this.product_items.find(product => product.id === this.selectedProduct);
      if (selectedProduct) {
        this.selectedProductName = selectedProduct.name;
        this.confirmationBox = true;
      }
    },
    async confirmDelete() {
      try {
        const response = await deleteProductById(this.selectedProduct);
        if (response.ok) {
          this.msg = `Product '${this.selectedProductName}' deleted successfully`;
          await this.fetchProductsByCategory(this.selectedCategory); // Refresh products after deletion
          window.location.reload();
        } else {
          this.error = 'Failed to delete product';
        }
        this.confirmationBox = false;
      } catch (error) {
        console.error('Error deleting product:', error);
        this.error = 'Error deleting product';
      }
    },
    cancelDelete() {
      this.confirmationBox = false;
    },
  },
};
</script>