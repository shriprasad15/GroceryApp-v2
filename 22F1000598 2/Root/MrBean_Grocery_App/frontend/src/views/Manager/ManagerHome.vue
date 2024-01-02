<template>
  <div v-if="msg" class="alert alert-success" role="alert">
      {{ msg }}
    </div>
    <!-- Display error message if available -->
    <div v-if="error" class="alert alert-danger mb-3" role="alert">
      {{ error }}
    </div>
<div>
  <div v-show="showSpinner" class="spinner-grow text-warning" style="width: 5em; height: 5rem; margin-left: 650px" role="status">
    <span class="sr-only"></span>
  </div>

  <div class="container mt-5">

    <div class="card border-1 mb-4">
      <h1 class="mb-3 m-lg-2">Category List</h1>
    </div>
    <div class="row-cols-2">
    <div class="card shadow-lg">

      <div v-if="category_items.length === 0" class="alert alert-info" role="alert">
        No categories available
      </div>
      <div v-else>
      <ul class="list-group">
        <li v-for="category in category_items" :key="category.id" class="list-group-item">{{ category.name[0].oldName }}</li>
      </ul>
        </div>
    </div>
    </div>
  </div>
    <div class="container mt-5" >
      <div class="card border-1 mb-4">
        <h1 class="mb-3 m-lg-2">Product List</h1>
      </div>
      <div class="card shadow-lg p-lg-2">
      <div v-if="product_items.length === 0" class="alert alert-info" role="alert">
        No products available
      </div>
      <div v-else>
      <div class="row">
        <div v-for="product in product_items" :key="product.id" class="col-md-4">
          <div class="card mb-4 ">
            <div class="card-body">
              <h5 class="card-title">{{ product.name }}</h5>
              <p class="card-text">
                Category:
                <span v-for="category in category_items" :key="category.id">
                  <span v-if="category.id === product.category_id">{{ category.name[0].oldName }}</span>
                </span>
              </p>
              <p class="card-text">Rate Per Unit: ₹{{ product.rate_per_unit }}</p>
              <p class="card-text">Quantity: {{ product.quantity }}</p>
              <p class="card-text">Manufacture Date: {{ product.manufacture_date }}</p>
              <p class="card-text">Expiry Date: {{ product.expiry_date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>
    </div>

</div>
</template>
<script>
import {fetchCategories, fetchPendingCategories, fetchProducts} from "../../../api_helpers/helpers";
export default {
  props: {
    msg: String,
    error: String,
  },
  data() {
    return {
      isNavbarOpen: false,
      isCategoryDropdownOpen: false,
      isProductDropdownOpen: false,
      productItems: ['Create-Product', 'Delete-Product', 'Edit-Product'],
      categoryItems: ['Create-Category', 'Delete-Category', 'Edit-Category'],
      category_items: [],
      product_items: [],
      showSpinner:false,
    };
  },
  created(){
    this.showSpinner=true;
    this.spin();
  },
  // mounted() {
  //   this.assign();
  // },
  methods: {
    async spin() {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await this.assign();
      this.showSpinner = false;
    },
    async assign() {
      this.category_items = await fetchCategories();
      this.product_items= await fetchProducts();
    },

  },
};
</script>
