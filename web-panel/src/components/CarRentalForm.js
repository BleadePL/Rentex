import React, {useState} from "react";
import '../App.css'


export default function RentCar({Api, reservation, flowData, endRentalData, actRented}){

    //rent(carId, cvv, paymentType, success, failure, auth_failed)
    //endRental(rentalId, success, failure, auth_failed)
    const [rentalDetails, setRentalDetails] = useState({carId : "", cvv: "", paymentType: ""});
    const [error, setError] = useState();



    const RentalCar = (details) => {
        console.log(details)
        setError("Success")
        flowData(details)
    }

    const submitHandler = e =>{
        e.preventDefault();
        console.log(rentalDetails)
        //Api.rent(rentalDetails.carId, rentalDetails.cvv, rentalDetails.paymentType, RentalCar, setError, setError)
    }

    const endRental = () =>{
        setError("Success")
        endRentalData(rentalDetails)
    }

    const buttonHandler = e =>{
        // e.preventDefault();
        // Api.endRental(actRented)
    }

    if(reservation == undefined) return (<div>No reservation, nothing to rent</div>)

    return(

        <div>
                <form onSubmit={submitHandler}>
                    <div className="form-inner">
                        <h2>Rent a car</h2>
                        {(error != "") ? (<div className="error">{error}</div>) : ""}
                        <div className="form-group">
                                <label htmlFor="text">car ID: </label>
                                <input type="text"  onChange={e => setRentalDetails({...rentalDetails, carId: e.target.value})} value={rentalDetails.carId}/>
                        </div>
                        
                        <div className="form-group">
                                <label htmlFor="text">cvv on card: </label>
                                <input type="text"  onChange={e => setRentalDetails({...rentalDetails, cvv: e.target.value})} value={rentalDetails.cvv}/>
                        </div>

                        <div className="form-group">
                                <label htmlFor="text">payment type: </label>
                                <input type="text"  onChange={e => setRentalDetails({...rentalDetails, paymentType: e.target.value})} value={rentalDetails.paymentType}/>
                        </div>


                        <input className="submitButton" type="submit" value="Rent" />
                    </div>
                </form>

                {actRented == undefined ? " " :
                    <button onClick={buttonHandler}>End Rental</button>
                }

        </div>

    );



}