export const isAuthenticated = () => {
  const sessionKey = sessionStorage.getItem('yourKey');
  const secretkey = env.JWT_SECRET
  if(sessionKey!=secretkey){
    return false
  }

  return !!sessionKey; // Return true if a session key exists, false otherwise
};