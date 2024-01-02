<template>

    <div class="container mt-5">
      <div v-show="showSpinner" class="spinner-grow text-warning" style="width: 5em; height: 5rem; margin-left: 600px" role="status">
        <span class="sr-only"></span>
      </div>
  <div v-if="filteredCategories.length > 0">
    <form class="d-flex mx-auto" @submit.prevent="searchProducts" >
      <input v-model="searchQuery" class="form-control me-3 shadow-lg border-black" type="search" placeholder="Search" aria-label="Search">
<!--        <button class="btn btn-outline-success" type="submit">-->
<!--          <i class="bi bi-search"></i> Search-->
<!--        </button>-->
      </form>



    <div class= "container mb-5 pt-5" >
      <div class="card border-1 mb-4">
        <h1 class="mb-3 m-lg-2">Product List</h1>
      </div>
      <div class="card border-1 mb-4 p-lg-2">


   <div v-for="category in filteredCategories" :key="category.id">
     <center> <h3 v-if="filteredProductsByCategory(category.id).length > 0">Category: {{ category.name[0].oldName }}</h3></center>
      <div class="row">
        <div v-for="(product, index) in filteredProductsByCategory(category.id)" :key="product.id" class="col-md-4 mb-3">
         <div class="card">
<!--             <h4>{{category.name[0].oldName}}</h4>-->
            <div class="card-header" v-if="product_quantity[product.id] > 0">
              <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-cart-fill" viewBox="0 0 16 16" style="position: absolute; top: 5px; right: 50px;">
                <path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1H.5zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm-1.646-7.646-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L8 8.293l2.646-2.647a.5.5 0 0 1 .708.708z"/>
              </svg>
              <p>(Item in Cart: {{ product_quantity[product.id] }})</p>
            </div>
           <div class="card-body">
<!--        <p>{{product.id}}</p>-->
<!--        <p>(Item Cart: {{ product_quantity }})</p>-->
<!--        {{product_quantity}}-->
        <h3 class="card-title">{{ product.name }}</h3>
        <p class="card-text">Rate Per Unit: ₹{{ product.rate_per_unit }}</p>
        <p class="card-text">Quantity: {{ product.quantity ? product.quantity : 'Out of Stock' }}</p>
        <p class="card-text">Manufacture Date: {{ product.manufacture_date }}</p>
        <p class="card-text">Expiry Date: {{ product.expiry_date }}</p>
        <button class="btn btn-outline-success" v-if="product.quantity !== 0" @click="addCart(product.id)">Add to cart (1)</button>
      </div>
    </div>
  </div>
</div>


    </div>

  </div>
      <!-- Show a message if there are no products -->
</div>
    </div>
    </div>
</template>

<script>
import {fetchCategories} from "../../../api_helpers/helpers";
import cart from "@/views/User/Cart.vue";

export default {
  name: 'ProductList',
  props: {
    name: String,
    userid: String,
  },
  data() {
    return {
      searchQuery: '',
      isNavbarOpen: false,
      products: [],
      categories: [],
      category_with_products: [],
      cartProduct:[],
      cart_value: 0,
      product_quantity: {},
      showSpinner:false,
    };
  },

  created() {
    this.showSpinner = true;
    this.spin();
    this.fetchProducts();
    //this.fetchCategories();
  },

  computed: {
    filteredCategories() {
      return this.categories.filter(category =>
        this.products.some(product => product.category_id === category.id)
      );
    },

  },
  methods: {
    async spin() {
      await new Promise(resolve => setTimeout(resolve, 2000));
      await this.fetch_cart_quantity();
      await this.fetch_product_quantity();
      await this.assign();
      this.showSpinner = false;
    },
    async fetch_product_quantity() {
      try {
        const response = await fetch('http://127.0.0.1:5003/api/cart', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
        });
        const cartData = await response.json();
        if (response.ok) {
          console.log(cartData)
          console.log("prod",cartData[0])
          console.log("prod id", cartData[0].product_id)

          for (const product of this.products) {
            this.cartProduct = cartData.find(item => item.product_id === product.id);

            // Checking if cartProduct exists, then assign its quantity, else 0
            this.product_quantity[product.id] = this.cartProduct ? this.cartProduct.cart_quantity : 0;
          }
        } else {
          console.error('Failed to fetch cart');
        }
      } catch (error) {
        console.error('Error fetching cart:', error);
      }
    },
    async fetch_cart_quantity(){
      const response = await fetch('http://127.0.0.1:5003/api/cart',{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.cart_value = data.length;
        console.log(data.length)
      }
      else {
        console.error('Failed to fetch cart');
      }
    },
    filteredProductsByCategory(categoryId) {
      return this.products.filter(product =>
        (product.category_id === categoryId) &&
        (product.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
         this.getCategoryNameById(product.category_id).toLowerCase().includes(this.searchQuery.toLowerCase()))
      );
    },

    getCategoryNameById(categoryId) {
      const category = this.categories.find(category => category.id === categoryId);
      return category ? category.name[0].oldName : '';
    },
   //implement searchProducts from the products list and category list without api
    async searchProducts() {
      try {
        const response = await fetch(`http://127.0.0.1:5003/api/product/search/${this.searchQuery}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.products = data;
        } else {
          console.error('Failed to fetch products');
        }
      }
      catch (error) {
        console.error('Error fetching products:', error);
      }
    },


    async addCart(product_id) {
      try {
      const response = await fetch(`http://127.0.0.1:5003/api/cart`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        },
        body: JSON.stringify({
          "product_id": product_id,
        }),
      });
        if (response.ok) {
          alert('Product added to cart');
          await this.fetch_cart_quantity();
          window.location.reload()
        }
        else {
          console.error('Failed to add product to cart');
        }
      }
      catch (error) {
        alert('Item quantity exceeded');
      }

    },
      async fetchProducts() {
        try {
          const response = await fetch('http://127.0.0.1:5003/api/products');
          const data = await response.json();
          if (response.ok) {
            this.products = data;
            const prices = this.products.map(product => product.rate_per_unit);
            this.minPrice = Math.min(...prices, 0);
            this.maxPrice = Math.max(...prices, 1000);
          }
          else {
            console.error('Failed to fetch products');
          }
        } catch (error) {
          console.error('Error fetching products:', error);
        }
      },

    async fetchCategoryProducts(category_id) {
      try {
        const response = await fetch(`http://127.0.0.1:5003/api/product/cat/${category_id}`);

        const data = await response.json();
        if (response.ok) {
          this.category_with_products = data;

        } else {
          console.error('Failed to fetch products');
        }
      }
      catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    async logout() {
          sessionStorage.removeItem("token");
          const response = await fetch('http://127.0.0.1:5003/signout');
          if(response.ok){
            this.$router.push('/user-login');
            alert('Logout successful');
          }
          else{
            console.log(response)
            alert('Logout failed');
          }
          // console.log(sessionStorage.getItem("token"));

        },
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    async assign(){
      this.categories = await fetchCategories();
    }

  },
};
</script>
