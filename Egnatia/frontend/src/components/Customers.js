import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, DoughnutController } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, DoughnutController);

const Customers = () => {
  const [customers, setCustomers] = useState([]);
  const [searchQuery, setSearchQuery] = useState(''); // State for search query

  // Fetch customer data from the Django API
  useEffect(() => {
    axios.get('https://egnatiaapp.onrender.com/customers/')  // Replace with your backend URL
      .then(response => {
        setCustomers(response.data);
      })
      .catch(error => console.error('There was an error fetching the customers!', error));
  }, []);

  // Filter customers by search query
  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Function to generate Pie Chart data for Done vs Assigned (Total)
  const generateJobPieChartData = (assigned, done) => {
    const total = assigned + done;
    const assignedPercentage = ((assigned / total) * 100).toFixed(2);
    const donePercentage = ((done / total) * 100).toFixed(2);

    return {
      labels: [`Assigned: ${assignedPercentage}%`, `Done: ${donePercentage}%`],
      datasets: [
        {
          data: [assigned, done],
          backgroundColor: ['#FF6384', '#36A2EB'],
          hoverBackgroundColor: ['#FF6384', '#36A2EB'],
        },
      ],
    };
  };

  return (
    <div>
      <h1>Customers</h1>

      {/* Search Bar */}
      <div style={{ textAlign: 'right', paddingBottom: '20px' }}>
        <input
          type="text"
          placeholder="Search by customer name"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            width: '250px',
            padding: '10px',
            fontSize: '16px',
            borderRadius: '5px',
            border: '1px solid #ccc',
          }}
        />
      </div>

      <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: '15px' }}>
        <tbody>
          {/* Table row for displaying the customers */}
          {filteredCustomers.map((customer) => (
            <tr key={customer.id}>
              <td style={{ padding: '15px', textAlign: 'center' }}>
                {/* Customer Name */}
                <h2>{customer.name}</h2>

                {/* Row for 4 Pies: Done Assigned, Done Assigned for Cabins, Done Assigned for Freatio, Done Assigned for Katheta */}
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                  <div style={{ width: '23%' }}>
                    <h3>Done/Assigned (Total)</h3>
                    <Pie
                      data={generateJobPieChartData(customer.total_meters_assigned, customer.total_meters_done)}
                    />
                  </div>

                  <div style={{ width: '23%' }}>
                    <h3>Done/Assigned (Cabins)</h3>
                    <Pie
                      data={generateJobPieChartData(customer.total_cabins_assigned, customer.total_cabins_done)}
                    />
                  </div>

                  <div style={{ width: '23%' }}>
                    <h3>Done/Assigned (Freatio)</h3>
                    <Pie
                      data={generateJobPieChartData(customer.total_freatio_assigned, customer.total_freatio_done)}
                    />
                  </div>

                  <div style={{ width: '23%' }}>
                    <h3>Done/Assigned (Katheta)</h3>
                    <Pie
                      data={generateJobPieChartData(customer.total_catheta_assigned, customer.total_catheta_done)}
                    />
                  </div>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Customers;
