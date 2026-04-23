import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Clock, MapPin, User } from 'lucide-react';

export const Timetable = () => {
  const [slots, setSlots] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTimetable = async () => {
      try {
        const res = await api.get('/timetable/slots/');
        setSlots(res.data.results || res.data || []);
      } catch (err) {
        console.error('Failed to load timetable slots', err);
      } finally {
        setLoading(false);
      }
    };
    fetchTimetable();
  }, []);

  const days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div>
        <h2>Weekly Class Timetable Schedule</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
          Weekly schedule grid showing lecture rooms, timings, and course instructors.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '16px' }}>
        {days.map((day) => {
          const daySlots = slots.filter((s) => s.day_of_week === day);
          return (
            <div key={day} className="card" style={{ padding: '16px' }}>
              <h3 style={{ fontSize: '0.9rem', color: 'var(--primary)', marginBottom: '14px', textTransform: 'uppercase', letterSpacing: '0.05em', borderBottom: '2px solid var(--primary-light)', paddingBottom: '6px' }}>
                {day}
              </h3>
              {daySlots.length === 0 ? (
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic', padding: '12px 0' }}>No lectures scheduled</div>
              ) : (
                daySlots.map((slot) => (
                  <div key={slot.id} style={{ padding: '12px', borderRadius: '8px', backgroundColor: 'var(--bg-primary)', marginBottom: '10px', border: '1px solid var(--border-color)' }}>
                    <span className="badge badge-warning" style={{ fontSize: '0.65rem', marginBottom: '6px' }}>
                      {slot.start_time} - {slot.end_time}
                    </span>
                    <h4 style={{ fontSize: '0.875rem', fontWeight: 600, marginTop: '4px' }}>{slot.subject_code}</h4>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{slot.subject_name}</p>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '8px' }}>
                      <span><MapPin size={12} inline /> {slot.room_number}</span>
                      <span><User size={12} inline /> {slot.faculty_name}</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
