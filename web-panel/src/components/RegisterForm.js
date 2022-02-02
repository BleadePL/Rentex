import React, {useState} from "react";
import '../App.css'

function RegisterForm({api, Register}){
    const [details, setDetails] = useState({name: "", surname: "", login: "", password: "", email: "", pesel: ""});
    const [error, setError] = useState()


    const submitHandler = e =>{
        e.preventDefault();
        api.register(details.name, details.surname, details.gender, details.login, details.password, details.address, details.email, details.pesel,
            () => setError("Success"), () => setError("Auth err"))
        }
    
    return (
        <form onSubmit={submitHandler}>
            <div className="form-inner">
                <h2>Register</h2>
                {(error != "") ? (<div className="errorRegister">{error}</div>) : ""}
                <div className="form-group">
                        <label htmlFor="name">Name: </label>
                        <input type="text" name="name" id="name" onChange={e => setDetails({...details, name: e.target.value})} value={details.name}/>
                </div>

                <div className="form-group">
                        <label htmlFor="name">Surname: </label>
                        <input type="text" name="surname" id="surname" onChange={e => setDetails({...details, surname: e.target.value})} value={details.surname}/>
                </div>

                <div className="form-group">
                        <label htmlFor="name">Login: </label>
                        <input type="text" name="login" id="login" onChange={e => setDetails({...details, login: e.target.value})} value={details.login}/>
                </div>

                <div className="form-group">
                    <label htmlFor="password">Password: </label>
                    <input type="password" name="password" id="password" onChange={e => setDetails({...details, password: e.target.value})} value={details.password}/>
                </div>
                <div className="form-group">
                    <label htmlFor="password">Gender: </label>
                    <input type="password" name="password" id="password" onChange={e => setDetails({...details, gender: e.target.value})} value={details.gender}/>
                </div>
                <div className="form-group">
                    <label htmlFor="email">Email: </label>
                    <input type="email" name="email" id="email" onChange={e => setDetails({...details, email: e.target.value})} value={details.email}/>
                </div>

                <div className="form-group">
                        <label htmlFor="name">Pesel: </label>
                        <input type="text" name="pesel" id="pesel" onChange={e => setDetails({...details, pesel: e.target.value})} value={details.pesel}/>
                </div>

                <input className="submitButton" type="submit" value="Sign IN" />
            </div>
        </form>
    )
}


export default RegisterForm;