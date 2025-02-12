import { api } from '../api';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('API Client', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('createFreeDiagnosis', () => {
    const mockRequest = {
      name: 'テスト太郎',
      birth_date: '2000-01-01',
    };

    const mockResponse = {
      diagnosis_token: 'test-token',
      result: 'テスト診断結果',
    };

    it('正常に診断結果を取得できる', async () => {
      mockedAxios.post.mockResolvedValueOnce({ data: mockResponse });

      const result = await api.createFreeDiagnosis(mockRequest);

      expect(result).toEqual(mockResponse);
      expect(localStorage.getItem('diagnosisToken')).toBe('test-token');
      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/diagnosis/free'),
        mockRequest
      );
    });

    it('APIエラー時に例外をスローする', async () => {
      const error = new Error('API Error');
      mockedAxios.post.mockRejectedValueOnce(error);

      await expect(api.createFreeDiagnosis(mockRequest)).rejects.toThrow('API Error');
    });
  });

  describe('createDetailedDiagnosis', () => {
    const mockRequest = {
      name: 'テスト太郎',
      birth_date: '2000-01-01',
      categories: ['love', 'work'],
      free_text: 'テスト',
    };

    const mockResponse = {
      diagnosis_token: 'test-token',
      partial_result: 'テスト診断結果',
      is_locked: true,
    };

    it('正常に診断結果を取得できる', async () => {
      mockedAxios.post.mockResolvedValueOnce({ data: mockResponse });

      const result = await api.createDetailedDiagnosis(mockRequest);

      expect(result).toEqual(mockResponse);
      expect(localStorage.getItem('diagnosisToken')).toBe('test-token');
      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/diagnosis/detail'),
        mockRequest
      );
    });
  });

  describe('createCheckoutSession', () => {
    it('正常にチェックアウトURLを取得できる', async () => {
      const mockResponse = {
        checkout_url: 'https://checkout.stripe.com/test',
      };
      mockedAxios.post.mockResolvedValueOnce({ data: mockResponse });

      const result = await api.createCheckoutSession('test-token');

      expect(result).toEqual(mockResponse);
      expect(mockedAxios.post).toHaveBeenCalledWith(
        expect.stringContaining('/api/payment/create-checkout-session'),
        { diagnosis_token: 'test-token' }
      );
    });
  });

  describe('downloadDiagnosisPDF', () => {
    it('正常にPDFをダウンロードできる', async () => {
      const mockBlob = new Blob(['test'], { type: 'application/pdf' });
      mockedAxios.get.mockResolvedValueOnce({ data: mockBlob });

      const result = await api.downloadDiagnosisPDF('test-token');

      expect(result).toEqual(mockBlob);
      expect(mockedAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('/api/diagnosis/test-token/pdf'),
        { responseType: 'blob' }
      );
    });
  });
}); 