import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, Users, BookOpen, Calendar, 
  Clock, Bell, ShieldAlert, LogOut, GraduationCap 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Sidebar = () => {
  const { user, logout } = useAuth();
  const role = user?.role;

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard, roles: ['SUPER_ADMIN', 'COLLEGE_ADMIN', 'FACULTY', 'STAFF', 'STUDENT'] },
    { path: '/students', label: 'Students Directory', icon: Users, roles: ['SUPER_ADMIN', 'COLLEGE_ADMIN', 'FACULTY', 'STAFF'] },
    { path: '/academic', label: 'Courses & Subjects', icon: BookOpen, roles: ['SUPER_ADMIN', 'COLLEGE_ADMIN', 'FACULTY', 'STAFF', 'STUDENT'] },
    { path: '/attendance', label: 'Attendance Portal', icon: Calendar, roles: ['SUPER_ADMIN', 'COLLEGE_ADMIN', 'FACULTY', 'STUDENT'] },
    { path: '/timetable', label: 'Timetable Grid', icon: Clock, roles: ['SUPER_ADMIN', 'COLLEGE_ADMIN', 'FACULTY', 'STAFF', 'STUDENT'] },
    { path: '/notices', label: 'Notices & Feed', icon: Bell, roles: ['SUPER_ADMIN', 'COLLEGE_ADMIN', 'FACULTY', 'STAFF', 'STUDENT'] },
    { path: '/audit-logs', label: 'Audit Logs', icon: ShieldAlert, roles: ['SUPER_ADMIN', 'COLLEGE_ADMIN'] },
  ];

  const filteredNav = navItems.filter((item) => item.roles.includes(role));

  return (
    <aside className="sidebar">
      <div style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '12px', borderBottom: '1px solid rgba(255, 255, 255, 0.08)' }}>
        <div style={{ background: 'var(--primary)', padding: '8px', borderRadius: '8px', display: 'flex' }}>
          <GraduationCap size={24} color="#fff" />
        </div>
        <div>
          <h2 className="logo-text" style={{ fontSize: '1.15rem', color: '#fff', fontWeight: 700, lineHeight: 1.2 }}>
            EduCloud
          </h2>
          <span className="logo-text" style={{ fontSize: '0.7rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Multi-Cloud Engine
          </span>
        </div>
      </div>

      <nav style={{ flex: 1, padding: '16px 12px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
        {filteredNav.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              style={({ isActive }) => ({
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                borderRadius: '8px',
                color: isActive ? '#ffffff' : '#94a3b8',
                backgroundColor: isActive ? 'var(--primary)' : 'transparent',
                textDecoration: 'none',
                fontSize: '0.9rem',
                fontWeight: 500,
                transition: 'all 0.2s ease',
              })}
            >
              <Icon size={18} />
              <span className="nav-text">{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div style={{ padding: '16px 12px', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
        <button
          onClick={logout}
          style={{
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '12px 16px',
            borderRadius: '8px',
            color: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            border: 'none',
            cursor: 'pointer',
            fontSize: '0.9rem',
            fontWeight: 500,
          }}
        >
          <LogOut size={18} />
          <span className="nav-text">Sign Out</span>
        </button>
      </div>
    </aside>
  );
};
