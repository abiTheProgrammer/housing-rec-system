import { useState } from "react";
import "./UserInputs.css";

interface UserInputsProps {
  onSearchSubmit: () => void;
}

function UserInputs({ onSearchSubmit }: UserInputsProps) {
  const [formData, setFormData] = useState({
    "Annual Income": "",
    "Monthly Expenditure": "",
    "Credit Score": "",
    "Available Savings": "",
    "Monthly Down Payment": "",
  });

  const [errors, setErrors] = useState({
    "Annual Income": "",
    "Monthly Expenditure": "",
    "Credit Score": "",
    "Available Savings": "",
    "Monthly Down Payment": "",
  });

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e: any) => {
    e.preventDefault();
    const validationErrors = {
      "Annual Income": "",
      "Monthly Expenditure": "",
      "Credit Score": "",
      "Available Savings": "",
      "Monthly Down Payment": "",
    };
    // Input Validation Ranges

    // annual income range ($20,000 - $3 bil)
    // monthly expenditure range ($1,000 - $5 mil)
    // credit score range (0 - 800)
    // available savings range ($0 - $50 bil)
    // monthly downpayment range ($0 - $300 mil)

    if (!formData["Annual Income"].trim()) {
      validationErrors["Annual Income"] = "Annual Income invalid";
    }
    if (!formData["Monthly Expenditure"].trim()) {
      validationErrors["Monthly Expenditure"] = "Monthly Expenditure invalid";
    }
    if (!formData["Credit Score"].trim()) {
      validationErrors["Credit Score"] = "Credit Score invalid";
    }
    if (!formData["Available Savings"].trim()) {
      validationErrors["Available Savings"] = "Available Savings invalid";
    }
    if (!formData["Monthly Down Payment"].trim()) {
      validationErrors["Monthly Down Payment"] = "Monthly Down Payment invalid";
    }

    setErrors(validationErrors);
    if (
      Object.values(validationErrors).every(
        (value) => value === Object.values(validationErrors)[0]
      )
    ) {
      onSearchSubmit();
    }
  };
  // Change font, style, layout of error message in <span>
  return (
    <form onSubmit={handleSubmit}>
      <div className="input-group mb-3" style={{ marginTop: "60px" }}>
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Annual Income"
          aria-label="Annual Income"
          name="Annual Income"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
        />
        {errors["Annual Income"] && <span>{errors["Annual Income"]}</span>}
      </div>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Monthly Expenditure"
          aria-label="Monthly Expenditure"
          name="Monthly Expenditure"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
        />
        {errors["Monthly Expenditure"] && (
          <span>{errors["Monthly Expenditure"]}</span>
        )}
      </div>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Credit Score"
          aria-label="Credit Score"
          name="Credit Score"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
        />
        {errors["Credit Score"] && <span>{errors["Credit Score"]}</span>}
      </div>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Available Savings"
          aria-label="Available Savings"
          name="Available Savings"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
        />
        {errors["Available Savings"] && (
          <span>{errors["Available Savings"]}</span>
        )}
      </div>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Monthly Down Payment"
          aria-label="Monthly Down Payment"
          name="Monthly Down Payment"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
        />
        {errors["Monthly Down Payment"] && (
          <span>{errors["Monthly Down Payment"]}</span>
        )}
      </div>
      <button
        type="submit"
        id="first-to-second-page-button"
        className="btn btn-outline-primary"
      >
        Search Houses
      </button>
    </form>
  );
}

export default UserInputs;
