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
                    <td>Email</td>
                    <td>Balance</td>
                    <td>Account Status</td>
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
                            {data.email}
                        </td>
                        <td>
                            {data.balance}
                        </td>
                        <td>
                            {data.status}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    )
}
