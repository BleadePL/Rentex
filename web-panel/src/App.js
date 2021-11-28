import React, {useState, useEffect} from 'react' 
import {BrowserRouter as Router, useNavigate, Route, Routes} from "react-router-dom"
import API_Session from "./API_Connector";
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import './App.css'

const api = new API_Session();


function App() {
  //Testing data
  const adminUser = {
    login: "admin",
    password: "admin123"
  }

  const [user, setUser] = useState({name: "", surname: "", login: "", password: "", address: "", email: "", pesel: ""});
  const [error, setError] = useState("");

  const Login = details =>{
    console.log(details);
    //Praca na bazie
    // api.login(details.email, details.password, setError("success"), setError("invalid_data"), setError("authorization_err"));

    // if(error == "success"){
    //   console.log("Logged in");
    //   setUser({
    //     name: details.name,
    //     email : details.email,
    //     password : details.password
    //   });
    // }else {
    //   console.log(error);
    // }

    if(details.login == adminUser.login && details.password == adminUser.password){
      console.log("Logged in");
      setError("success");

      setUser({
        // name: details.name,
        // email : details.email,
        // password : details.password

        login: details.login,
        name: "Daniel",
        surname: "Markowski",
        gender: "M",
        password: details.password,
        address: "20;Sienkiewicza;60951;Tarnobrzeg;Polska",
        email: details.email,
        pesel: "60060535351"
      });

      navigate("/loggedIn");
  
    }
    else if(user.login == details.login) navigate("/loggedIn");
    else setError("invalid_data");
  }

  const Logout = () => {

    // Praca na bazie
    
    // api.logout(setError("success"), setError("failure"));

    // if(error == "success")
    // {
    //   setUser({name: "", email: ""});
    //   setError("");
    // }
    // else{
    //   console.log(error);
    // }

    setError("");

    navigate("/");
  }

  const Register = details => {
    api.register(details.name, details.surname, details.gender, details.login, details.password, details.address, details.email, details.pesel, setError("success"), setError("Failure"));

    if(error == "success" || 1 == 1){
      setUser({
        // name: details.name,
        // email : details.email,
        // password : details.password

        login: details.login,
        name: details.name,
        surname: details.surname,
        gender: details.gender,
        password: details.password,
        address: details.address,
        email: details.email,
        pesel: details.pesel
      });
      navigate("/loggedIn");
      console.log(details);
    }
  }

  const RentCar = () => {

  }

  const BrowseCars = () => {

  }

  const navigate = useNavigate();
  useEffect(() => {
    if(user.name == "") navigate("/")
  },[])

  return (
      
    <Routes>
        <Route path="/" element={
            <div>
              <h1>Welcome to Rentex</h1>
              <button name="login" onClick={() => navigate("/login")}>Login</button>
              <button name="register" onClick={() => navigate("/register")}>Register</button>
            </div>
        }/>

          <Route path="/login" element = {
            <div>
              <LoginForm Login={Login} error={error}/>
              <button name="index" onClick={() => navigate("/")}>Return</button>
            </div>
          } />
          

          <Route path="/register" element = {
            <div>
              <RegisterForm  Register={Register} error={error}/>
              <button name="index" onClick={() => navigate("/")}>Return</button>
            </div>
          }/>

          <Route path="/loggedIn" element = {
              <div>
                <h2>Welcome, <span>{user.name}</span></h2>

                <ul>
                  <li><button name="rent-car" onClick={RentCar}>Rent a car</button></li>
                  <li><button name="browse-cars" onClick={BrowseCars}>Browse available cars</button></li>
                  <li><button name="reserved-car">Reserved car</button></li>
                  <li><button name="logout" onClick={Logout}>Logout</button></li>
                </ul>
              </div>
          }/>


      
    </Routes>
      
  );
}

export default App;