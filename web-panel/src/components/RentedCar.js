import React, {useState} from "react";
import '../App.css'


function RentedCar({Api, rental, appManagment, children}){
    
    console.log()
    const [details, setDetails] = useState({rental_id: ""})
    const [error, setError] = useState()

    const submitHandler = e =>{
        e.preventDefault();
        Api.endRental(details.rental_id, deleterental,
            () => setError("Incorrect Data"), () => setError("Auth err"))
        }
        
        const deleterental = () =>{
            appManagment()
            setError("Success")
        }
    if (rental != undefined){
        rental = rental.rental}

    if(rental == undefined) return(<div>Brak wypozyczenia</div>)

    return(
            <div>
                <table>
                    <thead>
                        <tr>
                            <td>Res ID</td>
                            <td>car ID</td>
                            <td>rental Start</td>
                            <td>rental End</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                             <td>{rental._id}</td> 
                            <td>{rental.carId}</td>
                            <td>{rental.rentalStart}</td>
                        </tr>
                    </tbody>
                </table>

                <form onSubmit={submitHandler}>
                    <div className="form-inner">
                        <h2>Delete rental</h2>
                        {(error != "") ? (<div className="error">{error}</div>) : ""}
                        <div className="form-group">
                                <label htmlFor="text">rental ID:</label>
                                <input type="text"  onChange={e =>
                                     setDetails({...details, rental_id: e.target.value})} value={details.rental_id}/>
                        </div>
                        <input className="submitButton" type="submit" value="Delete" />
                    </div>
                </form>
            </div>
    );


}

export default RentedCar;