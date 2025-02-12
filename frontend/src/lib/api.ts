/*
File: frontend/src/lib/api.ts
*/

import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 共通の型定義
export interface DiagnosisBase {
  name: string;
  birth_date: string;
}

// 無料診断
export type FreeDiagnosisRequest = {
  name: string;
  birth_date: string;
};

export type FreeDiagnosisResponse = {
  diagnosis_token: string;
  result: string;
};

// 有料診断
export type DetailedDiagnosisRequest = {
  name: string;
  birth_date: string;
  categories: string[];
  free_text?: string;
};

export type DetailedDiagnosisResponse = {
  diagnosis_token: string;
  partial_result: string;
  is_locked: boolean;
};

// 支払い関連の型定義
export type CreateCheckoutSessionResponse = {
  checkout_url: string;
};

// API関数
export const api = {
  // 無料診断APIを呼び出す
  createFreeDiagnosis: async (params: FreeDiagnosisRequest): Promise<FreeDiagnosisResponse> => {
    const { data } = await axios.post<FreeDiagnosisResponse>(
      `${API_BASE_URL}/api/diagnosis/free`,
      params
    );
    return data;
  },

  // 有料診断APIを呼び出す
  createDetailedDiagnosis: async (params: DetailedDiagnosisRequest): Promise<DetailedDiagnosisResponse> => {
    const { data } = await axios.post<DetailedDiagnosisResponse>(
      `${API_BASE_URL}/api/diagnosis/detail`,
      params
    );
    // 診断トークンを保存
    localStorage.setItem('diagnosisToken', data.diagnosis_token);
    return data;
  },

  // 支払い関連のAPIを呼び出す
  createCheckoutSession: async (diagnosisToken: string): Promise<CreateCheckoutSessionResponse> => {
    const { data } = await axios.post<CreateCheckoutSessionResponse>(
      `${API_BASE_URL}/api/payment/create-checkout-session`,
      { diagnosis_token: diagnosisToken }
    );
    return data;
  },

  // PDFダウンロードのAPIを呼び出す
  downloadDiagnosisPDF: async (token: string): Promise<Blob> => {
    const response = await axios.get<Blob>(
      `${API_BASE_URL}/api/diagnosis/${token}/pdf`,
      { responseType: 'blob' }
    );
    return response.data;
  }
};

export { api as diagnosisApi };
