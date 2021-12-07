import React, {useState} from "react";
import '../App.css'


export default function NearestCarsForm({data, Reserve, cars, api, children}){    
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
