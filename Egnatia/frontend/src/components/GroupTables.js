import React, { useEffect, useState } from 'react';
import axios from 'axios';

const GroupTables = () => {
    const [groups, setGroups] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get('https://egnatiaapp.onrender.com/groups/')  // Replace with your backend URL
            .then(response => {
                setGroups(response.data);
                setLoading(false);
            })
            .catch(error => {
                setError(error.message);
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;

    return (
        <div>
            <h2>Group Data</h2>
            <table border="1" style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Total Expenses</th>
                        <th>Total Meters Assigned</th>
                        <th>Total Meters Done</th>
                        <th>Total Freatio Assigned</th>
                        <th>Total Freatio Done</th>
                        <th>Total Cabins Assigned</th>
                        <th>Total Cabins Done</th>
                        <th>Total Katheta Assigned</th>
                        <th>Total Katheta Done</th>
                    </tr>
                </thead>
                <tbody>
                    {groups.map(group => (
                        <tr key={group.id}>
                            <td>{group.id}</td>
                            <td>{group.name}</td>
                            <td>{group.total_expenses}</td>
                            <td>{group.total_meters_assigned}</td>
                            <td>{group.total_meters_done}</td>
                            <td>{group.total_freatio_assigned || 0}</td>
                            <td>{group.total_freatio_done || 0}</td>
                            <td>{group.total_cabins_assigned || 0}</td>
                            <td>{group.total_cabins_done || 0}</td>
                            <td>{group.total_catheta_assigned || 0}</td>
                            <td>{group.total_catheta_done || 0}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default GroupTables;
