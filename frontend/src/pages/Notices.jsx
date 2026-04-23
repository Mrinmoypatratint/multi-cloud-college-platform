import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Bell, Pin, Plus, Calendar, AlertCircle } from 'lucide-react';

export const Notices = () => {
  const { user } = useAuth();
  const [notices, setNotices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [formData, setFormData] = useState({
    title: '',
    content: '',
    target_role: 'ALL',
    priority: 'NORMAL',
    is_pinned: false
  });

  const fetchNotices = async () => {
    try {
      const res = await api.get('/notices/');
      setNotices(res.data.results || res.data || []);
    } catch (err) {
      console.error('Failed to fetch notices', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotices();
  }, []);

  const handleCreateNotice = async (e) => {
    e.preventDefault();
    try {
      await api.post('/notices/', formData);
      setShowModal(false);
      fetchNotices();
      setFormData({ title: '', content: '', target_role: 'ALL', priority: 'NORMAL', is_pinned: false });
    } catch (err) {
      alert('Failed to publish notice.');
    }
  };

  const isStaff = ['SUPER_ADMIN', 'COLLEGE_ADMIN', 'STAFF'].includes(user?.role);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2>Notices & Announcements Board</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Official college announcements, academic notices, and department updates.
          </p>
        </div>
        {isStaff && (
          <button onClick={() => setShowModal(true)} className="btn btn-primary">
            <Plus size={18} /> Publish New Notice
          </button>
        )}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {loading ? (
          <div className="card">Loading announcements...</div>
        ) : notices.length === 0 ? (
          <div className="card" style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '30px' }}>
            No active announcements for your role.
          </div>
        ) : (
          notices.map((n) => (
            <div key={n.id} className="card" style={{ borderLeft: n.is_pinned ? '5px solid var(--primary)' : '1px solid var(--border-color)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  {n.is_pinned && <Pin size={18} color="var(--primary)" fill="var(--primary)" />}
                  <h3 style={{ fontSize: '1.1rem' }}>{n.title}</h3>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <span className={`badge ${n.priority === 'HIGH' || n.priority === 'URGENT' ? 'badge-danger' : 'badge-info'}`}>
                    {n.priority}
                  </span>
                  <span className="badge badge-secondary">{n.target_role}</span>
                </div>
              </div>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
                {n.content}
              </p>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '16px', borderTop: '1px solid var(--border-color)', paddingTop: '10px' }}>
                <span>Published by: {n.author_name}</span>
                <span>Date: {new Date(n.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Publish Notice Modal */}
      {showModal && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div className="card" style={{ width: '100%', maxWidth: '550px', backgroundColor: 'var(--bg-card)', padding: '30px' }}>
            <h3 style={{ marginBottom: '16px' }}>Publish New Announcement</h3>
            <form onSubmit={handleCreateNotice}>
              <div className="form-group">
                <label>Notice Title</label>
                <input type="text" required value={formData.title} onChange={(e) => setFormData({ ...formData, title: e.target.value })} />
              </div>
              <div className="grid-2">
                <div className="form-group">
                  <label>Target Audience</label>
                  <select value={formData.target_role} onChange={(e) => setFormData({ ...formData, target_role: e.target.value })}>
                    <option value="ALL">All Users</option>
                    <option value="STUDENT">Students Only</option>
                    <option value="FACULTY">Faculty Only</option>
                    <option value="STAFF">Staff Only</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Priority</label>
                  <select value={formData.priority} onChange={(e) => setFormData({ ...formData, priority: e.target.value })}>
                    <option value="LOW">Low</option>
                    <option value="NORMAL">Normal</option>
                    <option value="HIGH">High</option>
                    <option value="URGENT">Urgent</option>
                  </select>
                </div>
              </div>
              <div className="form-group">
                <label>Content</label>
                <textarea rows="4" required value={formData.content} onChange={(e) => setFormData({ ...formData, content: e.target.value })} />
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
                <input type="checkbox" id="pinned" checked={formData.is_pinned} onChange={(e) => setFormData({ ...formData, is_pinned: e.target.checked })} style={{ width: 'auto' }} />
                <label htmlFor="pinned" style={{ cursor: 'pointer', margin: 0 }}>Pin this announcement to top of feed</label>
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
                <button type="button" onClick={() => setShowModal(false)} className="btn btn-secondary">Cancel</button>
                <button type="submit" className="btn btn-primary">Publish Notice</button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
