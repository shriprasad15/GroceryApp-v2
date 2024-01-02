

<template>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
       <section class="vh-100" style="background-color: #273447;">
  <div class="container py-5 h-100">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col col-xl-10">
        <div class="card" style="border-radius: 1rem;">
          <div class="row g-0">
            <div class="col-md-6 col-lg-5 d-none d-md-block">
              <img src="../../../static/mrbean_login.jpg"
                alt="login form" class="img-fluid" style="border-radius: 1rem 0 0 0;" height="273"/>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

                <img src="../../../static/mrbean_login.jpg"
                alt="login form" class="img-fluid" style="border-radius: 0 0 0 1rem;" height="273"/>
            </div>
            <div class="col-md-6 col-lg-7 d-flex align-items-center">
              <div class="card-body p-4 p-lg-5 text-black">


                  <div class="d-flex align-items-center mb-3 pb-1">
                    <i class="fas fa-cubes fa-2x me-3" style="color: #ff6219;"></i>
                    <span class="h1 fw-bold mb-0">MrBean Groceries</span>
                  </div>

                  <h5 class="fw-normal mb-3 pb-3" style="letter-spacing: 1px;">Sign into your account</h5>

                 <div class="form-floating mb-3">
                      <input v-model="email" type="email" class="form-control" id="floatingInput" placeholder="name@example.com" required>
                      <label for="floatingInput">Email address</label>
                    </div>

                  <div class="form-floating">
                      <input v-model="password" type="password" class="form-control" id="floatingPassword" placeholder="Password" required>
                      <label for="floatingPassword">Password</label>
                    </div>
                  <br>

                  <div class="pt-1 mb-4">

<!--                    <button @click="submitForm" class="btn btn-lg btn-block" type="submit" style="background-color: #6F4E37; color: white;">Login</button>-->
                    <button
                        @click="submitForm"
                        :class="{ 'btn-block': isLoading, 'btn-lg': !isLoading, 'btn': !isLoading, 'btn-secondary': !isLoading, 'disabled': isLoading }"
                        type="submit"
                        style="background-color: #6F4E37; color: white;"
                        :disabled="isLoading"
                    >
                      <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                      <span v-else>Login</span>
                    </button>

                  </div><br>
                  <p class="mb-5 pb-lg-2" style="color: #393f81;">Don't have an account? <a href="/user-signup"
                      style="color: #393f81;">Register here</a></p>
                <a href="/"><button type="button" class="btn btn-primary" style="background-color: #6F4E37; color: white;">Home</button></a>
<!--                </form>-->

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

</template>


<script>
import {ref} from "vue";

export default {

  data() {
    return {
      email: '',
      password: '',
      role:'',
      isLoading:false,
    };
  },
  props: {
    error: String,
  },
  beforeCreate() {
    if(sessionStorage.getItem("token")  && (JSON.parse(sessionStorage.getItem("role"))?.[0] === "user") ){
      this.$router.push('/user-dashboard');
    }
  },
  methods: {
    async submitForm() {
      this.isLoading = true;
      const formData = {
        email: this.email,
        password: this.password,
      };
      setTimeout(async () => {
      const response = await fetch('http://127.0.0.1:5003/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // 'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      console.log(data);
      if (data.message === "Invalid user!") {
        alert('Login Failed. Invalid Credentials');
        this.email = '';
        this.password = '';
        this.$router.push('/user-login');
      } else if (data.message === 'Wrong Password!') {
        alert('Login Failed. Wrong Password');
        this.email = '';
        this.password = '';
        this.$router.push('/user-login');
      } else if (data.message === "User not authenticated!") {
        alert('Login Failed. User not yet authenticated');
        this.email = '';
        this.password = '';
        this.$router.push('/user-login');
      } else {
        if (response.status === 200) {

          // console.log('Login successful');
          sessionStorage.setItem("token", JSON.stringify(data.token));
          if (data.role[0] === "user") {
            console.log(data.role[0]);
            sessionStorage.setItem("role", JSON.stringify(data.role));
            sessionStorage.setItem("email", JSON.stringify(data.email));
            sessionStorage.setItem("mobile", JSON.stringify(data.mobile));
            sessionStorage.setItem("fname", JSON.stringify(data.fname));
            sessionStorage.setItem("lname", JSON.stringify(data.lname));

            // alert('Login successful');
            this.$router.push('/user-dashboard');
          } else {
            const logout_response = await fetch('http://127.0.0.1:5003/signout');
            if (logout_response.ok) {
              alert('Login Failed. Invalid Credentials');
              this.email = '';
              this.password = '';
              this.$router.push('/user-login');
            }
          }

        }
      }
      this.isLoading = false;
    },2000);
    },
  },
};
</script>