import { useState } from "react";

import "./App.css";
import UserInputs from "./components/first-page/UserInputs";
import HousingRecs from "./components/second-page/HousingRecs";

function App() {
  const [currentPage, setCurrentPage] = useState<"user" | "recs" | "details">(
    "user"
  );

  const handlePageChange = (page: "user" | "recs" | "details") => {
    setCurrentPage(page);
  };

  const UserPage = () => {
    return (
      <div className="first-page">
        <div className="user-inputs">
          <UserInputs onSearchSubmit={() => handlePageChange("recs")} />
        </div>
      </div>
    );
  };

  const RecsPage = () => {
    return (
      <div className="second-page">
        <button
          type="button"
          id="second-to-first-page-button"
          className="btn btn-outline-primary"
          onClick={() => handlePageChange("user")}
        >
          Go Back
        </button>
        <div className="housing-recs">
          <HousingRecs />
        </div>
      </div>
    );
  };

  const DetailsPage = () => {
    return <div>Details of Houses Page called from App</div>;
  };

  return (
    <div style={{ backgroundColor: "pink" }}>
      <div className="heading">
        <h1>Housing Recommendation System</h1>
      </div>
      {currentPage === "user" && <UserPage />}
      {currentPage === "recs" && <RecsPage />}
      {currentPage === "details" && <DetailsPage />}
    </div>
  );
}

export default App;
