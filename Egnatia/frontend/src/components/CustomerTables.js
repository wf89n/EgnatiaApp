import React, { useEffect, useState } from 'react';
import axios from 'axios';

const CustomerTables = () => {
  // States for customers data, loading state, error message, and search query
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch customer data using axios
  useEffect(() => {
    axios.get('https://egnatiaapp.onrender.com/customers/')  // Replace with your backend URL
      .then(response => {
        setCustomers(response.data);
        setLoading(false);  // Set loading to false once data is fetched
      })
      .catch(error => {
        setError('There was an error fetching the customers!');
        setLoading(false);  // Set loading to false even if there is an error
        console.error(error);
      });
  }, []);

  // Filter customers based on the search query
  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return <div>Loading...</div>;  // Display loading message while data is being fetched
  }

  if (error) {
    return <div>{error}</div>;  // Display error message if there's an error
  }

  return (
    <div>
      <h2>Customer List</h2>

      {/* Search input field to filter customers */}
      <input
        type="text"
        placeholder="Search by name"
        value={searchQuery}
        onChange={e => setSearchQuery(e.target.value)}  // Update search query on input change
      />

      {/* Customer table */}
      <table border="1">
        <thead>
          <tr>
            <th>Name</th>
            <th>Total Meters Assigned</th>
            <th>Total Freatio Assigned</th>
            <th>Total Cabins Assigned</th>
            <th>Total Katheta Assigned</th>
            <th>Total Meters Done</th>
            <th>Total Freatio Done</th>
            <th>Total Cabins Done</th>
            <th>Total Katheta Done</th>
          </tr>
        </thead>
        <tbody>
          {filteredCustomers.map(customer => (
            <tr key={customer.id}>
              <td>{customer.name}</td>
              <td>{customer.total_meters_assigned}</td>
              <td>{customer.total_freatio_assigned}</td>
              <td>{customer.total_cabins_assigned}</td>
              <td>{customer.total_catheta_assigned}</td>
              <td>{customer.total_meters_done}</td>
              <td>{customer.total_freatio_done}</td>
              <td>{customer.total_cabins_done}</td>
              <td>{customer.total_catheta_done}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerTables;
