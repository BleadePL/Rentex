import React, {useState, useEffect} from 'react' 
import {BrowserRouter as Router, useNavigate, Route, Routes} from "react-router-dom"
import API_Session from "./API_Connector";
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import DescriptionTable from './components/DescripionTable';
import './App.css'
import ChangePasswordForm from './components/ChangePasswordForm';
import NearestCarsForm from './components/NearestCars';

const api = new API_Session();


function App() {

  const [user, setUser] = useState({name: "", surname: "", login: "", password: "", address: "", email: "", pesel: ""});
  const [error, setError] = useState();
  const [car, setCar] = useState();
  const [reserved, setReservation] = useState()

  


    const Login = details =>{
    //Praca na bazie
    // api.login(details.login, details.password, LoadUser , () => setError("invalid"), setError)
    api.getUserDetails(setUser, () => console.log())
    api.getNearestCars('51.119475', '17.050562', 100000, setCar, console.log, console.log)
    navigate("/loggedIn")
  }
  
  
  // const LoadUser = () => {
  //   api.getUserDetails(setUser, () => console.log())
  //   navigate("/loggedIn")
  // }



  const Logout = () => {

    setError("");

    navigate("/");
  }

  const Register = details => {
    //api.register(details.name, details.surname, details.gender, details.login, details.password, details.address, details.email, details.pesel, setError("success"), setError("Failure"));

  }


  const BrowseCars = (details, resId) => {
      console.log(details)
      console.log(resId)
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
              <LoginForm Login={Login} api={api}/>
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
                  {/* <li><button name="rent-car" onClick={RentCar}>Rent a car</button></li> */}
                  <li><button name="browse-cars" onClick={() => navigate("/browse-cars")}>Browse available cars</button></li>
                  <li><button name="reserved-car">Reserved car</button></li>
                  <li><button name="persona-data" onClick={() => navigate("/userDescr")}>User Description</button></li>
                  <li><button name="logout" onClick={Logout}>Logout</button></li>
                </ul>
              </div>
          }/>

          
          <Route path="/userDescr" element={
              <div>
                <DescriptionTable data={user}/>
                <button name="index" onClick={() => navigate("/loggedIn")}>Return</button>
              </div>
          }/>

          <Route path="/browse-cars" element={
              <div>
                {/* {() => api.getNearestCars("51.1", "16.2", 100000, setCar, () => console.log(), () => console.log())} */}
                <NearestCarsForm data={user} Reserve={BrowseCars} cars={car} api={api}/>
                <button name="index" onClick={() => navigate("/loggedIn")}>Return</button>
              </div>
          }/>

      
    </Routes>
      
  );
}

export default App;