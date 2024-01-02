<template>

<!--  <div class="container mt-5">-->
    <div class="container mt-5" >
      <hr>
    <center><h2>Pending Manager Signups</h2></center>
      <hr>
    <!-- Create Manager Pending Requests -->
    <div>
      <div class="card shadow-lg">
      <u><h3 class="mt-5 mb-3" style="margin-left:430px">Create Manager Pending Requests</h3></u>
      <div>
        <table v-if="pendingManagers.length > 0" class="wider-table">
          <!-- Table headers -->
          <thead>
            <tr>
              <th style="width: 50%;">Manager First Name</th>
              <th style="width: 20%;">Manager Last Name</th>
              <th style="width: 20%;">Email</th>
              <th style="width: 20%;"></th>
            </tr>
          </thead>
          <!-- Table body for create manager pending requests -->
          <tbody>
            <tr v-for="(manager, index) in pendingManagers" :key="index">
              <td style="width: 20%;">{{ manager.fname }}</td>
              <td style="width: 20%;">{{ manager.lname }}</td>
              <td>{{ manager.email }}</td>
              <td>
                <button @click="approveCreateManager(manager.id)" class="btn btn-success">Approve</button>
                <button @click="rejectCreateManager(manager.id)" class="btn btn-danger">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="alert alert-danger mt-2"  role="alert" style="width: 50%; margin-left: 315px; text-align: center">No requests pending</div>
        </div>
      </div>
    </div>
      <hr>
    <center><h2 >Pending Manager Approvals</h2></center>
    <hr>

      <div class="card shadow-lg mb-5">
    <u><h3 class="mt-5 mb-3" style="margin-left:430px">Create Category Pending Requests</h3></u>
<div>
    <table v-if="pendingCategoriesCreate.length > 0" class="table-responsive">
  <!-- Table headers -->
  <thead>
    <tr>
      <th style="width: 50%;">Category Name</th>
      <th style="width: 20%;"></th>
    </tr>
  </thead>
  <!-- Table body for create category pending requests -->
  <tbody>
    <tr v-for="(category, index) in pendingCategoriesCreate" :key="index">
      <td>{{ category.name[0].oldName }}</td>
      <td>{{ category.requestedBy }}</td>
      <td>
        <button @click="approveCreateCategory(category.id)" class="btn btn-success">Approve</button>
        <button @click="rejectCreateCategory(category.id)" class="btn btn-danger">Reject</button>
      </td>
    </tr>
  </tbody>
</table>

<!--    <table v-else class="alert alert-danger mt-4 py-5 px-5" role="alert">No requests pending</table>-->
  <div v-else class="alert alert-danger mt-2"  role="alert" style="width: 50%; margin-left: 315px; text-align: center">No requests pending</div>
    </div>
      </div>
        <div class="card shadow-lg mb-5">
    <!-- Delete Category -->
    <u><h3 class="mt-5 mb-3" style="margin-left:430px">Delete Category Pending Requests</h3></u>
    <table v-if="pendingCategoriesDelete.length>0" class="table">
      <!-- Table headers -->
      <thead>
        <tr>
          <th>Category Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <!-- Table body for delete category pending requests -->
      <tbody>
        <tr v-for="(category, index) in pendingCategoriesDelete" :key="index">
          <td>{{ category.name[0].oldName }}</td>
          <td>
            <button @click="approveDeleteCategory(category.id)" class="btn btn-success">Approve</button><br>
            <button @click="rejectDeleteCategory(category.id)" class="btn btn-danger">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
          <div v-else class="alert alert-danger mt-2"  role="alert" style="width: 50%; margin-left: 315px; text-align: center">No requests pending</div>
        </div>
        <div class="card shadow-lg mb-4">
    <!-- Edit Category -->
    <u><h3 class="mt-5 mb-3" style="margin-left:430px">Edit Category Pending Requests</h3></u>
    <table v-if="pendingCategoriesEdit.length>0" class="table">
      <!-- Table headers -->
      <thead>
        <tr>
          <th>Old Name</th>
          <th>New Name</th>
          <th>Actions</th>
        </tr>
      </thead>
      <!-- Table body for edit category pending requests -->
      <tbody>
        <tr v-for="(category, index) in pendingCategoriesEdit" :key="index">
          <td>{{ category.name[0].oldName }}</td>
          <td>{{ category.name[0].newName }}</td>
          <td>
            <button @click="approveEditCategory(category.id)" class="btn btn-success">Approve</button>
            <button @click="rejectEditCategory(category.id)" class="btn btn-danger">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
          <div v-else class="alert alert-danger mt-2"  role="alert" style="width: 50%; margin-left: 315px; text-align: center">No requests pending</div>

  </div>

      </div>
</template>


<script>
import { fetchPendingCategories, fetchPendingManagers} from '../../../api_helpers/helpers'
export default {
  data() {
    return {
      pendingManagers: [], // To store pending managers fetched from the backend
      pendingCategories: [], // To store pending categories fetched from the backend
      pendingCategoriesCreate: [],
      pendingCategoriesEdit: [],
      pendingCategoriesDelete: [],
      categoryName: '',
      categoryId: ''
    };
  },
  methods: {
    async assign() {
      this.pendingCategories = await fetchPendingCategories();
      this.pendingManagers = await fetchPendingManagers();
      this.pendingCategoriesCreate = this.pendingCategories.filter(category => category.is_approved === 0);
      this.pendingCategoriesEdit = this.pendingCategories.filter(category => category.is_approved === -2);
      this.pendingCategoriesDelete = this.pendingCategories.filter(category => category.is_approved === -1);
    },
    async approveCreateManager(managerId){
      try {
        // this.managerId = this.pendingManagers.find(manager => manager.id === managerId).id;

        const response = await fetch(`http://127.0.0.1:5003/api/pending-managers`,{
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
          },

          body: JSON.stringify({"id": managerId}),
        });
        const data = await response.json();
        // console.log(data.message)
        // console.log(data)
        // console.log(response.message)
        if (response.ok) {
          alert(data.message);
          window.location.reload();
        } else {
          console.error('Something went wrong');
        }
        }
        catch (error) {
          console.error('Error creating manager:', error);
        }
    },
    async rejectCreateManager(managerId){
      try {
        // this.managerId = this.pendingManagers.find(manager => manager.id === managerId).id;

        const response = await fetch(`http://127.0.0.1:5003/api/pending-managers`,{
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
          },

          body: JSON.stringify({"id": managerId}),
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          window.location.reload();
        } else {
          console.error('Something went wrong');
        }
        }
        catch (error) {
          console.error('Error creating manager:', error);
        }
    },
    async approveCreateCategory(categoryId) {
      // Your approval logic for Create category
      try {
        this.categoryId = this.pendingCategoriesCreate.find(category => category.id === categoryId).id;

        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
          },

          body: JSON.stringify({"is_approved": 1}),
        });
        const jsonResponse = await response.json();
        if (jsonResponse.message === 'something went wrong') {
          alert('Category already exists');
        } else {
          if (response.ok) {
            console.log('Category created successfully');
            alert('Category created successfully');
            window.location.href = '/admin-dashboard/Approve-Requests';
          }
        }
      } catch (error) {
        console.error('Error creating category:', error);
      }
    },
    async rejectCreateCategory(categoryId) {
      console.log(categoryId);
      // Your rejection logic for Create category
      try {
        this.categoryId = this.pendingCategoriesCreate.find(category => category.id === categoryId).id;

        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
          },
        });
        if (response.ok) {
          alert('Category rejected successfully');
          window.location.href = '/admin-dashboard/Approve-Requests';
        } else {
          console.error('Something went wrong');
        }
      } catch (error) {
        console.error('Error rejecting category:', error);
      }

    },
    async approveEditCategory(categoryId) {
      // Your approval logic for Edit category
      try {
        this.categoryId = this.pendingCategoriesEdit.find(category => category.id === categoryId).id;
        const name={
          "old_name": this.pendingCategoriesEdit.find(category => category.id === categoryId).name[0].newName,
          "new_name": this.pendingCategoriesEdit.find(category => category.id === categoryId).name[0].newName,
          "is_approved": 1
      }
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))

          },

          body: JSON.stringify(name),
        });
        const jsonResponse = await response.json();
        if (jsonResponse.message === 'something went wrong') {
          alert('Category already exists');
        } else {
          if (response.ok) {
            console.log('Category created successfully');
            alert('Request Approved successfully');
            window.location.href = '/admin-dashboard/Approve-Requests';
          }
        }
      } catch (error) {
        console.error('Error creating category:', error);
      }
    },
    async rejectEditCategory(categoryId) {
      // Your rejection logic for Edit category
      try {
        this.categoryId = this.pendingCategoriesEdit.find(category => category.id === categoryId).id;
        const name={
          "old_name": this.pendingCategoriesEdit.find(category => category.id === categoryId).name[0].oldName,
          "new_name": this.pendingCategoriesEdit.find(category => category.id === categoryId).name[0].oldName,
          "is_approved": 1
      }
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))

          },

          body: JSON.stringify(name),
        });
        const jsonResponse = await response.json();
        if (jsonResponse.message === 'something went wrong') {
          alert('Category already exists');
        } else {
          if (response.ok) {
            // console.log( 'Category created successfully');
            alert('Request Approved successfully');
            window.location.href = '/admin-dashboard/Approve-Requests';
          }
        }
      } catch (error) {
        console.error('Error creating category:', error);
      }
    },
    async approveDeleteCategory(categoryId) {
      // Your approval logic for Delete category
      try {

        this.categoryId = this.pendingCategoriesDelete.find(category => category.id === categoryId).id;
        console.log(this.categoryId);
        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))

          },
        });
        if (response.ok) {
          alert('Category deleted successfully');
          window.location.href = '/admin-dashboard/Approve-Requests';
        } else {
          console.error('Something went wrong');
        }
      } catch (error) {
        console.error('Error deleting category:', error);
      }
    },
    async rejectDeleteCategory(categoryId) {
      // Your rejection logic for Delete category
      try {
        this.categoryId = this.pendingCategoriesDelete.find(category => category.id === categoryId).id;

        const response = await fetch(`http://127.0.0.1:5003/api/category/${this.categoryId}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': JSON.parse(sessionStorage.getItem('token'))

          },

          body: JSON.stringify({"is_approved": 1}),
        });
        const jsonResponse = await response.json();
        if (jsonResponse.message === 'something went wrong') {
          alert('Category already exists');
        } else {
          if (response.ok) {
            console.log('Category created successfully');
            alert('Request Rejected successfully');
            window.location.href = '/admin-dashboard/Approve-Requests';
          }
        }
      } catch (error) {
        console.error('Error creating category:', error);
      }
    },
  },
  mounted() {
      // Fetch pending categories when the component is mounted
      this.assign();
    }
}
</script>

<style scoped>
    /* Your CSS styles */
    .wider-table td {
      padding-right: 10px; /* Adjust the value as needed */
    }
    /* In your CSS file */
.wider-table td {
  margin-right: 10px; /* Adjust the value as needed */
}
.spaced-row {
  margin-bottom: 200px; /* Adjust the value as needed */
}

</style>