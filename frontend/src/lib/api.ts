import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface FreeDiagnosisRequest {
  name: string;
  birth_date: string;
}

export interface FreeDiagnosisResponse {
  diagnosis_token: string;
  result: string;
}

export interface DetailedDiagnosisRequest {
  name: string;
  birth_date: string;
  categories: string[];
  free_text?: string;
}

export interface DetailedDiagnosisResponse {
  diagnosis_token: string;
  partial_result: string;
  is_locked: boolean;
}

export const diagnosisApi = {
  // 無料診断
  createFreeDiagnosis: async (data: FreeDiagnosisRequest): Promise<FreeDiagnosisResponse> => {
    const response = await api.post<FreeDiagnosisResponse>('/api/diagnosis/free', data);
    return response.data;
  },

  // 有料診断(詳細)
  createDetailedDiagnosis: async (data: DetailedDiagnosisRequest): Promise<DetailedDiagnosisResponse> => {
    const response = await api.post<DetailedDiagnosisResponse>('/api/diagnosis/detail', data);
    return response.data;
  },
};
