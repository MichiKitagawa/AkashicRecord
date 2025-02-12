# アカシックAI占い

GPT-4を活用した本格的なAI占いサービス

## 機能概要

- 無料診断機能
  - 基本的な運勢診断
  - 名前と生年月日による簡易診断

- 有料診断機能
  - 詳細な運勢診断
  - 複数分野(恋愛、仕事、金運など)の選択式診断
  - 具体的な悩みに対する個別アドバイス
  - PDF形式でのダウンロード機能

## 技術スタック

### フロントエンド
- Next.js
- TypeScript
- Tailwind CSS
- Stripe決済

### バックエンド
- FastAPI (Python)
- GPT-4 API
- PDF生成機能

## 開発環境のセットアップ

### 必要条件
- Node.js 18.x以上
- Python 3.9以上
- npm or yarn

### フロントエンド
```bash
cd frontend
npm install
npm run dev
```

### バックエンド
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 環境変数
`.env`ファイルをフロントエンド・バックエンドそれぞれのディレクトリに作成し、必要な環境変数を設定してください。

## ライセンス
MIT

## 作者
Michi Kitagawa
