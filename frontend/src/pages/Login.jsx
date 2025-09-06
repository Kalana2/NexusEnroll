import { useState } from "react";
import "./login.css";

  async function login(email , password , setRole){
    const response = await fetch("http://localhost:8000/login" , {
      credentials:"include",
      method:"post",
      headers:{"content-type":"application/json"},
      body:JSON.stringify({
        email : email,
        password : password,
      })
    });
    const data = await response.json()
    if(data.success) setRole(data.role);
    else alert("user name or password invalid");
}




export default function Login({setRole}){
    const [email , setEmail] = useState('');
    const [password , setPassword] = useState('');



    return  <>
        <div class="background"></div>

        <div class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
            <div class="header-content">
                <div class="logo"><img src="/src/img/logo.png" /></div>
                <div class="header-text">
                <h2>Welcome Back</h2>
                <p>Sign in to your account</p>
                </div>
            </div>
            <button class="close-btn">×</button>
            </div>

            <div class="form-container">
            <div id="signinForm" method="post" action="/login">
                <div class="form-group">
                <label for="email">Email Address</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    placeholder="your.email@example.com"
                    required

                    onChange={(e)=>setEmail(e.target.value)}
                />
                </div>

                <div class="form-group">
                <label for="password">Password</label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    placeholder="Enter your password"
                    required
                    onChange={(e)=>setPassword(e.target.value)}
                />
                </div>

                <div class="form-options">
                <a href="#" class="forgot-password">Forgot password?</a>
                </div>

                <div class="button-container">
                <button onClick={()=>{
                    login(email , password   ,setRole)}
                } type="submit" class="btn btn-primary btn-full">
                    Sign In
                </button>
                </div>

                <div class="signup-link">
                Don't have an account?
                <a href="#" class="signup-link-text">Sign up</a>
                </div>
            </div>
            </div>
        </div>
        </div>
    </>
}