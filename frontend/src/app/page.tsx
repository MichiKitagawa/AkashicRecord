/*
File: frontend/src/app/page.tsx
*/
'use client';

import {
  Box,
  Container,
  Heading,
  Text,
  VStack,
  SimpleGrid,
  useColorModeValue,
} from '@chakra-ui/react';
import { FreeDiagnosisForm } from '@/components/FreeDiagnosisForm';
import Image from 'next/image';
import Link from 'next/link';
import { FadeIn } from '@/components/animations/FadeIn';

const features = [
  {
    title: 'AIが導く運命',
    description: '最新のAI技術を駆使して、あなたの運命を読み解きます。',
  },
  {
    title: '詳細な占い結果',
    description: '総合運、恋愛運、仕事運、金運など、多角的な視点からの診断を提供。',
  },
  {
    title: '即座に結果表示',
    description: '待ち時間なし。診断結果をすぐに確認できます。',
  },
];

export default function HomePage() {
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBgColor = useColorModeValue('white', 'gray.800');

  return (
    <div className="min-h-screen">
      {/* ヒーローセクション */}
      <FadeIn>
        <section className="relative bg-gradient-to-b from-purple-900 to-purple-600 text-white py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-4xl md:text-6xl font-bold mb-6">
                アカシックレコードがあなたの運命を導く
              </h1>
              <p className="text-xl md:text-2xl mb-8">
                AIが読み解く、あなただけの人生の道しるべ
              </p>
              <Link
                href="/diagnosis/free"
                className="inline-block bg-white text-purple-600 px-8 py-4 rounded-full text-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                無料で診断を始める
              </Link>
            </div>
          </div>
        </section>
      </FadeIn>

      {/* 特徴セクション */}
      <section className="py-20 bg-white">
        <FadeIn>
          <h2 className="text-3xl font-bold text-center mb-12">
            アカシックAI占いの特徴
          </h2>
        </FadeIn>
        <div className="grid md:grid-cols-3 gap-8">
          <FadeIn delay={0.2}>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🔮</span>
              </div>
              <h3 className="text-xl font-semibold mb-4">高精度な診断</h3>
              <p className="text-gray-600">
                最新のAI技術を駆使し、アカシックレコードから精密な情報を読み取ります
              </p>
            </div>
          </FadeIn>
          <FadeIn delay={0.4}>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📱</span>
              </div>
              <h3 className="text-xl font-semibold mb-4">手軽に利用可能</h3>
              <p className="text-gray-600">
                スマートフォンやPCから、いつでもどこでも占いを受けることができます
              </p>
            </div>
          </FadeIn>
          <FadeIn delay={0.6}>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="text-xl font-semibold mb-4">具体的なアドバイス</h3>
              <p className="text-gray-600">
                運勢だけでなく、具体的な行動指針まで提供します
              </p>
            </div>
          </FadeIn>
        </div>
      </section>

      {/* 診断の流れセクション */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">
            診断の流れ
          </h2>
          <div className="max-w-3xl mx-auto">
            <div className="flex flex-col space-y-8">
              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center flex-shrink-0">
                  1
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">基本情報の入力</h3>
                  <p className="text-gray-600">
                    お名前と生年月日を入力するだけで、無料診断を受けることができます
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center flex-shrink-0">
                  2
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">AIによる診断</h3>
                  <p className="text-gray-600">
                    アカシックレコードからAIが情報を読み取り、あなたの運勢を診断します
                  </p>
                </div>
              </div>
              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center flex-shrink-0">
                  3
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">詳細な結果</h3>
                  <p className="text-gray-600">
                    総合運、恋愛運、仕事運など、各分野の運勢と具体的なアドバイスを提供します
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTAセクション */}
      <section className="py-20 bg-purple-900 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-8">
            あなたの運命の道を見つけましょう
          </h2>
          <div className="space-y-4 md:space-y-0 md:space-x-4">
            <Link
              href="/diagnosis/free"
              className="inline-block bg-white text-purple-600 px-8 py-4 rounded-full text-lg font-semibold hover:bg-gray-100 transition-colors"
            >
              無料診断を試す
            </Link>
            <Link
              href="/diagnosis/detail"
              className="inline-block bg-transparent border-2 border-white text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-white hover:text-purple-600 transition-colors"
            >
              詳細診断を見る
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
