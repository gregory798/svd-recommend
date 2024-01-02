<template>
  <div  class="dashboard-page">
    <h1>Welcome to the Dashboard</h1>
    <!-- Display movie list or any content for the dashboard -->
    <div class="movie-list">
      <h2>Movies:</h2>
      <ul>
        <li v-for="movie in movies" :key="movie.id">
          {{ movie.title }}
        </li>
      </ul>
    </div>
    <button class="logout-button" @click="logout">Logout</button>
  </div>
</template>

<script>
export default {
  name: 'DashboardPage',
  data() {
    return {
      movies: [
        { id: 1, title: 'Movie 1' },
        { id: 2, title: 'Movie 2' },
        { id: 3, title: 'Movie 3' },
        // Add more movie objects as needed
      ],
    };
  },
  computed: {
    loggedInUserId() {
      // Retrieve user ID from localStorage after successful login
      return localStorage.getItem('token');
    },
  },
  methods: {
    logout() {
      // Simulate logout action by removing the token from localStorage
      localStorage.removeItem('token');
      this.$router.push('/login'); // Redirect to the login route
    },
  },
};
</script>

<style scoped>
/* Add your dashboard page styles here */
.dashboard-page {
  margin: 10px auto;
  height:700px;
  max-width: 1200px;
  padding: 10px;
  border: 5px solid #ccc;
  border-radius: 2px;
  background: #f9f9f9;
  color: black; /* Set text color to black */
}

.logout-button {
  position: absolute;
  top: 10px; /* Adjust as needed for the top spacing */
  right: 60px; /* Adjust as needed for the right spacing */
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.movie-list {
  margin-top: 20px;
}

.movie-list ul {
  list-style: none;
  padding: 0;
}

.movie-list li {
  margin-bottom: 5px;
}
</style>
