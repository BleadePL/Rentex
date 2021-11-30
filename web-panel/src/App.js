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

let registerUser = {
  name: "", 
  surname: "", 
  login: "", 
  password: "", 
  address: "", 
  email: "", 
  pesel: ""
}

function App() {
  //Testing data
  const adminUser = {
    name: "Daniel",
    surname: "Wątroba",
    login: "admin",
    password: "admin123",
    address: "Kamienna 27/5",
    email : "watrobowa@wp.pl",
    pesel : "0012312324"
  }


  const [user, setUser] = useState({name: "", surname: "", login: "", password: "", address: "", email: "", pesel: ""});
  const [error, setError] = useState();
  const [data, setData] = useState({name: "", surname: "", login: "", address: "", email: "", pesel: ""});
  const [car, setCar] = useState({"carId" : ""});

  const Login = details =>{
    console.log(details);
    //Praca na bazie
    // api.login(details.login, details.password, setError("success"), setError("invalid_data"), setError("authorization_err"));

    // if(error == "success"){
    //   console.log("Logged in");
    //   setUser({
    //     login: details.login,
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

        name: adminUser.name,
        surname: adminUser.surname,
        login: details.login,
        password: details.password,
        address: adminUser.address,
        email: adminUser.email,
        pesel: adminUser.pesel
      });

      setData({
        name: adminUser.name,
        surname: adminUser.surname,
        login: details.login,
        address: adminUser.address,
        email: adminUser.email,
        pesel: adminUser.pesel
      });

      navigate("/loggedIn");
    }
    else if(registerUser.login == details.login && registerUser.password == details.password && registerUser.login != ""){ 
      console.log("Logged in");
      setUser({
        // name: details.name,
        // email : details.email,
        // password : details.password

        name: registerUser.name,
        surname: registerUser.surname,
        login: details.login,
        password: details.password,
        address: registerUser.address,
        email: registerUser.email,
        pesel: registerUser.pesel
      });

      setData({
        name: registerUser.name,
        surname: registerUser.surname,
        login: details.login,
        address: registerUser.address,
        email: registerUser.email,
        pesel: registerUser.pesel
      });
      
      navigate("/loggedIn");
    }
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
    //api.register(details.name, details.surname, details.gender, details.login, details.password, details.address, details.email, details.pesel, setError("success"), setError("Failure"));

    if(error == "success" || 1 == 1){
      setUser({
        // name: details.name,
        // email : details.email,
        // password : details.password

        login: details.login,
        name: details.name,
        surname: details.surname,
        password: details.password,
        address: details.address,
        email: details.email,
        pesel: details.pesel
      });
      setData({
        login: details.login,
        name: details.name,
        surname: details.surname,
        address: details.address,
        email: details.email,
        pesel: details.pesel
      });
      
      registerUser.login = details.login
      registerUser.name = details.name
      registerUser.surname = details.surname;
      registerUser.password = details.password;
      registerUser.address = details.address;
      registerUser.email = details.email;
      registerUser.pesel = details.pesel;

      console.log(registerUser)

      navigate("/loggedIn");
      console.log(details);
    }
  }

  const ChangePassword = details => {
      if(registerUser.password == details.oldPasswd){
        registerUser.password = details.newPasswd;

        setUser({
          ...user,
          password: details.newPasswd
        });

        setError("success")
      }
      else setError("error")
  }


  const BrowseCars = details => {
      //api.reservate(details.carId, setError("success"), setError("failure"), setError("auth_err"));

      if(details.carId != ""){
          setCar({
            carId: details.carId
          })
          setError("success")
      }
      else setError("failure")
  }

  const navigate = useNavigate();
  useEffect(() => {
    if(user.name == "") navigate("/")
  },[])

  return (
      
    <Routes>
        <Route path="/" element={
            <div>
              {() => setError("")}
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
                {() => setError("")}
                <h2>Welcome, <span>{user.name}</span></h2>

                <ul>
                  {/* <li><button name="rent-car" onClick={RentCar}>Rent a car</button></li> */}
                  <li><button name="browse-cars" onClick={() => navigate("/browse-cars")}>Browse available cars</button></li>
                  <li><button name="reserved-car">Reserved car</button></li>
                  <li><button name="persona-data" onClick={() => navigate("/userDescr")}>User Description</button></li>
                  <li><button name="change-passwd" onClick={() => navigate("/changePasswd")}>Change Password</button></li>
                  <li><button name="logout" onClick={Logout}>Logout</button></li>
                </ul>
              </div>
          }/>

          <Route path="/changePasswd" element={
              <div>
                  <div>
                    <ChangePasswordForm Password={ChangePassword} error={error}/>
                    <button name="index" onClick={() => navigate("/loggedIn")}>Return</button>
                  </div>
              </div>
          }/>
          
          <Route path="/userDescr" element={
              <div>
                <DescriptionTable data={data}/>
                <button name="index" onClick={() => navigate("/loggedIn")}>Return</button>
              </div>
          }/>

          <Route path="/browse-cars" element={
              <div>
                <NearestCarsForm data={data} Reserve={BrowseCars} error={error} />
                <button name="index" onClick={() => navigate("/loggedIn")}>Return</button>
              </div>
          }/>

      
    </Routes>
      
  );
}

export default App;