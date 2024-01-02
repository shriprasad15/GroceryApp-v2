<template>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

  <h3 style="background-color: #FDF697;color: #B6261D">

  <img src="../../../static/mrbean_icon.png" alt="MrBean Grocery App" style="cursor: pointer;width: 75px; height: 75px; margin-right: 30px;" />
      Welcome {{ name }} to MrBean Groceries
    </h3>

    <!-- Rest of your HTML content goes here -->
    <nav class="navbar navbar-expand-lg bg-body-secondary">
  <div class="container-fluid">
    <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>

    <div class="collapse navbar-collapse" :class="{ 'show': isNavbarOpen }" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <!-- Home Link on the Left -->
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/user-dashboard/">
            <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-house-door" viewBox="0 0 16 16">
              <path d="M8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4.5a.5.5 0 0 0 .5-.5v-4h2v4a.5.5 0 0 0 .5.5H14a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146ZM2.5 14V7.707l5.5-5.5 5.5 5.5V14H10v-4a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5v4H2.5Z"/>
            </svg>Home
          </a>
        </li>

        <!-- Profile Link on the Left -->
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="profile">
            <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
  <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
  <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
</svg> Profile
          </a>
        </li>

        <!-- Logout Link on the Left -->
        <li class="nav-item">
          <button @click="logout" class="nav-link" >
            <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-box-arrow-right" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z"/>
  <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z"/>
</svg> Logout
          </button>
        </li>
      </ul>

      <!-- Search Form in the Middle -->


      <!-- Cart Button on the Right -->
      <ul class="navbar-nav ml-auto">
  <li class="nav-item">
    <!-- Cart with 0 items -->
    <template v-if="cart_value <= 0">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="50"
        height="50"
        fill="currentColor"
        class="bi bi-cart3"
        viewBox="0 0 16 16"
      >
        <!-- SVG path for cart when cart_value is 0 -->
        <path d="M0 1.5A.5.5 0 0 1 .5 1H2a.5.5 0 0 1 .485.379L2.89 3H14.5a.5.5 0 0 1 .49.598l-1 5a.5.5 0 0 1-.465.401l-9.397.472L4.415 11H13a.5.5 0 0 1 0 1H4a.5.5 0 0 1-.491-.408L2.01 3.607 1.61 2H.5a.5.5 0 0 1-.5-.5zM3.102 4l.84 4.479 9.144-.459L13.89 4H3.102zM5 12a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm7 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-7 1a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm7 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
      </svg>
      Cart (0)
    </template>

    <!-- Cart with items -->
    <template v-else>
      <router-link to="/user-dashboard/cart" class="nav-link" aria-current="page">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="50"
          height="50"
          fill="currentColor"
          class="bi bi-cart-check-fill"
          viewBox="0 0 16 16"
        >
          <!-- SVG path for cart when cart_value > 0 -->
          <path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.607 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1H.5zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm-1.646-7.646-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L8 8.293l2.646-2.647a.5.5 0 0 1 .708.708z"/>
        </svg>
        Cart ({{ cart_value }})
      </router-link>
    </template>
  </li>
</ul>
    </div>

  </div>
</nav>
<RouterView/>
</template>

<script>
import {fetchCategories} from "../../../api_helpers/helpers";

export default {

  props: {

    userid: String,
  },
  data() {
    return {
      name: JSON.parse(sessionStorage.getItem("fname"))+ " " + JSON.parse(sessionStorage.getItem("lname"))  ,
      isNavbarOpen: false,
      products: [],
      categories: [],
      cart_value: 0,
      product_quantity: {}
    };
  },

  beforeCreate() {
    console.log("sdfc",sessionStorage.getItem("token")?.length);
    if(!sessionStorage.getItem("token")  || (JSON.parse(sessionStorage.getItem("role"))?.[0] !== "user") ){
        sessionStorage.clear();
        this.$router.push('/user-login');
      }
    },
  created() {


    //this.fetchCategories();
  },
  mounted() {
    this.fetchProducts();
    this.fetch_cart_quantity();
    this.fetch_product_quantity();
    this.assign();
  },
  methods: {

    async fetch_product_quantity(prod_id){
      const response = await fetch('http://127.0.0.1:5003/api/cart',{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        },
      });
      const cart_data = await response.json();
      if (response.ok) {
        //filter the data to get the product id


        this.products.forEach(product => {
  const cartProduct = cart_data.find(item => item.product_id === product.id);

  if (cartProduct) {
    this.product_quantity[product.id] = cartProduct.quantity;
  } else {
    this.product_quantity[product.id] = 0;
  }
});

        console.log(this.product_quantity)
      }
      else {
        console.error('Failed to fetch cart');
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

    async addCart(product_id) {
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
        window.location.reload();
        await this.fetch_cart_quantity();

      }
      else {
        console.error('Failed to add product to cart');
      }
    },
      async fetchProducts() {
        try {
          const response = await fetch('http://127.0.0.1:5003/api/products');
          const data = await response.json();
          if (response.ok) {
            this.products = data;
          }
          else {
            console.error('Failed to fetch products');
          }
        } catch (error) {
          console.error('Error fetching products:', error);
        }
      },
    async logout() {
          sessionStorage.setItem("token", JSON.stringify(""));
          sessionStorage.clear()
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