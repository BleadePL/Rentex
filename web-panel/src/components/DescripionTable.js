import React, {useState} from "react";
import '../App.css'

export default function DescriptionTable({data, children}){
    return(
        <div>
            <table>
                <thead>
                    <tr>
                    <td>Name</td>
                    <td>Surname</td>
                    <td>Login</td>
                    <td>Address</td>
                    <td>Email</td>
                    <td>Pesel</td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            {data.name}
                        </td>
                        <td>
                            {data.surname}
                        </td>
                        <td>
                            {data.login}
                        </td>
                        <td>
                            {data.address}
                        </td>
                        <td>
                            {data.email}
                        </td>
                        <td>
                            {data.pesel}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    )
}
