'use client';

import { useState } from 'react';
import { api } from '@/lib/api';

export default function PaymentPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePayment = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const diagnosisToken = localStorage.getItem('diagnosisToken');
      if (!diagnosisToken) {
        throw new Error('診断情報が見つかりません');
      }

      const response = await api.createCheckoutSession(diagnosisToken);
      window.location.href = response.checkout_url;
    } catch (err) {
      setError('決済の開始に失敗しました。もう一度お試しください。');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-md mx-auto">
        <h1 className="text-2xl font-bold mb-6">詳細診断の購入</h1>

        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow mb-8">
          <h2 className="text-xl font-semibold mb-4">ご購入内容</h2>
          <div className="space-y-4">
            <div className="flex justify-between">
              <span>アカシックAI詳細診断</span>
              <span>¥1,000</span>
            </div>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              ※ 診断結果の全文表示とPDFダウンロードが可能になります
            </div>
          </div>
        </div>

        <button
          onClick={handlePayment}
          disabled={isLoading}
          className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 disabled:opacity-50"
        >
          {isLoading ? '処理中...' : '購入する'}
        </button>

        {error && (
          <p className="mt-4 text-red-600">{error}</p>
        )}
      </div>
    </div>
  );
} 