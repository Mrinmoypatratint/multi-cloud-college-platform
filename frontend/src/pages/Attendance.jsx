import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Calendar, Check, X, AlertTriangle, CheckCircle, PieChart } from 'lucide-react';

export const Attendance = () => {
  const { user } = useAuth();
  const isFaculty = user?.role === 'FACULTY' || user?.role === 'COLLEGE_ADMIN' || user?.role === 'SUPER_ADMIN';

  const [summary, setSummary] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [studentList, setStudentList] = useState([]);
  const [attendanceMap, setAttendanceMap] = useState({});
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    const loadSummary = async () => {
      try {
        const res = await api.get('/attendance/summary/');
        setSummary(res.data.data);
      } catch (err) {
        console.error('Failed to load attendance summary', err);
      }
    };

    const loadFacultyContext = async () => {
      try {
        const [subjRes, stuRes] = await Promise.all([
          api.get('/academic/subjects/'),
          api.get('/users/users/?role=STUDENT')
        ]);
        const subjs = subjRes.data.results || subjRes.data || [];
        setSubjects(subjs);
        if (subjs.length > 0) setSelectedSubject(subjs[0].id);

        const stus = stuRes.data.results || stuRes.data || [];
        setStudentList(stus);

        // Default all students to PRESENT
        const initialMap = {};
        stus.forEach((s) => { initialMap[s.id] = 'PRESENT'; });
        setAttendanceMap(initialMap);
      } catch (err) {
        console.error('Failed to load faculty attendance context', err);
      }
    };

    loadSummary();
    if (isFaculty) {
      loadFacultyContext();
    }
  }, [isFaculty]);

  const toggleStudentStatus = (studentId) => {
    setAttendanceMap((prev) => ({
      ...prev,
      [studentId]: prev[studentId] === 'PRESENT' ? 'ABSENT' : 'PRESENT'
    }));
  };

  const handleSaveAttendance = async () => {
    setSaving(true);
    setSuccessMsg('');
    try {
      const recordsPayload = Object.keys(attendanceMap).map((stuId) => ({
        student_id: parseInt(stuId),
        status: attendanceMap[stuId]
      }));

      await api.post('/attendance/bulk/', {
        subject_id: parseInt(selectedSubject),
        date: date,
        section: 'A',
        records: recordsPayload
      });

      setSuccessMsg('Attendance marked successfully!');
      setTimeout(() => setSuccessMsg(''), 4000);
    } catch (err) {
      alert('Failed to submit attendance');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      <div>
        <h2>Attendance Portal & Analytics</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          {isFaculty ? 'Conduct class sessions and log student attendance.' : 'Monitor your course attendance metrics and thresholds.'}
        </p>
      </div>

      {/* Student View Summary */}
      {summary && (
        <div className="grid-3">
          <div className="card">
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Overall Attendance</p>
            <h2 style={{ fontSize: '2rem', marginTop: '6px', color: summary.overall_percentage >= 75 ? 'var(--success)' : 'var(--danger)' }}>
              {summary.overall_percentage}%
            </h2>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '8px' }}>
              {summary.overall_percentage >= 75 ? 'Eligible for examination' : 'Below 75% requirement alert!'}
            </p>
          </div>

          <div className="card">
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Total Classes Attended</p>
            <h2 style={{ fontSize: '2rem', marginTop: '6px' }}>{summary.present_classes} / {summary.total_classes}</h2>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '8px' }}>
              Total conducted sessions logged
            </p>
          </div>

          <div className="card">
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Absences</p>
            <h2 style={{ fontSize: '2rem', marginTop: '6px', color: 'var(--danger)' }}>{summary.absent_classes}</h2>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '8px' }}>
              Unexcused leave instances
            </p>
          </div>
        </div>
      )}

      {/* Faculty Attendance Marking Matrix */}
      {isFaculty && (
        <div className="card">
          <h3 style={{ marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Calendar size={18} color="var(--primary)" /> Mark Class Attendance
          </h3>

          {successMsg && (
            <div style={{ padding: '12px', backgroundColor: 'var(--success-bg)', color: 'var(--success)', borderRadius: '6px', marginBottom: '16px', fontSize: '0.875rem' }}>
              {successMsg}
            </div>
          )}

          <div className="grid-2" style={{ marginBottom: '20px' }}>
            <div className="form-group">
              <label>Select Subject</label>
              <select value={selectedSubject} onChange={(e) => setSelectedSubject(e.target.value)}>
                {subjects.map((s) => (
                  <option key={s.id} value={s.id}>{s.code} - {s.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Date</label>
              <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            </div>
          </div>

          <div className="table-container" style={{ marginBottom: '20px' }}>
            <table>
              <thead>
                <tr>
                  <th>Enrollment No</th>
                  <th>Student Name</th>
                  <th>Status Toggle</th>
                </tr>
              </thead>
              <tbody>
                {studentList.map((stu) => {
                  const status = attendanceMap[stu.id] || 'PRESENT';
                  return (
                    <tr key={stu.id}>
                      <td style={{ fontWeight: 600 }}>{stu.student_profile?.enrollment_number || `STU-${stu.id}`}</td>
                      <td>{stu.full_name || stu.username}</td>
                      <td>
                        <button
                          type="button"
                          onClick={() => toggleStudentStatus(stu.id)}
                          className={`btn ${status === 'PRESENT' ? 'btn-primary' : 'btn-danger'}`}
                          style={{ padding: '6px 14px', fontSize: '0.8rem' }}
                        >
                          {status === 'PRESENT' ? <Check size={14} /> : <X size={14} />}
                          {status}
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <button onClick={handleSaveAttendance} disabled={saving} className="btn btn-primary">
            {saving ? 'Submitting...' : 'Submit Attendance Record'}
          </button>
        </div>
      )}

    </div>
  );
};
