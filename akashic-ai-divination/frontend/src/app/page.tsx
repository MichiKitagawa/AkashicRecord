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

export default function Home() {
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBgColor = useColorModeValue('white', 'gray.800');

  return (
    <Box bg={bgColor}>
      {/* ヒーローセクション */}
      <Box bg="purple.600" color="white" py={20} textAlign="center">
        <Container maxW="container.xl">
          <VStack spacing={6}>
            <Heading size="2xl">アカシックAI占い</Heading>
            <Text fontSize="xl">AIが導く、あなたの運命の道</Text>
          </VStack>
        </Container>
      </Box>

      {/* 特徴セクション */}
      <Box py={20}>
        <Container maxW="container.xl">
          <SimpleGrid columns={{ base: 1, md: 3 }} gap={10}>
            {features.map((feature, index) => (
              <Box
                key={index}
                bg={cardBgColor}
                p={6}
                borderRadius="lg"
                boxShadow="md"
                textAlign="center"
              >
                <Heading size="md" mb={4}>
                  {feature.title}
                </Heading>
                <Text>{feature.description}</Text>
              </Box>
            ))}
          </SimpleGrid>
        </Container>
      </Box>

      {/* 無料診断フォームセクション */}
      <Box py={20} bg="white">
        <Container maxW="container.md">
          <VStack spacing={8} align="stretch">
            <Heading textAlign="center" size="xl" mb={4}>
              無料で占ってみる
            </Heading>
            <Text textAlign="center" fontSize="lg" mb={8}>
              お名前と生年月日を入力するだけで、あなたの運勢を診断します。
            </Text>
            <FreeDiagnosisForm />
          </VStack>
        </Container>
      </Box>
    </Box>
  );
}
