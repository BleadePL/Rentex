import React, {useState} from "react";
import '../App.css'




export default function NearestCarsForm({data, Reserve, cars, api, children}){
    //     var carsy = [{"carId": 48530713, "brand": "Toyota","regNumber": "DW112233","model": "Yaris 1.0","seats": 5,"charge": 100, "activationCost": "10.30",
    //     "timeCost": "0.30","locationLat": "51.235123","locationLong": "16.50312","status": "ACTIVE"},
    
    //     {"carId": 321530713, "brand": "ESSA","regNumber": "DW112233","model": "Yaris 1123.0","seats": 5,"charge": 100, "activationCost": "10.30",
    //     "timeCost": "0.30","locationLat": "51.235123","locationLong": "16.50312","status": "ACTIVE"},
    
    //     {"carId": 12412330713, "brand": "Toyota","regNumber": "DW112233","model": "Yaris 1.0","seats": 5,"charge": 100, "activationCost": "10.30",
    //     "timeCost": "0.30","locationLat": "51.235123","locationLong": "16.50312","status": "ACTIVE"}
    // ];
    
    
    console.log(cars)
    
    const [state, setState] = React.useState(cars);
    const [details, setDetails] = useState({carId: ""});
    const [error, setError] = useState()
    
    
    const ReserveCar = (resId) =>{
        setError("Success")
        Reserve(details, resId)
    }
    
    
    const submitHandler = e =>{
        e.preventDefault();
        api.reservate(details.carId, ReserveCar, () => setError("invalid_argument"), () => setError("Has reservation"))
    }

    if(cars == undefined) return(<div/>)

    return(
            <div>

                <table>
                    <tr key={"header"}>
                        {Object.keys(state[0]).map((key) => (
                        <th>{key}</th>
                        ))}
                    </tr>
                    {state.map((item) => (
                        <tr key={item.id}>
                        {Object.values(item).map((val) => (
                            <td>{val}</td>
                        ))}
                        </tr>
                    ))}
                </table>
                
                <form onSubmit={submitHandler}>
                    <div className="form-inner">
                        <h2>Pick a car by it's id</h2>
                        {(error != "") ? (<div className="error">{error}</div>): ""}
                        <div>
                            <label htmlFor="text">Car ID: </label>
                            <input type="text" onChange={e => setDetails({...details, carId: e.target.value})} value={details.carId}/>
                        </div>
                        <input className="submitButton" type="submit" value="Reserve" />
                    </div>
                </form>

            </div>
    );
}
