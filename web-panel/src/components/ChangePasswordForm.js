import React, {useState} from "react";
import '../App.css'

function ChangePasswordForm({Password, error}){
    const [details, setDetails] = useState({oldPasswd: "", newPasswd: ""});

    const submitHandler = e =>{
        e.preventDefault();

        Password(details)
    }
    
    return (
        <form onSubmit={submitHandler}>
            <div className="form-inner">
                <h2>Change Password</h2>
                {(error != "") ? (<div className="error">{error}</div>) : ""}
                <div className="form-group">
                        <label htmlFor="password">Old Password: </label>
                        <input type="password" name="oldPassword" id="oldPassword" onChange={e => setDetails({...details, oldPasswd: e.target.value})} value={details.oldPasswd}/>
                </div>
                <div className="form-group">
                    <label htmlFor="password">New Password: </label>
                    <input type="password" name="newPassword" id="newPassword" onChange={e => setDetails({...details, newPasswd: e.target.value})} value={details.newPasswd}/>
                </div>
                <input className="submitButton" type="submit" value="Submit" />
            </div>
        </form>
    )
}


export default ChangePasswordForm;