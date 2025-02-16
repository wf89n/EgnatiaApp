import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Groups from './components/Groups';
import Regions from './components/Regions'; // Import Regions component
import Customers from './components/Customers'; // Import Customers component
import Attendance from './components/Attendance';

const App = () => {
  return (
    <Router>
      <div style={{ display: 'flex' }}>
        <Sidebar /> {/* Sidebar will be on the left */}
        <div style={{ marginLeft: '260px', padding: '20px' }}>
          <Routes>
            {/* Define routes here */}
            <Route path="/" element={<Groups />} /> {/* Default route for groups */}
            <Route path="/groups" element={<Groups />} /> {/* Route for groups */}
            <Route path="/regions" element={<Regions />} /> {/* Add route for regions */}
            <Route path="/customers" element={<Customers />} /> {/* Add route for customers */}
            <Route path="/attendance" element={<Attendance />} />

          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
