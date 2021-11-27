import logo from './logo.svg';
import './App.css';
import API_Session from "./API_Connector";

const api = new API_Session();

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
          <button onClick={async () => api.login("test", "test", ()=>console.log("Success"), ()=>console.log("Invalid Arguemnt"), () => console.log("Authorisation failed"))}>LOGIN</button>
          <button onClick={async () => api.logout( ()=>console.log("Success"), ()=>console.log("Failed"))}>LOGOUT</button>
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
