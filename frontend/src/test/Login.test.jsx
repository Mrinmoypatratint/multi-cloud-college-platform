import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Login } from '../pages/Login';
import { AuthProvider } from '../context/AuthContext';
import { BrowserRouter } from 'react-router-dom';

describe('Login Page Component', () => {
  it('renders login form and demo account buttons', () => {
    render(
      <AuthProvider>
        <BrowserRouter>
          <Login />
        </BrowserRouter>
      </AuthProvider>
    );

    expect(screen.getByText(/EduCloud Platform/i)).toBeInTheDocument();
    expect(screen.getByText(/Sign In to Portal/i)).toBeInTheDocument();
    expect(screen.getByText(/Super Admin/i)).toBeInTheDocument();
  });
});
