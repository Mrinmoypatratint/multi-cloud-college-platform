import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Search, Filter, Plus, UserCheck, Mail, Phone, BookOpen } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Students = () => {
  const { user } = useAuth();
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);

  // Form State
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: 'password123',
    first_name: '',
    last_name: '',
    role: 'STUDENT',
    enrollment_number: '',
    batch_year: 2026,
    semester: 1
  });

  const fetchStudents = async () => {
    try {
      const res = await api.get('/users/users/?role=STUDENT');
      setStudents(res.data.results || res.data || []);
    } catch (err) {
      console.error('Failed to fetch students', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleCreateStudent = async (e) => {
    e.preventDefault();
    try {
      await api.post('/users/users/', formData);
      setShowModal(false);
      fetchStudents();
      setFormData({
        username: '',
        email: '',
        password: 'password123',
        first_name: '',
        last_name: '',
        role: 'STUDENT',
        enrollment_number: '',
        batch_year: 2026,
        semester: 1
      });
    } catch (err) {
      alert('Error creating student. Please check input fields.');
    }
  };

  const filteredStudents = students.filter((s) => {
    const term = search.toLowerCase();
    return (
      s.full_name?.toLowerCase().includes(term) ||
      s.username?.toLowerCase().includes(term) ||
      s.email?.toLowerCase().includes(term) ||
      s.student_profile?.enrollment_number?.toLowerCase().includes(term)
    );
  });

  const isCanAdd = ['SUPER_ADMIN', 'COLLEGE_ADMIN', 'STAFF'].includes(user?.role);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2>Student Registration & Directory</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Manage active student profiles, enrollments, and academic details.
          </p>
        </div>
        {isCanAdd && (
          <button onClick={() => setShowModal(true)} className="btn btn-primary">
            <Plus size={18} /> Register New Student
          </button>
        )}
      </div>

      {/* Filter & Search Bar */}
      <div className="card" style={{ padding: '16px 20px', display: 'flex', gap: '16px', alignItems: 'center' }}>
        <div style={{ position: 'relative', flex: 1 }}>
          <Search size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search by name, username, email, or enrollment no..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ paddingLeft: '38px' }}
          />
        </div>
      </div>

      {/* Student Table */}
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Enrollment No</th>
              <th>Student Name</th>
              <th>Email Address</th>
              <th>Department</th>
              <th>Batch / Sem</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="6" style={{ textAlign: 'center', padding: '24px' }}>Loading student records...</td></tr>
            ) : filteredStudents.length === 0 ? (
              <tr><td colSpan="6" style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)' }}>No student records found.</td></tr>
            ) : (
              filteredStudents.map((s) => (
                <tr key={s.id}>
                  <td style={{ fontWeight: 600 }}>{s.student_profile?.enrollment_number || `STU-${s.id}`}</td>
                  <td style={{ fontWeight: 500 }}>{s.full_name || s.username}</td>
                  <td>{s.email || 'N/A'}</td>
                  <td>{s.student_profile?.department_details?.name || 'Computer Science'}</td>
                  <td>Sem {s.student_profile?.semester || 1} ({s.student_profile?.batch_year || 2026})</td>
                  <td><span className="badge badge-success">Active</span></td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Add Student Modal */}
      {showModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div className="card" style={{ width: '100%', maxWidth: '500px', backgroundColor: 'var(--bg-card)', padding: '30px' }}>
            <h3 style={{ marginBottom: '16px' }}>Register New Student Profile</h3>
            <form onSubmit={handleCreateStudent}>
              <div className="grid-2">
                <div className="form-group">
                  <label>First Name</label>
                  <input type="text" required value={formData.first_name} onChange={(e) => setFormData({ ...formData, first_name: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Last Name</label>
                  <input type="text" required value={formData.last_name} onChange={(e) => setFormData({ ...formData, last_name: e.target.value })} />
                </div>
              </div>
              <div className="form-group">
                <label>Username</label>
                <input type="text" required value={formData.username} onChange={(e) => setFormData({ ...formData, username: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Email Address</label>
                <input type="email" required value={formData.email} onChange={(e) => setFormData({ ...formData, email: e.target.value })} />
              </div>
              <div className="grid-2">
                <div className="form-group">
                  <label>Enrollment Number</label>
                  <input type="text" placeholder="e.g. STU-2026-099" value={formData.enrollment_number} onChange={(e) => setFormData({ ...formData, enrollment_number: e.target.value })} />
                </div>
                <div className="form-group">
                  <label>Semester</label>
                  <input type="number" min="1" max="8" value={formData.semester} onChange={(e) => setFormData({ ...formData, semester: parseInt(e.target.value) })} />
                </div>
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '20px' }}>
                <button type="button" onClick={() => setShowModal(false)} className="btn btn-secondary">Cancel</button>
                <button type="submit" className="btn btn-primary">Save Student</button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
