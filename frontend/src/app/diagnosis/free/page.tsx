"use client";

import { useState } from 'react';
import { api, FreeDiagnosisRequest } from '@/lib/api';
import { LoadingSpinner } from '@/components/animations/LoadingSpinner';

export default function FreeDiagnosisPage() {
  const [name, setName] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');  // エラーメッセージをリセット
    
    try {
      setIsLoading(true);
      const params: FreeDiagnosisRequest = {
        name,
        birth_date: birthDate,
      };
      const response = await api.createFreeDiagnosis(params);
      setResult(response.result);
    } catch (error) {
      console.error('Error:', error);
      setError('診断中にエラーが発生しました。しばらく待ってから再度お試しください。');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">アカシックAI無料診断</h1>
      
      {isLoading ? (
        <div className="text-center py-8">
          <LoadingSpinner />
          <p className="mt-4 text-gray-600">診断結果を生成中...</p>
        </div>
      ) : !result ? (
        <form onSubmit={handleSubmit} className="max-w-md mx-auto">
          <div className="mb-4">
            <label htmlFor="name" className="block mb-2">
              お名前
            </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full p-2 border rounded"
            />
          </div>

          <div className="mb-6">
            <label htmlFor="birthDate" className="block mb-2">
              生年月日
            </label>
            <input
              type="date"
              id="birthDate"
              value={birthDate}
              onChange={(e) => setBirthDate(e.target.value)}
              required
              className="w-full p-2 border rounded"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 disabled:opacity-50"
          >
            {isLoading ? '診断中...' : '無料診断を開始'}
          </button>

          {error && (
            <p className="mt-4 text-red-600">{error}</p>
          )}
        </form>
      ) : (
        <div className="max-w-2xl mx-auto">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">診断結果</h2>
            <div className="whitespace-pre-wrap">{result}</div>
            <div className="mt-8">
              <button
                onClick={() => setResult(null)}
                className="text-purple-600 hover:text-purple-700"
              >
                新しい診断を始める
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 