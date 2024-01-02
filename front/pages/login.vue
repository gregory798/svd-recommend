<template>
  <div class="login-page">
    <h5>Login Page</h5> 
    <br>
    <form @submit.prevent="loginAction"> <!-- Update method name here -->
      <div class="mb-3">
       <label for="userId" class="form-label">User ID</label> <br> <br>
       <input v-model="userId" type="text" class="form-control" id="userId"  required/>
      </div>
      <div class="d-grid gap-2">
      <button class="login-button" type="submit">Login</button>   </div>
      <p v-if="validationErrors" class="text-center"><small class="text-danger">Incorrect User ID</small></p>
    </form>
  
  </div>
</template>


<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      showLoginPage: false,
      userId: '',
      validationErrors: false,
      users: [
        { userId: '1234' },
        { userId: '9876' },
        { userId: '4356' },
      ],
    };
  },
  methods: {
    loginAction() { // Correct method name here
      const foundUser = this.users.find(user => user.userId === this.userId);
      if (foundUser) {
        // Simulating a successful login
        // For real authentication, you would handle tokens or session management here
        localStorage.setItem('token', 'someToken');
        this.showLoginPage = false;
        // Redirect to the dashboard page
        this.$router.push('/dashboard');
      } else {
        this.validationErrors = true;
      }
    },
  },
};
</script>

<style>
/* Add your login page styles here */
.login-page {
  /* Example styles */
  margin: 50px auto;
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background: #222;
  color: white;
  text-align: center;
}

.error-message {
  color: red;
  margin-top: 10px;
}
.form-control {
    background-color: #f0f0f0;
    color: rgb(9, 9, 9)
    }
.login-button {
  background-color: #007bff;
  padding: 6px 14px;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  border: none;
}
</style>
