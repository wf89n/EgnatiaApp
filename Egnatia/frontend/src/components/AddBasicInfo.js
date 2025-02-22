import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';
import './tailwind.css';  // Import your Tailwind CSS file here

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

    setFormData((prevData) => {
      const updatedData = {
        ...prevData,
        [name]: type === 'file' ? files[0] : value,
      };
      validateForm(updatedData);
      return updatedData;
    });
  };

  // Validate required fields
  const validateForm = useCallback((updatedData) => {
    const allRequiredFieldsFilled = requiredFields.every((field) => {
      if (field === 'degree_available') {
        return updatedData[field] instanceof File; // Check if a file is selected
      }
      return updatedData[field]?.trim() !== '';
    });
    setIsFormValid(allRequiredFieldsFilled);
  }, [requiredFields]);

  useEffect(() => {
    validateForm(formData);
  }, [formData, validateForm]);

  // Get CSRF token from cookies
  const getCsrfToken = () => {
    const csrfToken = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : '';
  };

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
      await axios.post('https://egnatiaapp.onrender.com/create_basic_info/', formDataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': getCsrfToken(), // Add CSRF token to headers
        },
      });
      alert('Basic Info added successfully!');
    } catch (error) {
      console.error('Error adding basic info:', error);
      alert('Failed to add basic info. Please check the form and try again.');
    }
  };

  // Fields divided into pages
  const fieldPages = [
    ['first_name', 'last_name', 'father_name', 'location', 'gender', 'marital_status', 'date_of_birth'],
    ['mobile_phone', 'landline_phone', 'email', 'tax_id', 'address', 'department', 'responsibilities'],
    ['specialization', 'degree_available', 'salary', 'iban', 'hiring_date', 'employee_status', 'termination_date'],
    ['medical_exams', 'medical_exams_date', 'medical_exams_renewal_date', 'safety_passport', 'safety_passport_date', 'safety_passport_renewal_date', 'certifications_seminars']
  ];

  // Render input fields dynamically with section layout
  const renderFields = (fields) => {
    return fields.map((field) => (
      <div key={field} className="mb-6">
        <label htmlFor={field} className="block text-sm font-medium text-gray-700">
          {field.replace('_', ' ').toUpperCase()}
          {requiredFields.includes(field) && (
            <span className="text-red-500">*</span> // Red star for required fields
          )}
        </label>
        <input
          type={field.includes('date') ? 'date' : field === 'degree_available' ? 'file' : 'text'}
          name={field}
          value={field === 'degree_available' ? undefined : formData[field]} // File input should not have a value
          onChange={handleInputChange}
          className={`mt-1 block w-full px-24 py-1 border border-gray-1300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-700 ${requiredFields.includes(field) && !formData[field] ? 'border-red-500' : ''}`}
        />
      </div>
    ));
  };

  return (
    <form onSubmit={handleSubmit} className="p-5 max-w-333xl mx-auto bg-white shadow-md rounded-lg">
      <h3 className="text-2xl font-semibold text-gray-700 mb-6">Add Basic Info</h3>

      {/* Section layout for each page */}
      <div className="form-sections">
        <section className={`page-section ${page === 1 ? 'block' : 'hidden'}`}>
          <h4 className="text-xl font-semibold text-gray-700">Personal Information</h4>
          {renderFields(fieldPages[0])}
        </section>

        <section className={`page-section ${page === 2 ? 'block' : 'hidden'}`}>
          <h4 className="text-xl font-semibold text-gray-700">Contact Information</h4>
          {renderFields(fieldPages[1])}
        </section>

        <section className={`page-section ${page === 3 ? 'block' : 'hidden'}`}>
          <h4 className="text-xl font-semibold text-gray-700">Job Details</h4>
          {renderFields(fieldPages[2])}
        </section>

        <section className={`page-section ${page === 4 ? 'block' : 'hidden'}`}>
          <h4 className="text-xl font-semibold text-gray-700">Health & Safety Information</h4>
          {renderFields(fieldPages[3])}
        </section>
      </div>

      {/* Navigation Controls */}
      <div className="flex justify-between items-center mt-8">
        <button
          type="button"
          onClick={() => setPage(page > 1 ? page - 1 : page)}
          disabled={page === 1}
          className="bg-gray-300 text-gray-700 px-4 py-2 rounded-md disabled:opacity-50"
        >
          Previous
        </button>
        <div className="flex-1 text-center">
          <span className="text-sm text-gray-500">{page} / {fieldPages.length}</span>
        </div>
        <button
          type="button"
          onClick={() => setPage(page < fieldPages.length ? page + 1 : page)}
          disabled={page === fieldPages.length}
          className="bg-blue-500 text-white px-4 py-2 rounded-md disabled:opacity-50"
        >
          Next
        </button>
      </div>

      {/* Submit Button */}
      <div className="mt-8 flex justify-center">
        <button
          type="submit"
          disabled={!isFormValid}
          className={`w-full px-6 py-3 text-white font-medium rounded-md focus:outline-none ${
            isFormValid ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-gray-400 cursor-not-allowed'
          }`}
        >
          Submit
        </button>
      </div>
    </form>
  );
};

export default AddBasicInfo;
