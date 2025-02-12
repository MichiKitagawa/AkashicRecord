interface ErrorPageProps {
  error: Error | null;
}

export function ErrorPage({ error }: ErrorPageProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full px-6 py-8 bg-white rounded-lg shadow-md">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            エラーが発生しました
          </h1>
          <p className="text-gray-600 mb-8">
            申し訳ありません。予期せぬエラーが発生しました。
            <br />
            しばらく時間をおいて、もう一度お試しください。
          </p>
          <div className="text-sm text-gray-500 mb-4">
            {error?.message}
          </div>
          <button
            onClick={() => window.location.reload()}
            className="bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700"
          >
            ページを再読み込み
          </button>
        </div>
      </div>
    </div>
  );
} 