import React, { useEffect, useState } from "react";
import axios from "axios";

const Attendance = () => {
  const [regions, setRegions] = useState([]);
  const [groups, setGroups] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState("");
  const [selectedGroup, setSelectedGroup] = useState("");
  const [attendance, setAttendance] = useState({});

  // Fetch regions on mount
  useEffect(() => {
    axios.get("'https://egnatiaapp.onrender.com/regions/")
      .then((response) => setRegions(response.data))
      .catch((error) => console.error("Error fetching regions:", error));
  }, []);

  // Fetch groups when a region is selected
  useEffect(() => {
    if (selectedRegion) {
      axios.get(`http://localhost:8000/groups/?region_id=${selectedRegion}`)
        .then((response) => setGroups(response.data))
        .catch((error) => console.error("Error fetching groups:", error));
    }
  }, [selectedRegion]);

  // Fetch employees when a group is selected
  useEffect(() => {
    if (selectedGroup) {
      axios.get(`http://localhost:8000/employees/?group_id=${selectedGroup}`)
        .then((response) => {
          setEmployees(response.data);
          const initialAttendance = {};
          response.data.forEach((employee) => {
            initialAttendance[employee.basic_info.id] = { presence: "NO", quantity: 0 };
          });
          setAttendance(initialAttendance);
        })
        .catch((error) => console.error("Error fetching employees:", error));
    }
  }, [selectedGroup]);

  // Handle attendance change
  const handleAttendanceChange = (basicInfoId, field, value) => {
    setAttendance((prev) => ({
      ...prev,
      [basicInfoId]: {
        ...prev[basicInfoId],
        [field]: value,
      },
    }));
  };

  // Submit attendance
  const handleSubmit = () => {
  const attendanceData = Object.entries(attendance).map(([basicInfoId, data]) => ({
    employee_id: basicInfoId,  // Adjusted to use employee_id as basic_info
    presence: data.presence,
    quantity: data.quantity,
  }));

  // Send the request with correct data structure
  axios.post('http://localhost:8000/submit-attendance/', {
    group_id: selectedGroup,  // Make sure to send the selected group_id
    attendance: attendanceData  // Passing the proper attendance data structure
  })
  .then(response => console.log("Success:", response))
  .catch(error => console.error("Error:", error));
};


  return (
    <div>
      <h2>Attendance Report</h2>

      {/* Region Filter */}
      <label>Select Region:</label>
      <select value={selectedRegion} onChange={(e) => setSelectedRegion(e.target.value)}>
        <option value="">-- Select Region --</option>
        {regions.map((region) => (
          <option key={region.id} value={region.id}>
            {region.name}
          </option>
        ))}
      </select>

      {/* Group Filter */}
      {selectedRegion && (
        <>
          <label>Select Group:</label>
          <select value={selectedGroup} onChange={(e) => setSelectedGroup(e.target.value)}>
            <option value="">-- Select Group --</option>
            {groups.map((group) => (
              <option key={group.id} value={group.id}>
                {group.name}
              </option>
            ))}
          </select>
        </>
      )}

      {/* Attendance Table */}
      {selectedGroup && employees.length > 0 && (
        <>
          <h3>Mark Attendance</h3>
          <table border="1">
            <thead>
              <tr>
                <th>Name</th>
                <th>Presence</th>
                <th>Quantity</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((employee) => (
                <tr key={employee.basic_info.id}>
                  <td>{employee.basic_info.first_name} {employee.basic_info.last_name}</td>
                  <td>
                    <select
                      value={attendance[employee.basic_info.id]?.presence || "NO"}
                      onChange={(e) => handleAttendanceChange(employee.basic_info.id, "presence", e.target.value)}
                    >
                      <option value="YES">YES</option>
                      <option value="NO">NO</option>
                    </select>
                  </td>
                  <td>
                    <input
                      type="number"
                      value={attendance[employee.basic_info.id]?.quantity || 0}
                      onChange={(e) => handleAttendanceChange(employee.basic_info.id, "quantity", parseInt(e.target.value))}
                      min="0"
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Submit Button */}
          <button onClick={handleSubmit}>Submit Attendance</button>
        </>
      )}
    </div>
  );
};

export default Attendance;
