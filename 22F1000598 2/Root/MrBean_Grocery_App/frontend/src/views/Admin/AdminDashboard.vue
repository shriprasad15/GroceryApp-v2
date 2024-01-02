<template>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

    <h2 style="background-color: #FDF697;color: #B6261D">
      <img src="../../../static/mrbean_icon.png" alt="MrBean Grocery App" style="width: 75px; height: 75px; margin-right: 15px;" />
      Admin Dashboard
    </h2>
    <nav class="navbar navbar-expand-lg bg-body-secondary ">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ 'show': isNavbarOpen }" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/admin-dashboard" class="nav-link" aria-current="page">Home</router-link>
            </li>

            <li class="nav-item dropdown" @mouseover="openCategoryDropdown" @mouseleave="closeCategoryDropdown">
              <a class="nav-link dropdown-toggle" role="button" @click.prevent>
                Category Operations
              </a>
              <ul class="dropdown-menu" :class="{ 'show': isCategoryDropdownOpen }">
                <li v-for="item in categoryItems" :key="item">
                  <router-link :to="`/admin-dashboard/${item}`" class="dropdown-item">{{ item }}</router-link>
                </li>
              </ul>
            </li>

            <li class="nav-item">
              <router-link to="/admin-dashboard/Approve-Requests" class="nav-link" aria-current="page">Manager Control</router-link>
            </li>

<!--            <li class="nav-item">-->
<!--              <router-link to="#" class="nav-link" aria-current="page">Summary</router-link>-->
<!--            </li>-->
            <li class="nav-item">

          <button @click="logout" class="nav-link" >Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  <RouterView/>

</template>

<script>
import {fetchCategories, fetchProducts} from "../../../api_helpers/helpers";

export default {

  name: 'ProductList',
  props: {
    msg: String,
    error: String,

  },


  data() {
    return {
      isNavbarOpen: false,
      isCategoryDropdownOpen: false,
      isProductDropdownOpen: false,
      categoryItems: ['Create-Category', 'Delete-Category', 'Edit-Category'],
      category_items: [],
      product_items: [],
    };
  },

  beforeCreate() {
    console.log("sdfc",sessionStorage.getItem("token")?.length);
    if(!sessionStorage.getItem("token")  || (JSON.parse(sessionStorage.getItem("role"))?.[0] !== "admin") ){
        sessionStorage.clear();
        this.$router.push('/admin-login');
      }
    },

  mounted() {
      this.assign();
  },

  methods: {
    async  logout() {

      console.log(sessionStorage.getItem("token"));
      sessionStorage.setItem("token", JSON.stringify(""));
      console.log(sessionStorage.getItem("token"));
      sessionStorage.clear()
          const response = await fetch('http://127.0.0.1:5003/signout');
          if(response.ok){
            this.$router.push('/admin-login');
            alert('Logout successful');
          }
          else{
            console.log(response)
            alert('Logout failed');
          }
          // console.log(sessionStorage.getItem("token"));

        },
    async assign() {
      this.category_items = await fetchCategories();
      this.product_items= await fetchProducts()
    },


    openCategoryDropdown() {
      this.isProductDropdownOpen = true;
    },
    closeCategoryDropdown() {
      this.isProductDropdownOpen = false;
    },
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
  },
};
</script>
