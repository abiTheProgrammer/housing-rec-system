import "./UserInputs.css";

function UserInputs() {
  return (
    <>
      <div className="input-group mb-3" style={{ marginTop: "60px" }}>
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Annual Income"
          aria-label="Annual Income"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
        />
      </div>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Monthly Expenditure"
          aria-label="Monthly Expenditure"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
        />
      </div>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Best Credit Score"
          aria-label="Best Credit Score"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
        />
      </div>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Available Savings"
          aria-label="Available Savings"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
        />
      </div>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Location to Buy House"
          aria-label="Location to Buy House"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
        />
      </div>
    </>
  );
}

export default UserInputs;
