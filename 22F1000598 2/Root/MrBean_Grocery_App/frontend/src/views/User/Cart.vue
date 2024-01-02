<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="container mt-5 mb-5">
    <h1 class="mb-4">Cart</h1>


    <!-- Display error message if exists -->
<!--    <div v-if="error" class="alert alert-danger mb-3" role="alert">-->
<!--      {{ error }}-->
<!--    </div>-->

    <!-- Product Cards -->
    <div class="row">
      <div v-for="product in product_items" :key="product.id" class="col-md-4">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">Rate Per Unit: ₹{{ product.rate_per_unit }}</p>
            <p class="card-text">Available quantity on stock: {{ product.quantity }}</p>

            <!-- Quantity Edit Form -->
              <div class="mb-3">
       <b> <label for="quantity" class="form-label">Selected Quantity: {{ product.cart_quantity }}</label></b>
        <div class="input-group">
          <input type="number" class="form-control" id="quantity" v-model="product.updateQty" min="1" :max="product.cart_quantity">
          <button class="btn btn-primary" @click="updateQuantity(product.product_id, product.updateQty)">Update Quantity</button>
        </div>
      </div>


            <p class="card-text">Manufacture Date: {{ product.manufacture_date }}</p>
            <p class="card-text">Expiry Date: {{ product.expiry_date }}</p>

            <!-- Remove Product Link -->
            <button @click="deleteProduct(product.product_id)" class="btn btn-danger">Remove Product</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Apply Coupon Code Form -->
<!--    <form :action="`/coupon/${userid}`">-->
<!--      <div class="mt-4 text-center">-->
<!--        <h4>Apply Coupon Code</h4>-->
<!--        <input type="text" class="form-control" id="coupon" name="coupon" v-model="couponCode">-->
<!--      </div>-->
<!--      <button type="submit" class="btn btn-primary">Apply</button>-->
<!--    </form>-->

    <!-- Total Cart Price and Buy All Button -->
    <div class="mt-4 text-center">
      <h4>Total Cart Price: ₹{{ total_price }}</h4>
      <button @click="buyAll()">Buy All</button>
    </div>
  </div>
</template>

<script>
export default {

  data() {
    return {
      couponCode: '', // For storing coupon code
    updateQty:Number,
    userid: '',
    product_items: [],
    total_price: Number,
    };
  },

  created() {
    console.log(this.product_items)
  },
  mounted() {
    this.fetch_cart_quantity()
  },
  methods:{
    // Function to convert date to time

    async fetch_cart_quantity(){
      const response = await fetch(`http://127.0.0.1:5003/api/cart`,{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        },
      });
      const data = await response.json();
      if (response.ok) {
        // this.cart_value = data.length;
        this.product_items = data;
      }
      else {
        console.error('Failed to fetch cart');
      }
    },
    async updateQuantity(product_id, product_qty) {
      if(product_qty === 0){
        this.deleteProduct(product_id);
      }
      // console.log(this.product.cart_quantity, "sdcdsc")
      try {
        const response = await fetch(`http://127.0.0.1:5003/api/cart/${product_id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },

          body: JSON.stringify({
            quantity: product_qty
          }),
        });
        if (response.ok) {
        alert('Quantity updated successfully');
        window.location.reload();
      } else {
        console.error('Failed to update quantity');
      }
      } catch (error) {
        alert('Item quantity exceeded');
      }
    },
      async deleteProduct(product_id){
        const response = await fetch(`http://127.0.0.1:5003/api/cart/${product_id}`,{
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
          },
        });
        if (response.ok) {
          alert('Product deleted successfully');
          window.location.reload();
        }
        else {
          console.error('Failed to delete product');
        }
      },
    async buyAll() {
      try {
        const response = await fetch(`http://127.0.0.1:5003/api/buy`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))
          },
        });
        if (response.ok) {
          alert('Products purchased successfully');
          window.location.reload()
          this.$router.push('/user-dashboard');

        } else {
          console.error('Failed to buy product');
        }
    }catch (error) {
        alert('Item quantity exceeded');
    }
    },
    },
    computed: {
      // Function to calculate total price of all products in cart
      total_price() {
        let total = 0;
        for (let i = 0; i < this.product_items.length; i++) {
          total += this.product_items[i].rate_per_unit * this.product_items[i].cart_quantity;
        }
        return total;
      },
    },
  }
</script>

