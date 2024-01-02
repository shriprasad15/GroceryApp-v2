<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="container mb-5">
     <div v-if="msg" class="alert alert-success" role="alert">{{ msg }}</div>
    <div v-if="error" class="alert alert-danger mt-3" role="alert">{{ error }}</div>
    <form @submit.prevent="addProductToCategory" class="mb-5">
    <h3>Create Product</h3>
      <div v-if = "dropdownItems.length <= 0" class="alert alert-danger">
        No categories available. Please send a request to admin for category creation
      </div>
      <div v-else>
        <h5>Select Category to add Product</h5>
        <select v-model="selectedCategory" class= "container mb-3" style="height: 40px; padding: 8px; border-radius: 4px; border: 1px solid #ccc;">
          <option v-for="item in dropdownItems" :key="item.id" :value="item.id">{{ item.name[0].oldName }}</option>
        </select>
        <b><p>Product Details</p></b>

        <div class="form-floating mb-3">
          <input type="text" aria-label="Category Name" v-model="productName" class="form-control">
          <label for="floatingInput">Product Name</label>
        </div>

        <div>
          <label for="m_date">Manufacture date:</label><br>
            <input type="date" id="m_date" v-model="manufactureDate" name="manufacture_date" required pattern="\d{4}-\d{2}-\d{2}">
        </div>

        <br>

        <div>
          <label for="e_date">Expiry date:</label><br>
          <input type="date" id="e_date" v-model="expiryDate" name="expiry_date" required pattern="\d{4}-\d{2}-\d{2}">
        </div><br>

        <div class="form-floating mb-3">
          <input type="number" class="form-control" v-model="ratePerUnit" name='rate_per_unit'>
          <label for="floatingInput">Rate per Unit</label>
        </div>

        <div class="form-floating mb-3">
          <input type="number" class="form-control" v-model="quantity" name='quantity'>
          <label for="floatingInput">Quantity</label>
        </div>

        <div class="pt-1 mb-4">
          <button class="btn btn-lg btn-block" type="submit" style="background-color: #6F4E37; color: white;">Submit</button>
        </div>
      </div>
    </form>


  </div>
</template>

<script>
import { fetchCategories } from "../../../api_helpers/helpers";

export default {
  data() {
    return {
      dropdownItems: [],
      selectedCategory: null,
      productName: '',
      manufactureDate: '',
      expiryDate: '',
      ratePerUnit: 0,
      quantity: 0,
      msg: '',
      error: '',
    };
  },
  methods: {
    async addProductToCategory() {
      try {
        if (!this.productName.trim()) {
          this.error = 'Product name cannot be empty';
          return;
        }

        if (!this.selectedCategory) {
          this.error = 'Please select a category';
          return;
        }
        console.log("sd", this.selectedCategory);
        const response = await fetch(`http://127.0.0.1:5003/api/product/cat/${this.selectedCategory}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))

          },
          body: JSON.stringify({
            prod_name: this.productName,
            mdate: this.manufactureDate,
            edate: this.expiryDate,
            rate: this.ratePerUnit,
            quantity: this.quantity,
          }),
        });

        if (response.ok) {
          this.msg = 'Product added to category successfully';
          // Reset form fields after successful addition if needed
          this.productName = '';
          this.manufactureDate = '';
          this.expiryDate = '';
          this.ratePerUnit = 0;
          this.quantity = 0;
          // Fetch and update categories again if necessary
          await this.assignCategories();
        } else {
          this.error = 'Failed to add product to category';
        }
      } catch (error) {
        console.error('Error adding product to category:', error);
        this.error = 'Error adding product to category';
      }
    },

    async assignCategories() {
      try {
        this.dropdownItems = await fetchCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
        this.error = 'Error fetching categories';
      }
    },
  },
  mounted() {
    this.assignCategories();
  },
};
</script>