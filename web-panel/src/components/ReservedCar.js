import React, {useState} from "react";
import '../App.css'


function ReservedCar({Api, reservation, appManagment, children}){
    const [details, setDetails] = useState({resId: ""})
    const [error, setError] = useState()

    const submitHandler = e =>{
        e.preventDefault();
        console.log(reservation)
        console.log(reservation.reservation.carId)
        Api.endReservation(details.resId, deleteReservation,
        () => setError("Incorrect Data"), () => setError("Auth err"))
    }

    const deleteReservation = () =>{
        appManagment()
        setError("Success")
    }

    if(reservation == undefined) return(<div>Brak rezerwacji</div>)

    return(
            <div>
                <table>
                    <thead>
                        <tr>
                            <td>Res ID</td>
                            <td>car ID</td>
                            <td>Reservation Start</td>
                            <td>Reservation End</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                             <td>{reservation.reservation._id}</td> 
                        
                        
                            <td>{reservation.reservation.carId}</td>
                        
                        
                            <td>{reservation.reservation.reservationStart}</td>
                        
                            <td>{reservation.reservation.reservationsEnd}</td>

                        </tr>
                    </tbody>
                </table>

                <form onSubmit={submitHandler}>
                    <div className="form-inner">
                        <h2>Delete Reservation</h2>
                        {(error != "") ? (<div className="error">{error}</div>) : ""}
                        <div className="form-group">
                                <label htmlFor="text">res ID:</label>
                                <input type="text"  onChange={e => setDetails({...details, resId: e.target.value})} value={details.resId}/>
                        </div>
                        <input className="submitButton" type="submit" value="Delete" />
                    </div>
                </form>
            </div>
    );


}

export default ReservedCar;