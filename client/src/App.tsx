import "./App.css";
import UserInputs from "./components/first-page/UserInputs";

function App() {
  return (
    <div style={{ backgroundColor: "pink" }}>
      <div className="heading">
        <h1>Housing Recommendation System</h1>
      </div>
      <div className="first-page">
        <UserInputs />
      </div>
    </div>
  );
}

export default App;
