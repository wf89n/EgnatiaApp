import React, { useState, useEffect } from 'react';

const EmployeeTable = () => {
  const [employees, setEmployees] = useState([]);

  // Fetch employees when the component mounts
  useEffect(() => {
    const fetchEmployees = async () => {
      try {
        const response = await fetch('https://egnatiaapp.onrender.com/employees/');
        const data = await response.json();
        setEmployees(data);
      } catch (error) {
        console.error('Error fetching employee data:', error);
      }
    };

    fetchEmployees();
  }, []);

  return (
    <div className="relative flex flex-col w-full h-full text-gray-700 bg-white shadow-md rounded-xl bg-clip-border">
      <div className="relative mx-4 mt-4 overflow-hidden text-gray-700 bg-white rounded-none bg-clip-border">
        <div className="flex items-center justify-between gap-8 mb-8">
          <div>
            <h5 className="block font-sans text-xl antialiased font-semibold leading-snug tracking-normal text-blue-gray-900">
              Employees list
            </h5>
            <p className="block mt-1 font-sans text-base antialiased font-normal leading-relaxed text-gray-700">
              See information about all employees
            </p>
          </div>
          <div className="flex flex-col gap-2 shrink-0 sm:flex-row">
            <button className="select-none rounded-lg border border-gray-900 py-2 px-4 text-center align-middle font-sans text-xs font-bold uppercase text-gray-900 transition-all hover:opacity-75 focus:ring focus:ring-gray-300 active:opacity-[0.85] disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" type="button">
              view all
            </button>
            <button className="flex select-none items-center gap-3 rounded-lg bg-gray-900 py-2 px-4 text-center align-middle font-sans text-xs font-bold uppercase text-white shadow-md shadow-gray-900/10 transition-all hover:shadow-lg hover:shadow-gray-900/20 focus:opacity-[0.85] focus:shadow-none active:opacity-[0.85] active:shadow-none disabled:pointer-events-none disabled:opacity-50 disabled:shadow-none" type="button">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" stroke-width="2" className="w-4 h-4">
                <path d="M6.25 6.375a4.125 4.125 0 118.25 0 4.125 4.125 0 01-8.25 0zM3.25 19.125a7.125 7.125 0 0114.25 0v.003l-.001.119a.75.75 0 01-.363.63 13.067 13.067 0 01-6.761 1.873c-2.472 0-4.786-.684-6.76-1.873a.75.75 0 01-.364-.63l-.001-.122zM19.75 7.5a.75.75 0000-1.5 0v2.25H16a.75.75 0 000 1.5h2.25v2.25a.75.75 0 001.5 0v-2.25H22a.75.75 0 000-1.5h-2.25V7.5z"></path>
              </svg>
              Add member
            </button>
          </div>
        </div>
        <div className="p-6 px-0 overflow-scroll">
          <table className="w-full mt-4 text-left table-auto min-w-max">
            <thead>
              <tr>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Member</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Function</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Role</p>
                </th>
                <th className="p-4 border-y border-blue-gray-100 bg-blue-gray-50/50">
                  <p className="block font-sans text-sm antialiased font-normal leading-none text-blue-gray-900 opacity-70">Photo</p>
                </th>
              </tr>
            </thead>
            <tbody>
              {employees.map((employee) => (
                <tr key={employee.id} className="text-center">
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{employee.basic_info.first_name} {employee.basic_info.last_name}</p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{employee.role_name}</p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    <p className="font-sans text-base antialiased font-normal text-blue-gray-900">{employee.department_name}</p>
                  </td>
                  <td className="p-4 border-y border-blue-gray-100">
                    {employee.photo ? (
                      <img src={employee.photo} alt={`${employee.basic_info.first_name} ${employee.basic_info.last_name}`} className="w-10 h-10 rounded-full" />
                    ) : (
                      'No Photo'
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default EmployeeTable;
