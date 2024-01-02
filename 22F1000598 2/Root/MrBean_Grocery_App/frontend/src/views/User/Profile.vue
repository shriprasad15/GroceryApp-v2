<template>
  <div>
    <center>
      <h3>
        <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" fill="currentColor" class="bi bi-person-circle" viewBox="0 0 16 16">
          <!-- SVG content -->
        </svg>
        Welcome {{ fname }} {{ lname }} to Profile Page of MrBean Groceries
      </h3>
    </center>

    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <!-- Navbar content -->
    </nav>

    <div class="container mt-5">
      <h1>Profile</h1>
      <div class="row">
        <div class="col-md-5">
          <div class="card mb-4">
            <div class="card-body">
              <h4>User: {{ fname }} {{ lname }}</h4>
              <h4>Email ID: {{ email }}</h4>
              <h4>Mobile Number: {{ mobile }}</h4><br>
            </div>
          </div>
        </div>
      </div>

      <h2>Ordered Items</h2>
      <div v-if="profile_items.length > 0" class="row">
        <div v-for="product in profile_items" :key="product.id" class="col-md-4">
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">{{ product.product_name }}</h5>
              <p class="card-text">Rate Per Unit: ₹{{ product.rate_per_unit }}</p>
              <p class="card-text">Quantity: {{ product.quantity }}</p>
              <p class="card-text">Purchase Date & Time: {{ product.date_purchased }}</p>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <br><h3>No items purchased</h3>
<router-link :to="'/user-dashboard'"><h4>Click here to buy Products</h4></router-link>

      </div>
    </div>
  </div>
</template>

<script>
import { fetchProfileDetails } from "../../../api_helpers/helpers";

export default {
  data() {
    return {
      // Initialize data with empty values or defaults
      fname: JSON.parse(sessionStorage.getItem("fname")) || "",
      lname: JSON.parse(sessionStorage.getItem("lname")) || "",
      email: JSON.parse(sessionStorage.getItem("email")) || "",
      mobile: JSON.parse(sessionStorage.getItem("mobile")) || "",
      profile_items: [] // Initialize as an empty array
    };
  },
  async mounted() {
    // Fetch profile details on component creation
    console.log("error")
    await fetchProfileDetails().then((data) => {
      this.profile_items = data;
    })
    console.log("Profile: ",this.profile_items)
  }
};
</script>

<style>
/* Add any necessary styles here */
</style>
