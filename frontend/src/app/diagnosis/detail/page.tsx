'use client';

import { useState } from 'react';
import { api, DetailedDiagnosisRequest } from '@/lib/api';

const DIAGNOSIS_CATEGORIES = [
  { id: 'love', label: '恋愛' },
  { id: 'work', label: '仕事' },
  { id: 'money', label: '金運' },
  { id: 'health', label: '健康' },
  { id: 'family', label: '家族' },
  { id: 'future', label: '将来' },
];

export default function DetailedDiagnosisPage() {
  const [name, setName] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [freeText, setFreeText] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedCategories.length === 0) {
      setError('占いたい項目を1つ以上選択してください');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const params: DetailedDiagnosisRequest = {
        name,
        birth_date: birthDate,
        categories: selectedCategories,
        free_text: freeText,
      };
      const response = await api.createDetailedDiagnosis(params);
      setResult(response.partial_result);
    } catch (err) {
      setError('診断中にエラーが発生しました。もう一度お試しください。');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleCategory = (categoryId: string) => {
    setSelectedCategories(prev => 
      prev.includes(categoryId)
        ? prev.filter(id => id !== categoryId)
        : [...prev, categoryId]
    );
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">アカシックAI詳細診断</h1>
      
      {!result ? (
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

          <div className="mb-6">
            <label className="block mb-2">
              占いたい項目（複数選択可）
            </label>
            <div className="grid grid-cols-2 gap-2">
              {DIAGNOSIS_CATEGORIES.map(category => (
                <label
                  key={category.id}
                  className="flex items-center space-x-2 cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={selectedCategories.includes(category.id)}
                    onChange={() => toggleCategory(category.id)}
                    className="form-checkbox"
                  />
                  <span>{category.label}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="mb-6">
            <label htmlFor="freeText" className="block mb-2">
              具体的な相談内容（任意）
            </label>
            <textarea
              id="freeText"
              value={freeText}
              onChange={(e) => setFreeText(e.target.value)}
              className="w-full p-2 border rounded h-32"
              placeholder="具体的な悩みや状況があればご記入ください"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700 disabled:opacity-50"
          >
            {isLoading ? '診断中...' : '詳細診断を開始'}
          </button>

          {error && (
            <p className="mt-4 text-red-600">{error}</p>
          )}
        </form>
      ) : (
        <div className="max-w-2xl mx-auto">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">診断結果（プレビュー）</h2>
            <div className="whitespace-pre-wrap">{result}</div>
            <div className="mt-8 space-y-4">
              <button
                onClick={() => window.location.href = '/payment'}
                className="w-full bg-purple-600 text-white py-2 px-4 rounded hover:bg-purple-700"
              >
                詳細な結果を見る（有料）
              </button>
              <button
                onClick={() => setResult(null)}
                className="w-full text-purple-600 hover:text-purple-700"
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