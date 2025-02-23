import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Groups from './components/Groups';
import Regions from './components/Regions';
import Customers from './components/Customers';
import Attendance from './components/Attendance';
import AddBasicInfo from './components/AddBasicInfo'; // Import the AddBasicInfo component
import RegionTables from './components/RegionTables';
import GroupTables from './components/GroupTables';
import CustomerTables from './components/CustomerTables';
import EmployeeTable from "./components/EmpoyeeTables";
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
            <Route path="/region-tables" element={<RegionTables />} />
            <Route path="/customer-tables" element={<CustomerTables />} />
            <Route path="/employee-tables" element={<EmployeeTable />} />
            <Route path="/group-tables" element={<GroupTables />} />

          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
