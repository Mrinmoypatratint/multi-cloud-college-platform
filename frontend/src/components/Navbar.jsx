import React from 'react';
import { Sun, Moon, Bell, User as UserIcon } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Navbar = ({ title = 'Dashboard' }) => {
  const { user, theme, toggleTheme } = useAuth();

  const getRoleBadgeColor = (role) => {
    switch (role) {
      case 'SUPER_ADMIN': return 'badge-danger';
      case 'COLLEGE_ADMIN': return 'badge-primary';
      case 'FACULTY': return 'badge-warning';
      case 'STAFF': return 'badge-info';
      case 'STUDENT': return 'badge-success';
      default: return 'badge-secondary';
    }
  };

  return (
    <header className="topbar">
      <div>
        <h1 style={{ fontSize: '1.25rem', fontWeight: 600 }}>{title}</h1>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <button
          onClick={toggleTheme}
          aria-label="Toggle theme"
          className="btn btn-secondary"
          style={{ padding: '8px 12px', borderRadius: '50%' }}
        >
          {theme === 'light' ? <Moon size={18} /> : <Sun size={18} />}
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', borderLeft: '1px solid var(--border-color)', paddingLeft: '16px' }}>
          <div style={{ width: '36px', height: '36px', borderRadius: '50%', backgroundColor: 'var(--primary-light)', color: 'var(--primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 600 }}>
            {user?.first_name ? user.first_name[0].toUpperCase() : <UserIcon size={18} />}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)' }}>
              {user?.full_name || user?.username}
            </span>
            <span className={`badge ${getRoleBadgeColor(user?.role)}`} style={{ fontSize: '0.65rem', alignSelf: 'flex-start' }}>
              {user?.role?.replace('_', ' ')}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};
