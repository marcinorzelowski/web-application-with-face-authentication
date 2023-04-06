
export interface UserLoginData {
  username: string,
  password: string
}

export interface UserRegisterData {
  username: string,
  password: string
}

export interface AuthResponse {
  token: string
  email: string,
  firstName: string,
  lastName: string,
}

export interface User {
  email: string,
  firstName: string,
  lastName: string,
}
