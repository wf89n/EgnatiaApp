import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CustomerTables = () => {
  // States for customers data, loading state, error message, search query, and pagination
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [customersPerPage] = useState(5);  // You can adjust this value

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

  // Paginate the filtered customers
  const indexOfLastCustomer = currentPage * customersPerPage;
  const indexOfFirstCustomer = indexOfLastCustomer - customersPerPage;
  const currentCustomers = filteredCustomers.slice(indexOfFirstCustomer, indexOfLastCustomer);

  // Handle page change
  const paginate = (pageNumber) => setCurrentPage(pageNumber);

  if (loading) {
    return <div>Loading...</div>;  // Display loading message while data is being fetched
  }

  if (error) {
    return <div>{error}</div>;  // Display error message if there's an error
  }

  return (
    <div className="relative flex flex-col w-full h-full text-gray-700 bg-white shadow-md rounded-xl bg-clip-border">
      <div className="relative mx-4 mt-4 overflow-hidden text-gray-700 bg-white rounded-none bg-clip-border">
        <div className="flex items-center justify-between gap-8 mb-8">
          <div>
            <h5 className="block font-sans text-xl antialiased font-semibold leading-snug tracking-normal text-blue-gray-900">
              Customer List
            </h5>
            <p className="block mt-1 font-sans text-base antialiased font-normal leading-relaxed text-gray-700">
              See information about all customers
            </p>
          </div>
          <div className="flex flex-col gap-2 shrink-0 sm:flex-row">
            <button className="select-none rounded-lg border border-gray-900 py-2 px-4 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:opacity-75 focus:ring focus:ring-gray-300 active:opacity-[0.85] disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" type="button">
              View All
            </button>
            <button className="flex select-none items-center gap-3 rounded-lg bg-gray-900 py-2 px-4 text-center align-middle font-sans text-xs font-bold uppercase text-white shadow-md shadow-gray-900/10 transition-all hover:shadow-lg hover:shadow-gray-900/20 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" type="button">
              Add More
            </button>
          </div>
        </div>

        {/* Search Bar */}
        <div className="mb-4 mx-6">
          <input
            type="text"
            placeholder="Search by name"
            className="w-full p-2 border border-gray-300 rounded-md"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}  // Update search query on input change
          />
        </div>

        {/* Customers Table */}
        <div className="p-6 px-0 overflow-scroll">
          <table className="w-full mt-4 text-left table-auto min-w-max">
            <thead>
              <tr>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-left">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Customer Name</p>
                </th>
                {/* Total Meters (Assigned vs Done) */}
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Assigned Meters</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Done Meters</p>
                </th>
                {/* Total Freatio (Assigned vs Done) */}
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Assigned Freatio</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Done Freatio</p>
                </th>
                {/* Total Cabins (Assigned vs Done) */}
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Assigned Cabins</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Done Cabins</p>
                </th>
                {/* Total Katheta (Assigned vs Done) */}
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Assigned Katheta</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Done Katheta</p>
                </th>
              </tr>
            </thead>
            <tbody>
              {currentCustomers.map((customer) => (
                <tr key={customer.id} className="text-center">
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {customer.name}
                    </p>
                  </td>
                  {/* Total Meters (Assigned vs Done) */}
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{customer.total_meters_assigned}</p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{customer.total_meters_done}</p>
                  </td>
                  {/* Total Freatio (Assigned vs Done) */}
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{customer.total_freatio_assigned}</p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{customer.total_freatio_done}</p>
                  </td>
                  {/* Total Cabins (Assigned vs Done) */}
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{customer.total_cabins_assigned}</p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{customer.total_cabins_done}</p>
                  </td>
                  {/* Total Katheta (Assigned vs Done) */}
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{customer.total_catheta_assigned}</p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{customer.total_catheta_done}</p>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="flex justify-center items-center mt-4">
          <button
            onClick={() => paginate(currentPage - 1)}
            className="px-4 py-2 mx-2 bg-gray-300 text-gray-700 rounded-lg disabled:opacity-50"
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span className="px-4 py-2 text-gray-700">{currentPage}</span>
          <button
            onClick={() => paginate(currentPage + 1)}
            className="px-4 py-2 mx-2 bg-gray-300 text-gray-700 rounded-lg disabled:opacity-50"
            disabled={currentPage === Math.ceil(filteredCustomers.length / customersPerPage)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default CustomerTables;
