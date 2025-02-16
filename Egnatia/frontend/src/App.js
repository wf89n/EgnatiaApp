import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Groups from './components/Groups';
import Regions from './components/Regions';
import Customers from './components/Customers';
import Attendance from './components/Attendance';
import AddBasicInfo from './components/AddBasicInfo'; // Import the AddBasicInfo component

const App = () => {
  return (
    <Router>
      <div style={{ display: 'flex' }}>
        <Sidebar />
        <div style={{ marginLeft: '260px', padding: '20px' }}>
          <Routes>
            <Route path="/" element={<Groups />} />
            <Route path="/groups" element={<Groups />} />
            <Route path="/regions" element={<Regions />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/attendance" element={<Attendance />} />
            <Route path="/add-basic-info" element={<AddBasicInfo />} /> {/* Route for the new form */}
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
