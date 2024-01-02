<template>


  <h2 style="background-color: #FDF697;color: #B6261D">
    <img src="../../../static/mrbean_icon.png" alt="MrBean Grocery App" style="width: 75px; height: 75px; margin-right: 15px;" />
    Manager Dashboard
  </h2>
    <nav class="navbar navbar-expand-lg bg-body-secondary">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" @click="toggleNavbar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" :class="{ 'show': isNavbarOpen }" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/manager-dashboard" class="nav-link" aria-current="page">Home</router-link>
            </li>

            <li class="nav-item dropdown" @mouseover="openProductDropdown" @mouseleave="closeProductDropdown">
              <a class="nav-link dropdown-toggle" role="button" @click.prevent>
                Product Operations
              </a>
              <div class="dropdown-menu" v-show="isProductDropdownOpen" @mouseover="openProductDropdown" @mouseleave="closeProductDropdown">
                <router-link v-for="item in productItems" :key="item" :to="`/manager-dashboard/${item}`" class="dropdown-item">{{ item }}</router-link>
              </div>
            </li>

            <li class="nav-item dropdown" @mouseover="openCategoryDropdown" @mouseleave="closeCategoryDropdown">
              <a class="nav-link dropdown-toggle" role="button" @click.prevent>
                Category Operations
              </a>
              <ul class="dropdown-menu" :class="{ 'show': isCategoryDropdownOpen }">
                <li v-for="item in categoryItems" :key="item">
                  <router-link :to="`/manager-dashboard/${item}`" class="dropdown-item">{{ item }}</router-link>
                </li>
              </ul>
            </li>
            <li class="nav-item">
              <router-link to="/manager-dashboard/Manager-PendingRequests" class="nav-link" aria-current="page">Pending Requests</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" role="button" @click="exportCSV">Generate Report</a>
            </li>
            <li class="nav-item">
              <button @click="logout" class="nav-link" >Logout</button>
            </li>
            <div v-if="confirmationModal" class="modal fade show" style="display: block;">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirmation</h5>
            <button type="button" class="btn-close" @click="confirmationModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to export the CSV?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="confirmationModal = false">Cancel</button>
            <button type="button" class="btn btn-success" @click="confirmExport">Confirm</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
          </ul>
        </div>
      </div>
    </nav>

    <RouterView/>
</template>

<script>
import {fetchCategories, fetchPendingCategories, fetchProducts} from "../../../api_helpers/helpers";
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
      productItems: ['Create-Product', 'Delete-Product', 'Edit-Product'],
      categoryItems: ['Create-Category', 'Delete-Category', 'Edit-Category'],
      category_items: [],
      product_items: [],
      confirmationModal: false,
      errorMessage: null,
    };
  },
  beforeCreate() {
    console.log("sdfc",sessionStorage.getItem("token")?.length);
    if(!sessionStorage.getItem("token")  || (JSON.parse(sessionStorage.getItem("role"))?.[0] !== "manager") ){
        sessionStorage.clear();
        this.$router.push('/manager-login');
      }
    },
  mounted() {
    this.assign();
  },
  methods: {
    async  logout() {
          sessionStorage.setItem("token", JSON.stringify(""));
          sessionStorage.clear()
          const response = await fetch('http://127.0.0.1:5003/signout');
          if(response.ok){
            this.$router.push('/manager-login');
            alert('Logout successful');
          }
          else{
            console.log(response)
            alert('Logout failed');
          }
          // console.log(sessionStorage.getItem("token"));

        },
     exportCSV() {
      this.confirmationModal = true;
    },
    async confirmExport() {
      // Call your API endpoint to export CSV here
      // Example using axios:
     this.isWaiting = true
      const res = await fetch('http://127.0.0.1:5003/gen_csv')
      const data = await res.json()
      if (res.ok) {
        this.confirmationModal = false; // Close confirmation modal
        alert('CSV will be exported shortly. Please check your mail in a few minutes.');
        const taskId = data['task-id']
        const intv = setInterval(async () => {
          const csv_res = await fetch(`http://127.0.0.1:5003/get_csv/${taskId}`)
          if (csv_res.ok) {
            this.isWaiting = false
            clearInterval(intv)
            // window.location.href = `http://127.0.0.1:5003/get_csv/${taskId}`
          }
        }, 1000)
      }
    },
    async assign() {
      this.category_items = await fetchCategories();
      this.product_items= await fetchProducts();
    },
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    openProductDropdown() {
      this.isProductDropdownOpen = true;
    },
    closeProductDropdown() {
      this.isProductDropdownOpen = false;
    },
    openCategoryDropdown() {
      this.isProductDropdownOpen = true;
    },
    closeCategoryDropdown() {
      this.isProductDropdownOpen = false;
    },
  },
};
</script>


<style>
.dropdown:hover .dropdown-menu {
  display: block;
}
</style>