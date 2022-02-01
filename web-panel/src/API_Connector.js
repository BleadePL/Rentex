import API_Connector from "./API_Connector";


class Endpoints{
    static LOGIN_LOGIN = "login/login"
    static LOGIN_LOGOUT = "login/logout"
    static LOGIN_REGISTER = "login/register"
    static LOGIN_SENDTOKEN = "login/sendtoken"
    static LOGIN_STATUS = "login/status"
    static LOGIN_ACTIVATE = "login/activate"
    static LOGIN_UPLOADPHOTOS = "login/uploadphotos"

    static USER_DETAILS = "user/details"
    static USER_CHANGEPASSWORD = "user/changepasswd"
    static USER_UPDATELOCATION = "user/updatelocation"
    static USER_HISTORY = "user/history"
    static USER_CARDS = "user/cards"
    static USER_CARD = "user/card/{0}"
    static USER_CARD_CHARGE = "user/card/{0}/charge"

    static BROWSE_NEARESTCARS = "browse/nearestcars"
    static BROWSE_NEARESTLOCATION = "browse/nearestlocations"
    static BROWSE_CAR = "browse/car/{0}"
    static BROWSE_LOCATION = "browse/location/{0}"

    static RENT_RESERVATION = "rent/reservation/{0}"
    static RENT_RESERVATE = "rent/reservate"
    static RENT_RENT = "rent/rent"
    static RENT_RENT_GET_DELETE = "rent/rent/{0}"

    static SERVICE = "service"
    static SERVICE_GET_DELETE = "service/{0}"
    static SERVICE_CAR = "service/car/{0}"


}

class API_Session{
    static GLOBAL_IP_ENDPOINT = "http://127.0.0.1:5000/";
    static ERROR_HANDLER = (error) => {
        console.log(error)
    }
    constructor() {
        this.SESSION_TOKEN = ""
    }
    /**
     * @param {string} login
     * @param {string} password
     * @param {function(): void} success
     * @param {function(): void} invalid_argument
     * @param {function(): void} authorization_failure
     */
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
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     * @param {function(): void} success
     * @param {function(): void} failure
     */
    async logout(success, failure){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.LOGIN_LOGOUT, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "ua"
            }
        }).then(data => {
                if(data === "ua"){
                    failure()
                }
                else{
                    this.SESSION_TOKEN = ""
                    success()
                }
            }
        ).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param name {string}
     * @param surname {string}
     * @param gender {string}
     * @param login {string}
     * @param password {string}
     * @param address {string}
     * @param email {string}
     * @param pesel {string}
     * @param success {function(string): void}
     * @param failure {function(string): void}
     * @returns {Promise<void>}
     */
    async register(name, surname, gender, login, password, address, email, pesel, success, failure){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.LOGIN_REGISTER, {
            body: JSON.stringify({name: name, surname: surname, gender: gender, login: login, password: password, address: address, email: email, pesel: pesel}),
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if(response.ok){
                return [200, response.json()]
            }
            else if(response.status === 400){
                return [400, response.json()]
            }

        }).then(data => {
                console.log(data)
                var s = data[0]
                if(s === 400){
                    failure(data[1]["error"])
                }
                else{
                    success(data[1]["userId"])
                }
            }
        ).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param success {function(): void}
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async sendToken(success, failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.LOGIN_SENDTOKEN, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                success()
            }
            else if(response.status === 401){
                auth_failed()
            }
            else{
                failure()
            }
        }).catch((error)=>{
            console.log("Error")
            console.log(error)
        })
    }

    /**
     *
     * @param success {function(string): void} ACTIVE - Aktywne konto, INACTIVE - nieaktwyne konto, DOCUMENTS - Brak dokumentow, PENDING - wyslano dokumenty, oczekiwanie na potwierdzenie, PAYMENT - Brak srodkow na koncie, ADMIN - administrator, LOCKED - konto zablokowane, DELETED - konto usuniete
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async status(success, failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.LOGIN_STATUS, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data["status"])
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param activation_token
     * @param success {function(): void}
     * @param failure {function(): void}
     * @returns {Promise<void>}
     */
    async activate(activation_token, success, failure){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.LOGIN_ACTIVATE + "?activation_token="+activation_token, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if(response.ok){
                success()
            }
            else{
                failure()
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param front
     * @param back
     * @param success {function(): void}
     * @param failure {function(): void}
     * @returns {Promise<*>}
     */
    // async uploadPhoto(front, back, success, failure){
    //     failure()
    //     return unimplemented
    // }

    /**
     *
     * @param success {function(json): void} USER Object
     * @param failure
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getUserDetails(success, failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.USER_DETAILS, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else {
                return "ERR"
            }

        }).then(data => {
            if(data === "ERR"){
                auth_failed()
            } else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param oldPass
     * @param newPass
     * @param success {function(): void}
     * @param failure
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async changeUserPassword(oldPass, newPass, success, failure, auth_failed){

    }

    /**
     *
     * @param locationLatitude
     * @param locationLongitude
     * @param success {function(): void}
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async updateLocation(locationLatitude, locationLongitude, success, failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.USER_UPDATELOCATION, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            },
            body: JSON.stringify({
                "locationLat": locationLatitude,
                "locationLong": locationLongitude
            })
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success()
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param pageIndex
     * @param pageLength
     * @param success {function(json): void} list of rentals
     * @param failure{function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async rentalHistory(pageIndex, pageLength, success, failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.USER_HISTORY, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data["rentals"])
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param success {function(json): void} list of cards
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getCards(success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.USER_CARDS, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data["cards"])
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param cardNumber
     * @param expirationDate
     * @param cardHolder
     * @param cvv
     * @param holderAddress
     * @param success {function(string): void} CARD ID
     * @param failure {function(string): void} AUTH_ERROR - blad autoryzacji karty, BLOCK_ERROR - blad przetwarzania transakcji, UNKNOWN - inny blad
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async addCard(cardNumber, expirationDate, cardHolder, cvv, holderAddress, success, failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.USER_CARDS, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            },
            body: JSON.stringify({
                "cardNumber": cardNumber,
                "expirationDate": expirationDate,
                "cardHolder": cardHolder,
                "cvv": cvv,
                "holderAddress": holderAddress
            })
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return response.json()
            }

        }).then(data => {
            if(data === "BR"){
                failure(data["error"])
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data["cardId"])
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param cardId
     * @param success {function(json): void} Card with details: lastdigits, expirations and holderName
     * @param failure {function(): void}
     * @param auth_failed
     * @returns {Promise<void>}
     */
    async getCard(cardId, success, failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.USER_CARD.replace("{0}", cardId), {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param cardId
     * @param success {function(): void}
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async deleteCard(cardId, success, failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.USER_CARD.replace("{0}", cardId), {
            method: "DELETE",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success()
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }


    /**
     *
     * @param cardId
     * @param amount
     * @param cvv
     * @param success {function(): void}
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async chargeCard(cardId, amount, cvv, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.USER_CARD_CHARGE.replace("{0}", cardId), {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            },
            body: JSON.stringify({
                "amount": amount,
                "cvv": cvv
            })
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success()
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }

    /**
     *
     * @param locationLat
     * @param locationLong
     * @param distance
     * @param success {function(json): void} list of cars
     * @param failure
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getNearestCars(locationLat, locationLong, distance, success, failure, auth_failed){
        console.log("Im here")
        await fetch(
            API_Session.GLOBAL_IP_ENDPOINT+Endpoints.BROWSE_NEARESTCARS + `?locationLat=${locationLat}&locationLong=${locationLong}`,
            {
                method: "GET",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Session-Token': this.SESSION_TOKEN
                }
            }
        )
        .then(response => {
            if(response.ok){
                console.log("XD")
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                console.log("BAD")
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data["cars"])
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }

    /**
     *
     * @param locationLat
     * @param locationLong
     * @param distance
     * @param success {function(json): void} List of locations
     * @param failure
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getNearestLocations(locationLat, locationLong, distance, success,failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.BROWSE_NEARESTLOCATION + `?locationLat=${locationLat}&locationLong=${locationLong}&distance=${distance}`,
            {
                method: "GET",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Session-Token': this.SESSION_TOKEN
                }
            })
            .then(response => {
                if(response.ok){
                    return response.json()
                }
                else if(response.status === 401){
                    return "AUTH"
                }
                else{
                    return "BR"
                }

            }).then(data => {
                if(data === "BR"){
                    failure()
                }
                else if(data === "AUTH"){
                    auth_failed()
                }else{
                    success(data["locations"])
                }

            }).catch((error)=>{
                API_Connector.ERROR_HANDLER(error)
            })
    }

    /**
     *
     * @param carId
     * @param success {function(json): void} Car
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async browseCar(carId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.BROWSE_CAR.replace("{0}", carId), {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param locationId
     * @param success {function(json): void} Location
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async browseLocation(locationId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.BROWSE_LOCATION.replace("{0}", locationId), {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }


    /**
     *
     * @param resId reservation Id
     * @param success {function(json): void} Reservation object
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getReservation(resId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.RENT_RESERVATION.replace("{0}", resId), {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }

    /**
     *
     * @param resId reservation Id
     * @param success {function(): void}
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async endReservation(resId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.RENT_RESERVATION.replace("{0}", resId), {
            method: "DELETE",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success()
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }



    /**
     *
     * @param carId
     * @param success {function(string): void} Reservation ID
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async reservate(carId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.RENT_RESERVATE, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            },
            body: JSON.stringify({"carId": carId})
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data["resId"])
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }


    /**
     *
     * @param success {function(string): void} Reservation ID
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getUserReservation(success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.RENT_RESERVATE, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }

    /**
     *
     * @param carId
     * @param cvv
     * @param paymentType PP or ID of creditcard
     * @param success {function(string): void} Rental ID
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async rent(carId, cvv, paymentType, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.RENT_RENT, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            },
            body: JSON.stringify({"carId": carId, "cvv":cvv, "paymentType": paymentType})
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param success {function(string): void} Reservation ID
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getUserRental(success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.RENT_RENT, {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }


    /**
     *
     * @param rentId reservation Id
     * @param success {function(json): void} Reservation object
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getRental(rentId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.RENT_RENT_GET_DELETE.replace("{0}", rentId), {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }

    /**
     *
     * @param rentalId reservation Id
     * @param success {function(): void}
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async endRental(rentalId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.RENT_RENT_GET_DELETE.replace("{0}", rentalId), {
            method: "DELETE",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success()
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })

    }

    /**
     *
     * @param carId
     * @param success {function(string): void} Service ID
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async service(carId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.SERVICE, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            },
            body: JSON.stringify({"carId": carId})
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data["serviceId"])
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param serviceId
     * @param success {function(json): void} Service object
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getService(serviceId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.SERVICE_GET_DELETE.replace("{0}", serviceId), {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data)
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }

    /**
     *
     * @param serviceId Service ID
     * @param success {function(): void}
     * @param failure {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async endService(serviceId, success, failure, auth_failed)
    {
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.SERVICE_GET_DELETE.replace("{0}", serviceId), {
            method: "DELETE",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success()
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }


    async getServiceByCar(carId, success, failure, auth_failed){
        await fetch(API_Session.GLOBAL_IP_ENDPOINT+Endpoints.SERVICE_CAR.replace("{0}", carId), {
            method: "GET",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Session-Token': this.SESSION_TOKEN
            }
        }).then(response => {
            if(response.ok){
                return response.json()
            }
            else if(response.status === 401){
                return "AUTH"
            }
            else{
                return "BR"
            }

        }).then(data => {
            if(data === "BR"){
                failure()
            }
            else if(data === "AUTH"){
                auth_failed()
            }else{
                success(data["services"])
            }

        }).catch((error)=>{
            API_Connector.ERROR_HANDLER(error)
        })
    }
}

export default API_Session;
