<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="container mb-5 pt-5">
    <form @submit.prevent="createCategory" class="mb-5">
      <h5>Send a request to Admin for Category Creation</h5>
      <div class="form-floating mb-3">
        <input v-model="categoryName" type="text" aria-label="Category Name" class="form-control" required />
        <label for="floatingInput">Category Name</label>
      </div>
      <div class="pt-1 mb-4">
        <button class="btn btn-lg btn-block" type="submit" style="background-color: #6F4E37; color: white;">Submit</button>
      </div>
      <div v-if="requestSent" class="alert alert-info" role="alert">
        Category creation request sent for admin approval.
      </div>

    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categoryName: '',
      requestSent: false,
    };
  },
  methods: {
    async createCategory() {
      try {
        if (!this.categoryName.trim()) {
          console.error('Category name cannot be empty');
          return;
        }
        const catname = {
              "old_name": this.categoryName,
              "new_name": this.categoryName,
              "is_approved": 0
          }
        const token = JSON.parse(sessionStorage.getItem('token'));
        const response = await fetch('http://127.0.0.1:5003/api/category', {

          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': token
          },

          body: JSON.stringify(catname),
        });

        const jsonResponse = await response.json();
        if (jsonResponse.message === 'something went wrong') {
          alert('Category either already exists or given Category is not yet approved');
          this.categoryName = '';
        } else {
          if (response.ok) {
            this.requestSent = true;
            this.categoryName = '';
          }
        }
      } catch (error) {
        console.error('Error creating category:', error);
      }
    },
  },
};
</script>
