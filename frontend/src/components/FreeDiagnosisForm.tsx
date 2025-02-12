/*
File: frontend/src/components/FreeDiagnosisForm.tsx
*/
'use client';

import { useState } from 'react';
import {
  Box,
  Button,
  Stack,
  Input,
  Text,
  FormControl,
  FormLabel,
  useToast,
} from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { diagnosisApi } from '../lib/api';

// バリデーションスキーマ
const schema = yup.object({
  name: yup.string()
    .required('名前は必須です')
    .min(2, '名前は2文字以上で入力してください'),
  birth_date: yup.date()
    .required('生年月日は必須です')
    .max(new Date(), '未来の日付は入力できません')
    .min(new Date('1900-01-01'), '1900年以降の日付を入力してください')
    .typeError('正しい日付形式で入力してください'),
}).required();

type FreeDiagnosisFormData = {
  name: string;
  birth_date: Date;
};

interface DiagnosisResult {
  diagnosis_token: string;
  result: string;
}

export const FreeDiagnosisForm = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DiagnosisResult | null>(null);
  const toast = useToast();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<FreeDiagnosisFormData>({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data: FreeDiagnosisFormData) => {
    try {
      setLoading(true);
      // 日付をYYYY-MM-DD形式の文字列に変換
      const formattedData = {
        name: data.name,
        birth_date: data.birth_date.toISOString().split('T')[0],
      };
      
      console.log('Submitting data:', formattedData);
      const response = await diagnosisApi.createFreeDiagnosis(formattedData);
      console.log('API Response:', response);
      
      setResult(response);
      toast({
        title: '診断が完了しました',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (err) {
      console.error('API Error:', err);
      toast({
        title: 'エラーが発生しました',
        description: '診断の生成に失敗しました。もう一度お試しください。',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    reset();
  };

  return (
    <Box maxW="600px" mx="auto" p={4}>
      {!result ? (
        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={6}>
            <FormControl isInvalid={!!errors.name}>
              <FormLabel>お名前</FormLabel>
              <Input 
                {...register('name')} 
                placeholder="山田 太郎" 
                autoComplete="name"
                isDisabled={loading}
              />
              {errors.name && (
                <Text color="red.500" fontSize="sm" mt={1}>
                  {errors.name.message}
                </Text>
              )}
            </FormControl>

            <FormControl isInvalid={!!errors.birth_date}>
              <FormLabel>生年月日</FormLabel>
              <Input 
                {...register('birth_date')} 
                type="date" 
                max={new Date().toISOString().split('T')[0]}
                min="1900-01-01"
                isDisabled={loading}
              />
              {errors.birth_date && (
                <Text color="red.500" fontSize="sm" mt={1}>
                  {errors.birth_date.message}
                </Text>
              )}
            </FormControl>

            <Button
              type="submit"
              colorScheme="purple"
              size="lg"
              isLoading={loading}
              loadingText="診断中..."
              disabled={loading}
            >
              無料で占う
            </Button>
          </Stack>
        </form>
      ) : (
        <Box 
          mt={8} 
          p={6} 
          bg="white" 
          borderRadius="md" 
          boxShadow="md"
          position="relative"
        >
          <Text 
            fontSize="lg" 
            fontWeight="bold" 
            mb={4}
          >
            診断結果
          </Text>
          <Text 
            whiteSpace="pre-wrap" 
            mb={6}
            lineHeight="1.8"
          >
            {result.result}
          </Text>
          <Button
            colorScheme="purple"
            variant="outline"
            onClick={handleReset}
            w="full"
          >
            もう一度占う
          </Button>
        </Box>
      )}
    </Box>
  );
};
