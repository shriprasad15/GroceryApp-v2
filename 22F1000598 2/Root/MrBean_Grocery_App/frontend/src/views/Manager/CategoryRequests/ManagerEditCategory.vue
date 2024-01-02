<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
  <div class="container mb-5 pt-5">

    <form @submit.prevent="showEditConfirmation" class="mb-5">
      <h3>Request Edit Category</h3>
      <div v-if="dropdownItems.length <= 0" class="alert alert-danger mt-4" role="alert">
        No categories found
      </div>
      <div v-else>
        <div>
          <h5>Select category to request the change: </h5>
          <select v-model="selectedCategory" class="form-select">
            <option value="" disabled>Select Category to edit</option>
            <option v-for="item in dropdownItems" :key="item.id" :value="item.id">{{ item.name[0].oldName }}</option>
          </select>
        </div>
      <h5>Enter new category name: </h5>
      <input v-model="newCategoryName">
      <br><br>


      <br>
      <div>
        <button type="submit" class="btn btn-primary">Edit Category</button>
      </div>

      <div v-if="editConfirmationBox" class="alert alert-warning mt-3" role="alert">
        Are you sure you want to request to change"{{ selectedCategoryName[0].oldName }}" into "{{ newCategoryName }}"?
        <button @click="confirmEdit" class="btn btn-warning btn-sm ms-2">Confirm</button>
        <button @click="cancelEdit" class="btn btn-secondary btn-sm ms-2">Cancel</button>
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
      newCategoryName: '', // Store the new category name from input
      editConfirmationBox: false, // Control visibility of the edit confirmation dialog
    };
  },
  methods: {
    async showEditConfirmation() {
      if (!this.selectedCategory || !this.newCategoryName) {
        alert('Please select a category and enter a new name');
        return;
      }

      const selected = this.dropdownItems.find(item => item.id === this.selectedCategory);
      if (selected) {
        this.selectedCategoryName = selected.name;
        this.editConfirmationBox = true;
      }
    },

    async editCategory() {
      try {
        const catname = {
              "old_name": this.selectedCategoryName[0]['oldName'],
              "new_name": this.newCategoryName,
              "is_approved": -2
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
          this.editConfirmationBox = false;
          await this.fetchAndSetCategories();
          alert(`Category '${this.selectedCategoryName[0].oldName}' edit request to '${this.newCategoryName} sent'`);
          this.selectedCategoryName = '';
          this.newCategoryName = '';
        } else {
          console.error('Failed to edit category');
        }
      } catch (error) {
        console.error('Error editing category:', error);
      }
    },

    confirmEdit() {
      this.editCategory();
    },

    cancelEdit() {
      this.editConfirmationBox = false;
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
