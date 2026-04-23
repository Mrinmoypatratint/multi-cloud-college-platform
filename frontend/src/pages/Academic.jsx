import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { BookOpen, Building, Award, Layers } from 'lucide-react';

export const Academic = () => {
  const [departments, setDepartments] = useState([]);
  const [courses, setCourses] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [deptRes, courseRes, subjRes] = await Promise.all([
          api.get('/academic/departments/'),
          api.get('/academic/courses/'),
          api.get('/academic/subjects/')
        ]);
        setDepartments(deptRes.data.results || deptRes.data || []);
        setCourses(courseRes.data.results || courseRes.data || []);
        setSubjects(subjRes.data.results || subjRes.data || []);
      } catch (err) {
        console.error('Failed to load academic data', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div>
        <h2>Academic Catalog & Departments</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Overview of college academic departments, degree programs, and curriculum subjects.
        </p>
      </div>

      {/* Departments Grid */}
      <h3 style={{ marginTop: '8px' }}>Departments</h3>
      <div className="grid-3">
        {departments.map((dept) => (
          <div key={dept.id} className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
              <div style={{ padding: '10px', borderRadius: '10px', backgroundColor: 'var(--primary-light)', color: 'var(--primary)' }}>
                <Building size={20} />
              </div>
              <div>
                <h3 style={{ fontSize: '1rem' }}>{dept.name}</h3>
                <span className="badge badge-info">{dept.code}</span>
              </div>
            </div>
            <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)', marginBottom: '14px' }}>
              {dept.description || 'Core engineering and technology discipline.'}
            </p>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-muted)', borderTop: '1px solid var(--border-color)', paddingTop: '10px' }}>
              <span>Head: {dept.head_name || 'Assigned'}</span>
              <span>{dept.courses_count || 1} Program(s)</span>
            </div>
          </div>
        ))}
      </div>

      {/* Subjects Catalog */}
      <h3 style={{ marginTop: '16px' }}>Curriculum Subjects & Course Mapping</h3>
      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Subject Code</th>
              <th>Subject Name</th>
              <th>Course / Program</th>
              <th>Semester</th>
              <th>Credits</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="6" style={{ textAlign: 'center', padding: '24px' }}>Loading catalog...</td></tr>
            ) : subjects.map((subj) => (
              <tr key={subj.id}>
                <td style={{ fontWeight: 600 }}>{subj.code}</td>
                <td style={{ fontWeight: 500 }}>{subj.name}</td>
                <td>{subj.course_name || 'B.Tech CSE'}</td>
                <td>Sem {subj.semester}</td>
                <td><span className="badge badge-warning">{subj.credits} Credits</span></td>
                <td style={{ fontSize: '0.825rem', color: 'var(--text-secondary)' }}>{subj.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
};
