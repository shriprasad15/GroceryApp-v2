<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="container mt-5 mb-5" >

    <form @submit.prevent="createCategory" class="mb-5">
      <h3>Create Category</h3>
      <div class="form-floating mb-3">
        <input v-model="categoryName" type="text" aria-label="Category Name" class="form-control" required style="width: 50%"/>
        <label for="floatingInput" >Category Name</label>
      </div>
      <div class="pt-1 mb-4">
        <button class="btn btn-lg btn-block" type="submit" style="background-color: #6F4E37; color: white;">Submit</button>
      </div>

    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categoryName: '', // To store the category name from the input

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
              "is_approved": 1
          }
    const token = JSON.parse(sessionStorage.getItem('token'));
    // console.log(JSON.parse(sessionStorage.getItem('token')));
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
          alert('Category already exists');
          this.categoryName='';
          }
        else {
          if (response.ok) {
            console.log('Category created successfully');
            alert('Category created successfully');
            window.location.href = '/admin-dashboard';
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

<style>
/* Your CSS styles */
</style>
