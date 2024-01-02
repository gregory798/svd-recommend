export default function ({ route, redirect }) {
    if (route.path !== '/dashboard' && !localStorage.getItem('token')) {
      // Redirect to dashboard page if the route is not the dashboard and the user is logged in
      redirect('/dashboard')
    }
  }
  
