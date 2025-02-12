export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">アカシックAI占い</h3>
            <p className="text-gray-400">
              AIが導く、あなたの運命の道
            </p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">メニュー</h3>
            <ul className="space-y-2">
              <li>
                <a href="/" className="text-gray-400 hover:text-white">
                  ホーム
                </a>
              </li>
              <li>
                <a href="/diagnosis/free" className="text-gray-400 hover:text-white">
                  無料診断
                </a>
              </li>
              <li>
                <a href="/diagnosis/detail" className="text-gray-400 hover:text-white">
                  詳細診断
                </a>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4">お問い合わせ</h3>
            <p className="text-gray-400">
              ご質問やご要望がございましたら、お気軽にお問い合わせください。
            </p>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 アカシックAI占い. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
} 