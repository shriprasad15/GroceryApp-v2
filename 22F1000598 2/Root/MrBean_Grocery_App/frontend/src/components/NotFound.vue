<template>
  <div class="mr-bean-container">
    <img src="../../static/mrbean_login.jpg" alt="Mr. Bean Image" class="mr-bean-img">
    <h1>404!</h1>
    <h3 class="mr-bean-title">Oops! You've Found Mr. Bean's Silly Side</h3>
    <p class="mr-bean-message">Sorry, the page you're looking for seems to be as elusive as Mr. Bean's comic timing.</p>
    <router-link to="/" class="mr-bean-link">Go Back to Safety</router-link>
  </div>
</template>

<script>
export default {
  // Component logic
};
</script>

<style>
/* Styles for Mr. Bean themed 404 page */
.mr-bean-container {
  text-align: center;
  margin-top: 50px;
  font-family: 'Arial', sans-serif;
}

.mr-bean-img {
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.mr-bean-title {
  font-size: 2em;
  margin-top: 20px;
  color: #333;
}

.mr-bean-message {
  margin-top: 15px;
  color: #555;
}

.mr-bean-link {
  display: inline-block;
  margin-top: 25px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.mr-bean-link:hover {
  background-color: #0056b3;
}
</style>
