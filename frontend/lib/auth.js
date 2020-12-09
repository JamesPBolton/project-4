export function getUserId(){
  const token = localStorage.getItem('token')
  if (!token) return false

  const parsedToken = JSON.parse(atob(token.split('.')[1]))
  return parsedToken.sub
}

export function isCreator (compareId) {
  if (!compareId) return false
  return getUserId() === compareId
}