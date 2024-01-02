<template>

 <div class="container mt-5">
  <h2>Pending Requests</h2>

  <!-- Create Category -->
  <h3 class="mt-4">Create Category</h3>
  <div v-if="pendingCategoriesCreate.length <= 0" class="alert alert-danger mt-4" role="alert">
    No requests
    </div>
  <ul class="list-group">
    <li v-for="category in pendingCategoriesCreate" :key="category.id" class="list-group-item">
      {{ category.name[0].oldName }}
    </li>
  </ul>

  <!-- Delete Category -->
  <h3 class="mb-4 mt-5">Delete Category</h3>
  <div v-if="pendingCategoriesDelete.length <= 0" class="alert alert-danger mt-4" role="alert">
    No requests
  </div>
  <ul class="list-group">
    <li v-for="category in pendingCategoriesDelete" :key="category.id" class="list-group-item" >
      {{ category.name[0].oldName }}
    </li>
  </ul>

       <h3 class="mb-4 mt-5">Edit Category</h3>

        <div class="table-responsive">
          <div v-if="pendingCategoriesEdit.length <= 0" class="alert alert-danger mt-4" role="alert">
            No requests
          </div>
          <div v-else>
          <table class="table table-bordered">

            <thead class="table-primary">
              <tr>
                <th>Old Name</th>
                <th>New Name</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="category in pendingCategoriesEdit" :key="category.id">
                <td>{{ category.name[0].oldName }}</td>
                <td>{{ category.name[0].newName }}</td>
              </tr>
            </tbody>
          </table>
            </div>
        </div>

    </div>



</template>

<script>
import {fetchPendingCategories} from "../../../api_helpers/helpers";

export default {
  data() {
    return {
      pending_category_items: [],
      pendingCategoriesCreate:[],
      pendingCategoriesEdit:[],
      pendingCategoriesDelete:[]
    };
  },
  mounted() {
    this.assign();
  },
  methods:{
    async assign() {
      this.pending_category_items= await fetchPendingCategories();
      this.pendingCategoriesCreate = this.pending_category_items.filter(category => category.is_approved === 0),
          this.pendingCategoriesEdit = this.pending_category_items.filter(category => category.is_approved === -2),
          this.pendingCategoriesDelete = this.pending_category_items.filter(category => category.is_approved === -1)
    },
      // console.log(this.pending_category_items[0].is_approved)
    },

}
</script>