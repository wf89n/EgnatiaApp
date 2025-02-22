import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, DoughnutController } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, DoughnutController);

const Regions = () => {
  const [regions, setRegions] = useState([]);
  const [searchQuery, setSearchQuery] = useState(''); // State for search query

  // Fetch regions data from the Django API
  useEffect(() => {
    axios.get('https://egnatiaapp.onrender.com/regions/')  // Replace with your backend URL
      .then(response => {
        setRegions(response.data);
      })
      .catch(error => console.error('There was an error fetching the regions!', error));
  }, []);

  // Filter regions by search query
  const filteredRegions = regions.filter(region =>
    region.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Function to generate Pie Chart data for Done vs Assigned per region (total for the region)
  const generateJobPieChartData = (totalAssigned, totalDone) => {
    const total = totalAssigned + totalDone;
    const assignedPercentage = ((totalAssigned / total) * 100).toFixed(2);
    const donePercentage = ((totalDone / total) * 100).toFixed(2);

    return {
      labels: [`Assigned: ${assignedPercentage}%`, `Done: ${donePercentage}%`],
      datasets: [
        {
          data: [totalAssigned, totalDone],
          backgroundColor: ['#FF6384', '#36A2EB'],
          hoverBackgroundColor: ['#FF6384', '#36A2EB'],
        },
      ],
    };
  };

  // Function to generate Pie Chart data for Expenses per Group inside Region
  const generateRegionExpensesPerGroupData = (groups) => {
    const groupNames = groups.map(group => group.name);
    const groupExpenses = groups.map(group => group.total_expenses);

    return {
      labels: groupNames,
      datasets: [
        {
          data: groupExpenses,
          backgroundColor: ['#FFCD56', '#FF6384', '#36A2EB', '#FF9F40', '#4BC0C0'],
          hoverBackgroundColor: ['#FFCD56', '#FF6384', '#36A2EB', '#FF9F40', '#4BC0C0'],
        },
      ],
    };
  };

  // Function to generate Bar Chart data for Expenses per Department (aggregated data from all groups)
  const generateRegionExpensesPerDepartmentData = (costs) => {
    return {
      labels: Object.keys(costs),
      datasets: [
        {
          label: 'Total Cost',
          data: Object.values(costs),
          backgroundColor: '#FFCD56',
          borderColor: '#FFCD56',
          borderWidth: 1,
        },
      ],
    };
  };

  return (
    <div>
      <h1>Regions</h1>

      {/* Search Bar */}
      <div style={{ textAlign: 'right', paddingBottom: '20px' }}>
        <input
          type="text"
          placeholder="Search by region name"
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
          {/* Table row for displaying the regions */}
          {filteredRegions.map((region) => {
            // Calculate total values per region
            const totalAssigned = region.groups.reduce((sum, group) => sum + group.total_meters_assigned, 0);
            const totalDone = region.groups.reduce((sum, group) => sum + group.total_meters_done, 0);

            // Aggregating expenses by department across all groups
            const departmentExpenses = region.groups.reduce((acc, group) => {
              const groupDeptCosts = group.departments_costs;
              for (let dept in groupDeptCosts) {
                acc[dept] = (acc[dept] || 0) + groupDeptCosts[dept];
              }
              return acc;
            }, {});

            return (
              <tr key={region.id}>
                <td style={{ padding: '15px', textAlign: 'center' }}>
                  {/* Region Name */}
                  <h2>{region.name}</h2>

                  {/* Row for 3 Charts: Done Assigned, Expenses per Group, Expenses per Department */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
                    <div style={{ width: '30%' }}>
                      <h3>Done/Assigned per Region</h3>
                      <Pie
                        data={generateJobPieChartData(totalAssigned, totalDone)}
                      />
                    </div>

                    <div style={{ width: '30%' }}>
                      <h3>Expenses per Group inside Region</h3>
                      <Pie
                        data={generateRegionExpensesPerGroupData(region.groups)}
                      />
                    </div>

                    <div style={{ width: '30%' }}>
                      <h3>Expenses per Department (Aggregated from Groups)</h3>
                      <Bar
                        data={generateRegionExpensesPerDepartmentData(departmentExpenses)}
                      />
                    </div>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default Regions;
