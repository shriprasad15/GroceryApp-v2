<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="container mb-5 pt-5">

    <form @submit.prevent="showConfirmation" class="mb-5">
      <h3>Request Delete Category</h3>
      <div v-if="dropdownItems<=0" class="alert alert-danger mt-4" role="alert">
        No category to delete
      </div>
      <div v-else>
      <h5>Select Category requesting to delete</h5>
      <div>
        <select v-model="selectedCategory" class="form-select">
          <option value="" disabled>Select Category to delete</option>
          <option v-for="item in dropdownItems" :key="item.id" :value="item.id">{{ item.name[0].oldName }}</option>
        </select>
      </div>

      <div>
        <button type="submit" class="btn btn-danger mt-4">Delete</button>
      </div>

      <div v-if="confirmationBox" class="alert alert-danger mt-3" role="alert">
        Are you sure you want to request for deleting "{{ selectedCategoryName[0].oldName }}" <br>The products associated with this category would also be deleted if approved?
        <button @click="confirmDelete" class="btn btn-danger btn-sm ms-2">Confirm</button>
        <button @click="cancelDelete" class="btn btn-secondary btn-sm ms-2">Cancel</button>
      </div>


      </div>
    </form>
  </div>
</template>

<script>
import { fetchCategories } from "../../../../api_helpers/helpers";

export default {
  data() {
    return {
      dropdownItems: [],
      selectedCategory: null, // Store only the ID of the selected category
      selectedCategoryName: '', // Store the name of the selected category
      confirmationBox: false, // Control visibility of the confirmation dialog
    };
  },
  methods: {
    async showConfirmation() {
      if (!this.selectedCategory) {
        alert('Please select a category');
        return;
      }

      const selected = this.dropdownItems.find(item => item.id === this.selectedCategory);
      if (selected) {
        this.selectedCategoryName = selected.name;
        this.confirmationBox = true;
      }
    },

    async deleteCategory() {
      console.log(this.selectedCategory);
      try {
        console.log(this.selectedCategoryName[0]['oldName'])
        const catname = {
              "old_name": this.selectedCategoryName[0]['oldName'],
              "new_name": this.selectedCategoryName[0]['oldName'],
              "is_approved": -1
          }
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.selectedCategory}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))

          },
          body: JSON.stringify(catname),
        });

        if (response.ok) {

          this.selectedCategory = null;
          this.confirmationBox = false;
          await this.fetchAndSetCategories();
          alert(`Category '${this.selectedCategoryName[0].oldName}' delete requested sent`);
          this.selectedCategoryName = '';
          if (this.dropdownItems.length===0){
            window.location.href = '/admin-dashboard';
          }
        } else {
          console.error('Failed to delete category');
        }
      } catch (error) {
        console.error('Error deleting category:', error);
      }
    },

    confirmDelete() {
      this.deleteCategory();
    },

    cancelDelete() {
      this.confirmationBox = false;
    },

    async fetchAndSetCategories() {
      try {
        this.dropdownItems = await fetchCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
  },
  mounted() {
    this.fetchAndSetCategories();
  },
};
</script>

