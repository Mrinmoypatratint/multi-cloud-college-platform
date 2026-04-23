import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Users, GraduationCap, BookOpen, CheckCircle, Bell, Clock, ArrowUpRight } from 'lucide-react';

export const Dashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/reports/dashboard/');
        setStats(res.data.data);
      } catch (err) {
        console.error('Failed to load dashboard stats', err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return <div className="card">Loading dashboard insights...</div>;
  }

  const metrics = stats?.metrics || {};

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Welcome Banner */}
      <div className="card" style={{ background: 'linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%)', color: '#fff' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ color: '#fff', fontSize: '1.5rem', marginBottom: '4px' }}>
              Welcome back, {user?.full_name || user?.username}!
            </h1>
            <p style={{ color: 'rgba(255, 255, 255, 0.85)', fontSize: '0.9rem' }}>
              Role: <strong>{user?.role?.replace('_', ' ')}</strong> | Multi-Cloud Engine Active (AWS / Azure DR)
            </p>
          </div>
          <span className="badge" style={{ backgroundColor: 'rgba(255, 255, 255, 0.2)', color: '#fff', fontSize: '0.8rem' }}>
            System Status: 100% Operational
          </span>
        </div>
      </div>

      {/* Metric Cards */}
      <div className="grid-4">
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', fontWeight: 500 }}>Total Students</p>
              <h2 style={{ fontSize: '1.75rem', marginTop: '6px' }}>{metrics.total_students || 0}</h2>
            </div>
            <div style={{ padding: '10px', borderRadius: '10px', backgroundColor: 'var(--primary-light)', color: 'var(--primary)' }}>
              <Users size={22} />
            </div>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '12px' }}>
            <ArrowUpRight size={14} /> Active Academic Year 2025-2026
          </p>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', fontWeight: 500 }}>Faculty Members</p>
              <h2 style={{ fontSize: '1.75rem', marginTop: '6px' }}>{metrics.total_faculty || 0}</h2>
            </div>
            <div style={{ padding: '10px', borderRadius: '10px', backgroundColor: 'var(--warning-bg)', color: 'var(--warning)' }}>
              <GraduationCap size={22} />
            </div>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '12px' }}>
            Assigned across 3 Departments
          </p>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', fontWeight: 500 }}>Active Courses</p>
              <h2 style={{ fontSize: '1.75rem', marginTop: '6px' }}>{metrics.total_courses || 0}</h2>
            </div>
            <div style={{ padding: '10px', borderRadius: '10px', backgroundColor: 'var(--accent-light)', color: 'var(--accent)' }}>
              <BookOpen size={22} />
            </div>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '12px' }}>
            Bachelor & Master Programs
          </p>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', fontWeight: 500 }}>Avg Attendance</p>
              <h2 style={{ fontSize: '1.75rem', marginTop: '6px' }}>{metrics.avg_attendance_percentage}%</h2>
            </div>
            <div style={{ padding: '10px', borderRadius: '10px', backgroundColor: 'var(--success-bg)', color: 'var(--success)' }}>
              <CheckCircle size={22} />
            </div>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--success)', marginTop: '12px' }}>
            Above institutional threshold (75%)
          </p>
        </div>
      </div>

      {/* Content Grid */}
      <div className="grid-2">
        {/* Recent Notices */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Bell size={18} color="var(--primary)" /> Campus Announcements
            </h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {(stats?.recent_notices || []).slice(0, 3).map((notice) => (
              <div key={notice.id} style={{ padding: '14px', borderRadius: '8px', backgroundColor: 'var(--bg-primary)', borderLeft: notice.is_pinned ? '4px solid var(--primary)' : '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>{notice.title}</span>
                  <span className={`badge ${notice.priority === 'HIGH' ? 'badge-danger' : 'badge-info'}`}>
                    {notice.priority}
                  </span>
                </div>
                <p style={{ fontSize: '0.825rem', color: 'var(--text-secondary)' }}>{notice.content}</p>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '8px' }}>
                  By {notice.author_name} | Target: {notice.target_role}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Timetable Overview */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Clock size={18} color="var(--accent)" /> Today's Class Schedule
            </h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {(stats?.today_schedule || []).map((slot) => (
              <div key={slot.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 14px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                <div>
                  <span style={{ fontWeight: 600, fontSize: '0.875rem' }}>{slot.subject_code} - {slot.subject_name}</span>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    {slot.day_of_week} ({slot.start_time} - {slot.end_time}) | Room: {slot.room_number}
                  </p>
                </div>
                <span className="badge badge-primary">{slot.faculty_name}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

    </div>
  );
};
