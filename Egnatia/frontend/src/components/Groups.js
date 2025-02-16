import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Pie, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, DoughnutController, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement, DoughnutController);

const Groups = () => {
  const [groups, setGroups] = useState([]);
  const [searchQuery, setSearchQuery] = useState(''); // State for search query

  // Fetch groups data from the Django API
  useEffect(() => {
    axios.get('http://localhost:8000/groups/')  // Replace with your backend URL
      .then(response => {
        setGroups(response.data);
      })
      .catch(error => console.error('There was an error fetching the groups!', error));
  }, []);

  // Function to generate Pie Chart data for jobs assigned vs done with percentages
  const generateJobPieChartData = (assigned, done) => {
    const total = assigned + done;
    const assignedPercentage = ((assigned / total) * 100).toFixed(2); // Calculate the percentage for assigned
    const donePercentage = ((done / total) * 100).toFixed(2); // Calculate the percentage for done

    return {
      labels: [`Assigned: ${assignedPercentage}%`, `Done: ${donePercentage}%`],
      datasets: [
        {
          data: [assigned, done],
          backgroundColor: ['#FF6384', '#36A2EB'],
          hoverBackgroundColor: ['#FF6384', '#36A2EB'],
        },
      ],
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: (tooltipItem) => {
                const percentage = tooltipItem.raw;
                const label = tooltipItem.label;
                return `${label} (${percentage} meters)`; // Show label and meters for each segment
              },
            },
          },
        },
      },
    };
  };

  // Function to generate Pie Chart data for total cost per department with total cost in the center
  const generateCostPieChartData = (costs) => {
    if (!costs || typeof costs !== 'object') {
      return {
        labels: [],
        datasets: [],
      }; // Return empty data if costs is undefined or invalid
    }

    // Format costs to show only 2 decimal places
    const formattedCosts = Object.values(costs).map((cost) => parseFloat(cost).toFixed(2));

    // Calculate total cost
    const totalCost = formattedCosts.reduce((acc, cost) => acc + parseFloat(cost), 0).toFixed(2);

    return {
      labels: Object.keys(costs),
      datasets: [
        {
          data: formattedCosts,
          backgroundColor: ['#FFCD56', '#FF6384', '#36A2EB'],
          hoverBackgroundColor: ['#FFCD56', '#FF6384', '#36A2EB'],
        },
      ],
      // Adding a custom plugin to display the total cost in the center
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: (tooltipItem) => {
                return `${tooltipItem.label}: $${tooltipItem.raw.toFixed(2)}`; // Show cost with 2 decimals
              }
            }
          },
          // Custom text in the center of the pie
          beforeDraw: (chart) => {
            const ctx = chart.ctx;
            const width = chart.width;
            const height = chart.height;
            const fontSize = (height / 100).toFixed(2);
            ctx.font = `${fontSize}px Arial`;
            ctx.textBaseline = 'middle';
            const text = `$${totalCost}`;
            const textX = Math.round((width - ctx.measureText(text).width) / 2);
            const textY = height / 2;
            ctx.fillText(text, textX, textY); // Draw the total cost in the center
          },
        },
      },
    };
  };

  // Function to generate Barplot data for total cost per department
  const generateCostBarChartData = (costs) => {
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

  // Function to calculate the total cost of all departments for a group
  const calculateTotalCost = (costs) => {
    if (!costs || typeof costs !== 'object') return 0;

    // Ensure that all values are valid numbers before summing
    const validCosts = Object.values(costs).filter((cost) => !isNaN(cost)); // Filter out non-numeric values

    const totalCost = validCosts.reduce((acc, cost) => acc + parseFloat(cost), 0); // Sum valid numbers

    return totalCost.toFixed(2); // Return the total cost formatted to 2 decimal places
  };

  // Filter groups by search query
  const filteredGroups = groups.filter(group =>
    group.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Sort filtered groups by total expenses (descending)
  const sortedGroups = filteredGroups.sort((a, b) => b.total_expenses - a.total_expenses);

  return (
    <div>
      <h1>Groups</h1>

      <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: '15px' }}>
        <tbody>
          {/* Table row for groups and search bar */}
          <tr>
            <td colSpan={3} style={{ textAlign: 'right', paddingBottom: '20px' }}>
              {/* Search Bar on the right side of the table */}
              <input
                type="text"
                placeholder="Search by group name"
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
            </td>
          </tr>

          {/* Table row for displaying the groups */}
          {sortedGroups.slice(0, 3).map((group) => (
            <tr key={group.id}>
              <td style={{ padding: '15px' }}>
                <h2>{group.name}</h2>
                <div style={{ height: '300px', width: '100%' }}>
                  <h3>Job Assignment vs Done</h3>
                  <Pie
                    data={generateJobPieChartData(group.total_meters_assigned, group.total_meters_done)}
                  />
                </div>
              </td>
              <td style={{ padding: '15px' }}>
                <div style={{ height: '300px', width: '100%' }}>
                  <h3>Cost per Department </h3>
                  <Pie
                    data={generateCostPieChartData(group.departments_costs || {})} // Safe check here
                  />
                </div>
              </td>
              <td style={{ padding: '15px' }}>
                <div style={{ height: '300px', width: '100%' }}>
                  {/* Display total cost per department inside the barplot section */}
                  <h3>Total cost Per Department : ${calculateTotalCost(group.departments_costs || {})}</h3>
                  <Bar
                    data={generateCostBarChartData(group.departments_costs || {})} // Safe check here
                  />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Groups;
