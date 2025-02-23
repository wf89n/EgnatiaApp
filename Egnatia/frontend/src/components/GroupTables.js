import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GroupTables = () => {
  // States for groups data, loading state, error message, search query, and pagination
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [groupsPerPage] = useState(5);  // You can adjust this value

  // Fetch group data using axios
  useEffect(() => {
    axios.get('https://egnatiaapp.onrender.com/groups/')  // Replace with your backend URL
      .then(response => {
        setGroups(response.data);
        setLoading(false);  // Set loading to false once data is fetched
      })
      .catch(error => {
        setError('There was an error fetching the groups!');
        setLoading(false);  // Set loading to false even if there is an error
        console.error(error);
      });
  }, []);

  // Filter groups based on the search query
  const filteredGroups = groups.filter(group =>
    group.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Paginate the filtered groups
  const indexOfLastGroup = currentPage * groupsPerPage;
  const indexOfFirstGroup = indexOfLastGroup - groupsPerPage;
  const currentGroups = filteredGroups.slice(indexOfFirstGroup, indexOfLastGroup);

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
              Group List
            </h5>
            <p className="block mt-1 font-sans text-base antialiased font-normal leading-relaxed text-gray-700">
              See information about all groups
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

        {/* Groups Table */}
        <div className="p-6 px-0 overflow-scroll">
          <table className="w-full mt-4 text-left table-auto min-w-max">
            <thead>
              <tr>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-left">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Group Name</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Assigned Meters</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Done Meters</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Assigned Freatio</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Done Freatio</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Assigned Cabins</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Done Cabins</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Assigned Katheta</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Done Katheta</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50 text-center">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Total Expenses</p>
                </th>
              </tr>
            </thead>
            <tbody>
              {currentGroups.map((group) => (
                <tr key={group.id} className="text-center">
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.name}
                    </p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.total_meters_assigned || 0}
                    </p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.total_meters_done || 0}
                    </p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.total_freatio_assigned || 0}
                    </p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.total_freatio_done || 0}
                    </p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.total_cabins_assigned || 0}
                    </p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.total_cabins_done || 0}
                    </p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.total_katheta_assigned || 0}
                    </p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.total_katheta_done || 0}
                    </p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">
                      {group.total_expenses || 0}
                    </p>
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
            disabled={currentPage === Math.ceil(filteredGroups.length / groupsPerPage)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default GroupTables;
