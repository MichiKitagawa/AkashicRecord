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
  name: yup.string().required('名前は必須です'),
  birth_date: yup.string().required('生年月日は必須です'),
}).required();

type FreeDiagnosisFormData = yup.InferType<typeof schema>;

export const FreeDiagnosisForm = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const toast = useToast();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FreeDiagnosisFormData>({
    resolver: yupResolver(schema),
  });

  const onSubmit = async (data: FreeDiagnosisFormData) => {
    try {
      setLoading(true);
      const response = await diagnosisApi.createFreeDiagnosis(data);
      setResult(response.result);
    } catch (err) {
      toast({
        title: 'エラーが発生しました',
        description: '診断の生成に失敗しました。もう一度お試しください。',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Stack spacing={4}>
          <FormControl isInvalid={!!errors.name}>
            <FormLabel>お名前</FormLabel>
            <Input {...register('name')} placeholder="山田 太郎" />
            {errors.name && (
              <Text color="red.500" fontSize="sm">
                {errors.name.message}
              </Text>
            )}
          </FormControl>

          <FormControl isInvalid={!!errors.birth_date}>
            <FormLabel>生年月日</FormLabel>
            <Input {...register('birth_date')} type="date" />
            {errors.birth_date && (
              <Text color="red.500" fontSize="sm">
                {errors.birth_date.message}
              </Text>
            )}
          </FormControl>

          <Button
            type="submit"
            colorScheme="purple"
            size="lg"
            isLoading={loading}
          >
            無料で占う
          </Button>
        </Stack>
      </form>

      {result && (
        <Box mt={8} p={6} bg="white" borderRadius="md" boxShadow="md">
          <Text whiteSpace="pre-wrap">{result}</Text>
          <Button
            mt={4}
            colorScheme="purple"
            variant="outline"
            onClick={() => setResult(null)}
          >
            もう一度占う
          </Button>
        </Box>
      )}
    </Box>
  );
};
