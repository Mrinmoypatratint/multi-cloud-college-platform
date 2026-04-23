import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { GraduationCap, Lock, User, ArrowRight, AlertCircle } from 'lucide-react';

export const Login = () => {
  const [username, setUsername] = useState('superadmin');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid username or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const setDemoAccount = (demoUsername) => {
    setUsername(demoUsername);
    setPassword('admin123');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--bg-primary)', padding: '20px' }}>
      <div style={{ width: '100%', maxWidth: '440px', backgroundColor: 'var(--bg-card)', padding: '40px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-color)', boxShadow: 'var(--shadow-lg)' }}>
        
        <div style={{ textAlign: 'center', marginBottom: '28px' }}>
          <div style={{ display: 'inline-flex', background: 'var(--primary)', padding: '12px', borderRadius: '12px', marginBottom: '16px' }}>
            <GraduationCap size={32} color="#fff" />
          </div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700 }}>EduCloud Platform</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginTop: '4px' }}>
            Multi-Cloud College Management & Student Services
          </p>
        </div>

        {error && (
          <div style={{ padding: '12px 16px', borderRadius: 'var(--radius-sm)', backgroundColor: 'var(--danger-bg)', color: 'var(--danger)', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Username</label>
            <div style={{ position: 'relative' }}>
              <User size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={{ paddingLeft: '38px' }}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div style={{ position: 'relative' }}>
              <Lock size={18} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ paddingLeft: '38px' }}
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', padding: '12px', marginTop: '12px', fontSize: '0.95rem' }}
          >
            {loading ? 'Authenticating...' : 'Sign In to Portal'}
            <ArrowRight size={18} />
          </button>
        </form>

        <div style={{ marginTop: '28px', paddingTop: '20px', borderTop: '1px solid var(--border-color)' }}>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '10px', textAlign: 'center', fontWeight: 600, textTransform: 'uppercase' }}>
            Quick Demo Accounts (Click to test RBAC)
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', justifyContent: 'center' }}>
            <button onClick={() => setDemoAccount('superadmin')} className="badge badge-danger" style={{ cursor: 'pointer', border: 'none' }}>Super Admin</button>
            <button onClick={() => setDemoAccount('collegeadmin')} className="badge badge-primary" style={{ cursor: 'pointer', border: 'none' }}>College Admin</button>
            <button onClick={() => setDemoAccount('dr_smith')} className="badge badge-warning" style={{ cursor: 'pointer', border: 'none' }}>Faculty</button>
            <button onClick={() => setDemoAccount('staff_john')} className="badge badge-info" style={{ cursor: 'pointer', border: 'none' }}>Staff</button>
            <button onClick={() => setDemoAccount('alice_student')} className="badge badge-success" style={{ cursor: 'pointer', border: 'none' }}>Student</button>
          </div>
        </div>

      </div>
    </div>
  );
};
