import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';
import './AddBasicInfo.css';

const AddBasicInfo = () => {
  const [page, setPage] = useState(1);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    father_name: '',
    location: '',
    gender: '',
    marital_status: '',
    date_of_birth: '',
    mobile_phone: '',
    landline_phone: '',
    email: '',
    tax_id: '',
    address: '',
    department: '',
    responsibilities: '',
    specialization: '',
    degree_available: null, // File input
    salary: '',
    iban: '',
    hiring_date: '',
    employee_status: '',
    termination_date: '',
    medical_exams: '',
    medical_exams_date: '',
    medical_exams_renewal_date: '',
    safety_passport: '',
    safety_passport_date: '',
    safety_passport_renewal_date: '',
    certifications_seminars: '',
  });

  const [isFormValid, setIsFormValid] = useState(false);

  // Required fields
  const requiredFields = useMemo(() => [
    'first_name', 'last_name', 'father_name', 'location', 'gender', 'marital_status',
  ], []);

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value, type, files } = e.target;

    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'file' ? files[0] : value, // Handle file input
    }));
  };

  // Validate required fields
  const validateForm = useCallback(() => {
    const allRequiredFieldsFilled = requiredFields.every(field => formData[field]?.trim() !== '');
    setIsFormValid(allRequiredFieldsFilled);
  }, [formData, requiredFields]);

  useEffect(() => {
    validateForm();
  }, [formData, validateForm]);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form Data before submitting:', formData);

    const missingFields = requiredFields.filter(field => !formData[field]?.trim());
    if (missingFields.length > 0) {
      alert(`Please fill the required fields: ${missingFields.join(', ')}`);
      return;
    }

    // Prepare form data for submission
    const formDataToSend = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (value) {
        formDataToSend.append(key, value);
      }
    });

    try {
      await axios.post('http://localhost:8000/create_basic_info/', formDataToSend, {
        headers: { 'Content-Type': 'multipart/form-data' }, // Important for file upload
      });
      alert('Basic Info added successfully!');
    } catch (error) {
      console.error('Error adding basic info:', error);
      alert('Failed to add basic info. Please check the form and try again.');
    }
  };

  // Fields divided into pages (7 fields per page)
  const fieldPages = [
    ['first_name', 'last_name', 'father_name', 'location', 'gender', 'marital_status', 'date_of_birth'],
    ['mobile_phone', 'landline_phone', 'email', 'tax_id', 'address', 'department', 'responsibilities'],
    ['specialization', 'degree_available', 'salary', 'iban', 'hiring_date', 'employee_status', 'termination_date'],
    ['medical_exams', 'medical_exams_date', 'medical_exams_renewal_date', 'safety_passport', 'safety_passport_date', 'safety_passport_renewal_date', 'certifications_seminars']
  ];

  // Render input fields dynamically
  const renderFields = (fields) => {
    return fields.map((field) => (
      <div key={field} className="form-group">
        <label>{field.replace('_', ' ').toUpperCase()}</label>
        <input
          type={field.includes('date') ? 'date' : field === 'degree_available' ? 'file' : 'text'}
          name={field}
          value={field === 'degree_available' ? undefined : formData[field]} // File input should not have a value
          onChange={handleInputChange}
          className={`form-control ${requiredFields.includes(field) && !formData[field] ? 'input-error' : ''}`}
        />
      </div>
    ));
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Add Basic Info</h3>

      {renderFields(fieldPages[page - 1])}

      <div className="pagination-controls">
        <button type="button" onClick={() => setPage(page > 1 ? page - 1 : page)}>
          Previous
        </button>
        <button type="button" onClick={() => setPage(page < fieldPages.length ? page + 1 : page)}>
          Next
        </button>
        <button type="submit" disabled={!isFormValid} className="submit-btn">
          Submit
        </button>
      </div>
    </form>
  );
};

export default AddBasicInfo;
