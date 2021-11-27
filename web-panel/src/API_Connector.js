


class Endpoints{
    static LOGIN_LOGIN = "login/login"
    static LOGIN_LOGOUT = "login/logout"
}

class API_Session{
    static GLOBAL_IP_ENDPOINT = "http://localhost:5000/";
    constructor() {
        this.SESSION_TOKEN = ""
    }
    async login(login, password, success, invalid_argument, authorization_failure){

        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.LOGIN_LOGIN, {
            body: JSON.stringify({login: login, password: password}),
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "ua"
            }
            else{
                return "er"
            }
        }).then(data => {
                console.log(data)
                if(data === "ua"){
                    authorization_failure()
                }
                else if(data === "er"){
                    invalid_argument()
                }
                else{
                    this.SESSION_TOKEN = data["token"]
                    success()
                }
            }
        ).catch((error)=>{
            console.log("Error")
            console.log(error)
        })
    }

    async logout(success, failure){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.LOGIN_LOGOUT, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            return response.ok ? response.json() : null
        }).then(data => {
                if(data == null){
                    failure()
                }
                else{
                    this.SESSION_TOKEN = ""
                    success()
                }
            }
        ).catch((error)=>{
            console.log("Error")
            console.log(error)
        })
    }


}

export default API_Session;
