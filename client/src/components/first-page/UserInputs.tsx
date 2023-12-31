import { useEffect, useState } from "react";
import axios from "axios";
import "./UserInputs.css";
import URL from "./BackendPort";

interface UserInputsProps {
  onSearchSubmit: () => void;
}

function UserInputs({ onSearchSubmit }: UserInputsProps) {
  const initialFormData = {
    "Annual Income": "",
    "Monthly Expenditure": "",
    "Credit Score": "",
    "Available Savings": "",
    "Monthly Down Payment": "",
  };

  const [formData, setFormData] = useState(() => {
    const savedFormData = localStorage.getItem("userInputsFormData");
    return savedFormData ? JSON.parse(savedFormData) : initialFormData;
  });

  useEffect(() => {
    // Add an event listener to clear localStorage on page refresh
    const handleBeforeUnload = () => {
      localStorage.removeItem("userInputsFormData");
    };
    window.addEventListener("beforeunload", handleBeforeUnload);

    // Clean up the event listener when the component unmounts
    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, []);

  const [errors, setErrors] = useState(initialFormData);

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e: any) => {
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

    const validNumberInRange = (value: any, min: number, max: number) => {
      const numericValue = Number(value);
      return !isNaN(numericValue) && numericValue >= min && numericValue <= max;
    };

    if (
      !formData["Annual Income"].trim() ||
      !validNumberInRange(formData["Annual Income"], 20000, 3000000000)
    ) {
      validationErrors["Annual Income"] =
        "Annual Income Range [$20,000 - $3 Bil]";
    }
    if (
      !formData["Monthly Expenditure"].trim() ||
      !validNumberInRange(formData["Monthly Expenditure"], 1000, 5000000)
    ) {
      validationErrors["Monthly Expenditure"] =
        "Monthly Expenditure Range [$1,000 - $5 Mil]";
    }
    if (
      !formData["Credit Score"].trim() ||
      !validNumberInRange(formData["Credit Score"], 0, 800)
    ) {
      validationErrors["Credit Score"] = "Credit Score Range [0 - 800]";
    }
    if (
      !formData["Available Savings"].trim() ||
      !validNumberInRange(formData["Available Savings"], 0, 50000000000)
    ) {
      validationErrors["Available Savings"] =
        "Available Savings Range [$0 - $50 Bil]";
    }
    if (
      !formData["Monthly Down Payment"].trim() ||
      !validNumberInRange(formData["Monthly Down Payment"], 0, 300000000)
    ) {
      validationErrors["Monthly Down Payment"] =
        "Monthly Down Payment Range [$0 - $300 Mil]";
    }

    setErrors(validationErrors);
    if (
      Object.values(validationErrors).every(
        (value) => value === Object.values(validationErrors)[0]
      )
    ) {
      try {
        const response = await axios.put(URL.REACT_APP_BACKEND_URL, formData);
        console.log("PUT request response:", response.data);
        localStorage.setItem("userInputsFormData", JSON.stringify(formData));
        onSearchSubmit();
      } catch (error: any) {
        console.error("PUT request error:", error);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="input-group mb-3" style={{ marginTop: "80px" }}>
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Annual Income"
          aria-label="Annual Income"
          name="Annual Income"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
          value={formData["Annual Income"]}
        />
      </div>
      {errors["Annual Income"] && (
        <span className="error-message">{errors["Annual Income"]}</span>
      )}
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Monthly Expenditure"
          aria-label="Monthly Expenditure"
          name="Monthly Expenditure"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
          value={formData["Monthly Expenditure"]}
        />
      </div>
      {errors["Monthly Expenditure"] && (
        <span className="error-message">{errors["Monthly Expenditure"]}</span>
      )}
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Credit Score"
          aria-label="Credit Score"
          name="Credit Score"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
          value={formData["Credit Score"]}
        />
      </div>
      {errors["Credit Score"] && (
        <span className="error-message">{errors["Credit Score"]}</span>
      )}
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Available Savings"
          aria-label="Available Savings"
          name="Available Savings"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
          value={formData["Available Savings"]}
        />
      </div>
      {errors["Available Savings"] && (
        <span className="error-message">{errors["Available Savings"]}</span>
      )}
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control custom-width mx-auto"
          placeholder="Monthly Down Payment"
          aria-label="Monthly Down Payment"
          name="Monthly Down Payment"
          style={{ backgroundColor: "rgb(216, 227, 184)" }}
          onChange={handleChange}
          value={formData["Monthly Down Payment"]}
        />
      </div>
      {errors["Monthly Down Payment"] && (
        <span className="error-message">{errors["Monthly Down Payment"]}</span>
      )}
      <button
        type="submit"
        id="first-to-second-page-button"
        className="btn btn-outline-primary"
      >
        Search Houses
      </button>
      <div className="padding" />
    </form>
  );
}

export default UserInputs;
