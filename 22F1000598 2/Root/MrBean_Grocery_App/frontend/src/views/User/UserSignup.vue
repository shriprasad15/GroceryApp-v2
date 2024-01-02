
<template>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">

  <h1>Welcome to User Signup Page</h1>
  <form @submit.prevent="handleSignup">
    <div class="input-group">
      <span class="input-group-text">First and last name</span>
      <input type="text" aria-label="First name" v-model="firstName" class="form-control" required>
      <input type="text" aria-label="Last name" v-model="lastName" class="form-control" required>
    </div>
    <br>
    <div class="form-floating mb-3">
      <input type="number" class="form-control" v-model="mobile" placeholder="Mobile" required>
      <label>Mobile</label>
    </div>

    <div class="form-floating mb-3">
      <input type="email" class="form-control" v-model="email" placeholder="Email address" required>
      <label>Email address</label>
    </div>

    <div class="form-floating">
      <input type="password" class="form-control" v-model="password" placeholder="Password" required>
      <label>Password</label>
    </div>
    <br>
    <button type="submit" class="btn btn-primary">Submit</button>
    <router-link to="/user-login"><button type="button" class="btn btn-primary">Back</button></router-link>
  </form>
</template>

<script>
import { ref } from "vue";

export default {
  name: "Signup",
  data() {
    return {
      firstName: "",
      lastName: "",
      mobile: "",
      email: "",
      password: "",
      role: ["user"],
    };
  },
  methods:{
    async handleSignup(){
      console.log(this.firstName);
      try {
        const response = await fetch("http://localhost:5003/create-user", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            "fname": this.firstName,
            "lname": this.lastName,
            "email": this.email,
            "mobile": this.mobile,
            "password": this.password,
            "roles": this.role,
            "is_auth":1
          }),
        });

        const data = await response.json();
        if (response.status === 200) {
          console.log(data);
          alert("Account created successfully. Please verify email to login");
          this.$router.push('/user-login');
        } else {
          console.log("Something went wrong");
        }
      } catch (err) {
        console.log(err)
        //set values to null in the form
        this.firstName = "";
        this.lastName = "";
        this.mobile = "";
        this.email = "";
        this.password = "";


        alert("Account already exists");


        // this.$router.reload();
      }
    }
  },
};
</script>
