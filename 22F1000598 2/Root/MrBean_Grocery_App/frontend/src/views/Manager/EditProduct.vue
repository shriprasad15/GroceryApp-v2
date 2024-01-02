<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="container mb-5"  >
    <div v-if="msg" class="alert alert-success" role="alert">{{ msg }}</div>
    <div v-if="error" class="alert alert-danger mt-3" role="alert">{{ error }}</div>
    <form @submit.prevent="submitProduct" class="pt-4">
      <h3>Edit Product</h3>
      <div v-if = "product_items.length <= 0" class="alert alert-danger">
        No products available. Please create one
      </div>
      <div v-else>
        <h5>Select Product to edit</h5>
        <select v-model="selectedProductId" style="height: 40px; width: 200px">
          <option v-for="item in product_items" :key="item.id" :value="item.id">{{ item.name }}</option>
        </select>

        <div class="form-floating mb-3">
          <br />
          <input type="text" aria-label="Category Name" v-model="newProductName" class="form-control" />
          <label for="floatingInput">Product New Name</label>
        </div>

        <div>
          <label for="m_date">Manufacture date:</label><br />
          <input type="date" id="m_date" v-model="manufactureDate" />
        </div>
        <br />

        <div>
          <label for="e_date">Expiry date:</label><br />
          <input type="date" id="e_date" v-model="expiryDate" />
        </div>
        <br />

        <div class="form-floating mb-3">
          <input type="number" class="form-control" v-model="ratePerUnit" />
          <label for="floatingInput">Rate per Unit</label>
        </div>

        <div class="form-floating mb-3">
          <input type="number" class="form-control" v-model="quantity" />
          <label for="floatingInput">Quantity</label>
        </div>

        <div>
          <h5>Change Category</h5>
          <p>Current Category: {{ getCategoryName(selectedProductId) }}</p>
          <select v-model="newCategoryId" style="height: 40px;">
            <option value="">-- Select New Category --</option>
            <option v-for="item in category_items" :key="item.id" :value="item.id">{{ item.name[0].oldName }}</option>
          </select>
        </div>

        <div class="pt-1 mb-4">
          <button class="btn btn-lg btn-block" type="submit" style="background-color: #6F4E37; color: white;">Submit</button>
        </div>
      </div>
    </form>


  </div>
</template>

<script>
import { fetchCategories,fetchProducts, updateProduct } from '../../../api_helpers/helpers'; // Replace './api' with your actual API module path

export default {
  data() {
    return {
      selectedProductId: null,
      product_items: [],
      category_items: [],
      newProductName: '',
      manufactureDate: '',
      expiryDate: '',
      ratePerUnit: null,
      quantity: null,
      newCategoryId: '',
      msg: '',
      error: '',
    };
  },
  methods: {
    getCategoryName(productId) {
      const selectedProductId = this.product_items.find(item => item.id === productId);
      if (selectedProductId) {
        const categoryId = selectedProductId.categoryId;
        const category = this.category_items.find(cat => cat.id === categoryId);
        return category ? category.name[0].oldName : '';
      }
      return '';
    },

    populateProductDetails() {

    },


    async assignProducts() {
      try {
        this.product_items = await fetchProducts();
      } catch (error) {
        console.error('Error fetching products:', error);
        this.error = 'Error fetching products';
      }
    },
    async assignCategories() {
      try {
        this.category_items = await fetchCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
        this.error = 'Error fetching categories';
      }
    },

    async submitProduct() {
      try {
        const productData = {
          prod_name: this.newProductName,
          mdate: this.manufactureDate,
          edate: this.expiryDate,
          rate: this.ratePerUnit,
          quantity: this.quantity,
          cat_id: this.newCategoryId,
        };

        const response = await updateProduct(this.selectedProductId, productData); // Replace 'updateProduct' with your API call function
        if (response.ok) {
          this.msg = `Product updated successfully`;
          this.resetForm();
        } else {
          this.error = 'Failed to update product';
        }
      } catch (error) {
        console.error('Error updating product:', error);
        this.error = 'Error updating product';
      }
    },
    resetForm() {
      this.selectedProductId = null;
      this.newProductName = '';
      this.manufactureDate = '';
      this.expiryDate = '';
      this.ratePerUnit = null;
      this.quantity = null;
      this.newCategoryId = '';
    },
  },
 mounted() {
    this.assignProducts();
    this.assignCategories();
    this.populateProductDetails();
  },
  watch:{
    selectedProductId(){
      console.log(this.selectedProductId);
      try {
        const selectedProduct = this.product_items.find(item => item.id === this.selectedProductId);
        if (selectedProduct) {
          this.newProductName = selectedProduct.name;
          this.manufactureDate = selectedProduct.manufacture_date;
          this.expiryDate = selectedProduct.expiry_date;
          this.ratePerUnit = selectedProduct.rate_per_unit;
          this.quantity = selectedProduct.quantity;
          this.newCategoryId = selectedProduct.category_id;
        }
      } catch (error) {
        console.error('Error populating product details:', error);
        this.error = 'Error populating product details';
      }

    }
  }
};
</script>
