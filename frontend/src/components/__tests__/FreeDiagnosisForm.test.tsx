import { render, screen } from '@testing-library/react';
import { FreeDiagnosisForm } from '../FreeDiagnosisForm';
import '@testing-library/jest-dom';

describe('FreeDiagnosisForm', () => {
  it('フォームが正しくレンダリングされる', () => {
    render(<FreeDiagnosisForm />);
    
    expect(screen.getByLabelText('お名前')).toBeInTheDocument();
    expect(screen.getByLabelText('生年月日')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: '無料で占う' })).toBeInTheDocument();
  });
}); 