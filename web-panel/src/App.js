import React, {useState} from 'react' 
import API_Session from "./API_Connector";
import LoginForm from './components/LoginForm';

const api = new API_Session();


function App() {

  const adminUser = {
    email: "admin@admin.com",
    password: "admin123"
  }

  const [user, setUser] = useState({name: "", email: ""});
  const [error, setError] = useState("");

  // Login
  //Log out

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

    if(details.email == adminUser.email && details.password == adminUser.password){
      console.log("Logged in");
      setError("success");

      setUser({
        name: details.name,
        email : details.email,
        password : details.password
      });
  
    }
    else setError("invalid_data");
  }

  const Logout = () => {
    setUser({name: "", email: ""});
    setError("");
  }

  return (
    <div className="App">
        {(user.email != "") ? (
          <div className="welcome">
            <h2>Welcome, <span>{user.name}</span></h2>
            <button onClick={Logout}>Logout</button>
          </div>
        ): (
          <LoginForm Login={Login} error={error}/>
        )}
    </div>
  );
}

export default App;
