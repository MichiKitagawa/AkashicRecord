'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { api } from '@/lib/api';

export default function DiagnosisCompletePage() {
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [diagnosis, setDiagnosis] = useState<{ result: string } | null>(null);

  useEffect(() => {
    const fetchDiagnosis = async () => {
      const token = searchParams.get('token');
      if (!token) {
        setError('診断情報が見つかりません');
        return;
      }

      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/api/diagnosis/${token}`);
        if (!response.ok) {
          throw new Error('診断結果の取得に失敗しました');
        }
        const data = await response.json();
        setDiagnosis(data);
      } catch (err) {
        setError('診断結果の取得に失敗しました。もう一度お試しください。');
        console.error(err);
      }
    };

    fetchDiagnosis();
  }, [searchParams]);

  const handleDownloadPDF = async () => {
    const token = searchParams.get('token');
    if (!token) {
      setError('診断情報が見つかりません');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const pdfBlob = await api.downloadDiagnosisPDF(token);
      const url = window.URL.createObjectURL(pdfBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `diagnosis-${token}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      setError('PDFのダウンロードに失敗しました。もう一度お試しください。');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">診断結果の確認</h1>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow mb-8">
          <h2 className="text-xl font-semibold mb-4">ご購入ありがとうございます</h2>
          
          {diagnosis && (
            <div className="mb-8 whitespace-pre-wrap">
              <h3 className="text-lg font-semibold mb-2">診断結果</h3>
              <p className="text-gray-700 dark:text-gray-300">{diagnosis.result}</p>
            </div>
          )}

          <div className="space-y-4">
            <button
              onClick={handleDownloadPDF}
              disabled={isLoading}
              className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 disabled:opacity-50"
            >
              {isLoading ? 'ダウンロード中...' : 'PDFをダウンロード'}
            </button>
          </div>

          {error && (
            <p className="mt-4 text-red-600">{error}</p>
          )}
        </div>
      </div>
    </div>
  );
} 