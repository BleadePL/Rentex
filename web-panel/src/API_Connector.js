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
    static GLOBAL_IP_ENDPOINT = "http://localhost:5000/";
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
     * @param failed {function(string): void}
     * @returns {Promise<void>}
     */
    async register(name, surname, gender, login, password, address, email, pesel, success, failed){
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
                    failed(data[1]["error"])
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
     * @param failed {function(): void}
     * @returns {Promise<void>}
     */
    async activate(activation_token, success, failed){
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
                failed()
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
     * @param failed {function(): void}
     * @returns {Promise<*>}
     */
    // async uploadPhoto(front, back, success, failed){
    //     failed()
    //     return unimplemented
    // }

    /**
     *
     * @param success {function(json): void} USER Object
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getUserDetails(success, auth_failed){

    }

    /**
     *
     * @param oldPass
     * @param newPass
     * @param success {function(): void}
     * @param failed {function(string): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async changeUserPassword(oldPass, newPass, success, failed, auth_failed){

    }

    /**
     *
     * @param locationLatitude
     * @param locationLongitude
     * @param success {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async updateLocation(locationLatitude, locationLongitude, success, auth_failed){

    }

    /**
     *
     * @param pageIndex
     * @param pageLength
     * @param success {function(json): void} list of rentals
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async rentalHistory(pageIndex, pageLength, success, auth_failed){

    }

    /**
     *
     * @param success {function(json): void} list of cards
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getCards(success, auth_failed)
    {

    }

    /**
     *
     * @param cardNumber
     * @param expirationDate
     * @param cardHolder
     * @param cvv
     * @param holderAddress
     * @param success {function(string): void} CARD ID
     * @param failed {function(): void} AUTH_ERROR - blad autoryzacji karty, BLOCK_ERROR - blad przetwarzania transakcji, UNKNOWN - inny blad
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async addCard(cardNumber, expirationDate, cardHolder, cvv, holderAddress, success, failed, auth_failed){

    }

    /**
     *
     * @param cardId
     * @param success {function(json): void} Card with details: lastdigits, expirations and holderName
     * @param failed {function(): void}
     * @param auth_failed
     * @returns {Promise<void>}
     */
    async getCard(cardId, success, failed, auth_failed){

    }

    /**
     *
     * @param cardId
     * @param success {function(): void}
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async deleteCard(cardId, success, failed, auth_failed){

    }

    /**
     *
     * @param cardId
     * @param success {function(): void}
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async chargeCard(cardId, success, failed, auth_failed)
    {

    }

    /**
     *
     * @param locationLat
     * @param locationLong
     * @param distance
     * @param success {function(json): void} list of cars
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getNearestCars(locationLat, locationLong, distance, success, auth_failed){

    }

    /**
     *
     * @param locationLat
     * @param locationLong
     * @param distance
     * @param success {function(json): void} List of locations
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getNearestLocations(locationLat, locationLong, distance, success, auth_failed){

    }

    /**
     *
     * @param carId
     * @param success {function(json): void} Car
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async browseCar(carId, success, failed, auth_failed)
    {

    }

    /**
     *
     * @param locationId
     * @param success {function(json): void} Location
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async browseLocation(locationId, success, failed, auth_failed)
    {

    }


    /**
     *
     * @param resId reservation Id
     * @param success {function(json): void} Reservation object
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getReservation(resId, success, failed, auth_failed)
    {

    }

    /**
     *
     * @param resId reservation Id
     * @param success {function(): void}
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async endReservation(resId, success, failed, auth_failed)
    {

    }



    /**
     *
     * @param carId
     * @param success {function(string): void} Reservation ID
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async reservate(carId, success, failed, auth_failed)
    {

    }

    /**
     *
     * @param carId
     * @param cvv
     * @param paymentType PP or ID of creditcard
     * @param success {function(string): void} Rental ID
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async rent(carId, cvv, paymentType, success, failed, auth_failed)
    {

    }

    /**
     *
     * @param rentalId
     * @param success {function(json): void} Rental object
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getRental(rentalId, success, failed, auth_failed)
    {

    }

    /**
     *
     * @param rentalId Rental ID
     * @param success {function(): void}
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async endRental(rentalId, success, failed, auth_failed)
    {

    }

    /**
     *
     * @param carId
     * @param success {function(string): void} Service ID
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async service(carId, success, failed, auth_failed)
    {

    }

    /**
     *
     * @param serviceId
     * @param success {function(json): void} Service object
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async getService(serviceId, success, failed, auth_failed)
    {

    }

    /**
     *
     * @param serviceId Service ID
     * @param success {function(): void}
     * @param failed {function(): void}
     * @param auth_failed {function(): void}
     * @returns {Promise<void>}
     */
    async endService(serviceId, success, failed, auth_failed)
    {

    }
}

export default API_Session;
