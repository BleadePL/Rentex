import React, {useState} from "react";
import '../App.css'

function LoginForm({Login, api}){
    const [details, setDetails] = useState({login: "", password: ""});
    const [error, setError] = useState()

    const submitHandler = e =>{
        e.preventDefault();

        api.login(details.login, details.password, sendData, () => setError("invalid_argument"), () => setError("authorization_failure"));
    }
    
    const sendData = () => {
        Login(details)
    }

    return (
        <form onSubmit={submitHandler}>
            <div className="form-inner">
                <h2>Login IN</h2>
                {(error != "") ? (<div className="error">{error}</div>) : ""}
                <div className="form-group">
                        <label htmlFor="login">Login:</label>
                        <input type="text" name="login" id="login" onChange={e => setDetails({...details, login: e.target.value})} value={details.login}/>
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password: </label>
                    <input type="password" name="password" id="password" onChange={e => setDetails({...details, password: e.target.value})} value={details.password}/>
                </div>
                <input className="submitButton" type="submit" value="Sign UP" />
            </div>
        </form>
    )
}


export default LoginForm;