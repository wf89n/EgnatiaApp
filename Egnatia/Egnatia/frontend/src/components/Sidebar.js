import React from 'react';
import { Link } from 'react-router-dom';

function Sidebar() {
  return (
    <div className="sidebar">
      <ul>
        <li><Link to="/groups">Groups</Link></li>
        <li><Link to="/regions">Regions</Link></li> {/* Add the Regions link here */}
        <li> <Link to="/customers">Customers</Link></li>
        <li><Link to="/attendance">Attendance</Link></li>

        {/* Add other links as necessary */}
      </ul>
    </div>
  );
}

export default Sidebar;


