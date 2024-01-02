export default function ({ route, redirect }) {
  if (route.path !== '/login') {
    // Redirect to login page if the route is not the login page
    redirect('/login')
  }
}
