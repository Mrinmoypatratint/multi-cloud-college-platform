import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { ShieldAlert, RefreshCw } from 'lucide-react';

export const AuditLogs = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchAuditLogs = async () => {
    setLoading(true);
    try {
      const res = await api.get('/audit/logs/');
      setLogs(res.data.results || res.data || []);
    } catch (err) {
      console.error('Failed to fetch audit logs', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAuditLogs();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2>Security & System Audit Logs</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Immutable activity log tracking API mutations, administrative actions, and IP addresses.
          </p>
        </div>
        <button onClick={fetchAuditLogs} className="btn btn-secondary">
          <RefreshCw size={16} /> Refresh Trail
        </button>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>User</th>
              <th>Role</th>
              <th>HTTP Method</th>
              <th>Endpoint Path</th>
              <th>IP Address</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan="7" style={{ textAlign: 'center', padding: '24px' }}>Loading audit logs...</td></tr>
            ) : logs.length === 0 ? (
              <tr><td colSpan="7" style={{ textAlign: 'center', padding: '24px', color: 'var(--text-muted)' }}>No audit events logged yet.</td></tr>
            ) : (
              logs.map((log) => (
                <tr key={log.id}>
                  <td style={{ fontSize: '0.8rem' }}>{new Date(log.created_at).toLocaleString()}</td>
                  <td style={{ fontWeight: 600 }}>{log.username}</td>
                  <td><span className="badge badge-info">{log.user_role}</span></td>
                  <td>
                    <span className={`badge ${log.method === 'POST' ? 'badge-primary' : log.method === 'DELETE' ? 'badge-danger' : 'badge-warning'}`}>
                      {log.method}
                    </span>
                  </td>
                  <td style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{log.path}</td>
                  <td style={{ fontSize: '0.8rem' }}>{log.ip_address || '127.0.0.1'}</td>
                  <td>
                    <span className={`badge ${log.status_code < 400 ? 'badge-success' : 'badge-danger'}`}>
                      {log.status_code}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
