import React, {useState} from "react";
import '../App.css'


var carsD

const LoadCars = (data) => {
    carsD = data
}

export default function NearestCarsForm({data, Reserve, error, api}){
    var cars = [{"carId": 48530713, "brand": "Toyota","regNumber": "DW112233","model": "Yaris 1.0","seats": 5,"charge": 100, "activationCost": "10.30",
                "timeCost": "0.30","locationLat": "51.235123","locationLong": "16.50312","status": "ACTIVE"},

                {"carId": 321530713, "brand": "ESSA","regNumber": "DW112233","model": "Yaris 1123.0","seats": 5,"charge": 100, "activationCost": "10.30",
                "timeCost": "0.30","locationLat": "51.235123","locationLong": "16.50312","status": "ACTIVE"},

                {"carId": 12412330713, "brand": "Toyota","regNumber": "DW112233","model": "Yaris 1.0","seats": 5,"charge": 100, "activationCost": "10.30",
                "timeCost": "0.30","locationLat": "51.235123","locationLong": "16.50312","status": "ACTIVE"}
                ];


    
    api.getNearestCars("51.1", "17.1", LoadCars, 1000, () => console.log(), () => console.log());

    console.log(carsD)

    
    const [state, setState] = React.useState(cars);

    const [details, setDetails] = useState({carId: ""});

    


    const submitHandler = e =>{
        e.preventDefault();

        Reserve(details)
    }

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
