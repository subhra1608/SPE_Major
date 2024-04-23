import React, { useState } from 'react';
import axios from 'axios'; // Import Axios for making HTTP requests
import './App.css'; // Import CSS file for styling
import swal from 'sweetalert'; // Import SweetAlert
import Swal from 'sweetalert2';


const App = () => {
    // State variables to hold input values and prediction result
    const [formData, setFormData] = useState({
        'worst concave points': '',
        'mean concave points': '',
        'worst radius': '',
        'worst perimeter': '',
        'mean concavity': ''
    });

    // Function to handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Make a POST request to the prediction endpoint
            const response = await axios.post('http://localhost:5000/predict', formData, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            });
            // Display prediction as styled alert using SweetAlert
            Swal.fire({
                title: "Prediction Result",
                text: response.data.prediction_text,
                icon: "success",
                confirmButtonText: "OK",
                customClass: {
                    confirmButton: 'sweet-alert-custom-style'
                }
            });
        } catch (error) {
            console.error('Error:', error);
        }
    };

    // Function to handle input changes
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    return (
        <div className="container">
            <div className="centered-content">
                <h1>Breast Cancer Prediction</h1>
                <h3>If the output turns out to be 1 then the cancer is probably Malignant else it's Benign!</h3>
                <form onSubmit={handleSubmit} className="form">
                    <div className="form-group">
                        <label htmlFor="worst_concave_points">Worst Concave Points:</label>
                        <input type="text" name="worst concave points" placeholder="Enter the Worst Concave Points" value={formData['worst concave points']} onChange={handleChange} />
                    </div>

                    <div className="form-group">
                        <label htmlFor="mean_concave_points">Mean Concave Points:</label>
                        <input type="text" name="mean concave points" placeholder="Enter the Mean Concave Points" value={formData['mean concave points']} onChange={handleChange} />
                    </div>

                    <div className="form-group">
                        <label htmlFor="worst_radius">Worst Radius:</label>
                        <input type="text" name="worst radius" placeholder="Enter the Worst Radius" value={formData['worst radius']} onChange={handleChange} />
                    </div>

                    <div className="form-group">
                        <label htmlFor="worst_perimeter">Worst Perimeter:</label>
                        <input type="text" name="worst perimeter" placeholder="Enter the Worst Perimeter" value={formData['worst perimeter']} onChange={handleChange} />
                    </div>

                    <div className="form-group">
                        <label htmlFor="mean_concavity">Mean Concavity:</label>
                        <input type="text" name="mean concavity" placeholder="Enter the Mean Concavity" value={formData['mean concavity']} onChange={handleChange} />
                    </div>
                    <div className="submitButton">
                        <input type="submit" value="Click here to Predict" />
                    </div>
                </form>
            </div>
        </div>
    );
};

export default App;
