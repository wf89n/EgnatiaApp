import React from 'react';
import { Link } from 'react-router-dom';

function Sidebar() {
  return (
    <div className="sidebar">
      <ul>
        <li><Link to="/groups">Groups</Link></li>
        <li><Link to="/regions">Regions</Link></li>
        <li><Link to="/customers">Customers</Link></li>
        <li><Link to="/attendance">Attendance</Link></li>
        <li><Link to="/add-basic-info">Add Basic Info</Link></li> {/* Add the new link */}
      </ul>
    </div>
  );
}

export default Sidebar;
