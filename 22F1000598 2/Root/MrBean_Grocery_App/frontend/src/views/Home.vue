<template>
  <div class="content-element">
    <!-- Navigation bar -->
    <nav class="navbar navbar-dark navbar-expand-lg bg-dark border-bottom border-primary">
      <div class="container-fluid">
        <div style="cursor: pointer;" class="navbar-brand">
          <img src="../../static/mrbean_icon.png" alt="MrBean Grocery App" style="cursor: pointer;width: 60px; height: 60px; margin-right: 5px;" />
          MrBean Grocery App
          </div><br>
        <div class="d-flex justify-content-center"> <!-- Align buttons center -->
          <router-link class="btn btn-primary me-2" to="/user-login">User Page</router-link>
          <router-link class="btn btn-primary me-2" to="/manager-login">Manager Page</router-link>
          <router-link class="btn btn-primary me-2" to="/admin-login">Admin Dashboard</router-link>
          <button class="btn btn-primary me-2" @click="installApp" v-if="deferredPrompt">Add to Desktop</button>

        </div>
      </div>
    </nav>

    <!-- Main content -->
    <div style="height: 60vh;" class="d-flex flex-column w-100 justify-content-center align-items-center">
      <h1>Welcome to MrBean Grocery App</h1>
    </div>
    <footer class="footer bg-dark text-light text-center py-5">
      <h5>Creator Details</h5>
      <div class="creator-details">
        <p>Name: S Shriprasad</p>
        <p>Email: 22f1000598@ds.study.iitm.ac.in</p>
        <p>IIT Madras BS in Data Science and Applications</p>
      </div>
      <div class="container">
        <p>&copy; 2023 MrBean Grocery App</p>
      </div>
    </footer>
  </div>
</template>

<style>
/* Add styling for the footer */
.creator-details p {
  margin-bottom: 5px; /* Adjust this value as needed */
}
.footer {
  padding-top: 50px;
}

</style>


<script>
export default {
  data() {
    return {
      deferredPrompt: null
    };
  },
  beforeCreate() {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
    });
  },
  methods: {
    installApp() {
      if (this.deferredPrompt) {
        this.deferredPrompt.prompt();
        this.deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            alert("MrBean Grocery App was installed")
            console.log('User accepted the Add to Desktop prompt');
          } else {
            alert("MrBean Grocery App was not installed");
            console.log('User dismissed the Add to Desktoo prompt');
          }
          this.deferredPrompt = null;
        });
      }
    }
  }
};
</script>
