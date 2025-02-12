/*
File: frontend/src/components/DetailedDiagnosisForm.tsx
*/
'use client';

import { useState } from 'react';
import {
  Box,
  Button,
  Stack,
  Text,
  FormControl,
  FormLabel,
  Checkbox,
  CheckboxGroup,
  Textarea,
  useToast,
} from '@chakra-ui/react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { diagnosisApi, DetailedDiagnosisResponse, DiagnosisBase } from '../lib/api';

// 占い分野の選択肢
const FORTUNE_CATEGORIES = [
  { id: 'love', label: '恋愛運' },
  { id: 'career', label: '仕事運' },
  { id: 'money', label: '金運' },
  { id: 'health', label: '健康運' },
  { id: 'family', label: '家族運' },
] as const;

type CategoryId = typeof FORTUNE_CATEGORIES[number]['id'];

// バリデーションスキーマ
const schema = yup.object().shape({
  categories: yup
    .array()
    .of(yup.string().required())
    .min(1, '少なくとも1つの分野を選択してください')
    .required('占いたい分野を選択してください'),
  free_text: yup
    .string()
    .required('具体的な悩みや状況を入力してください')
    .min(10, '10文字以上入力してください')
    .max(1000, '1000文字以内で入力してください'),
});

type DetailedDiagnosisFormData = yup.InferType<typeof schema>;

interface Props {
  onComplete: (result: DetailedDiagnosisResponse) => void;
  initialData: DiagnosisBase;
}

export const DetailedDiagnosisForm = ({ onComplete, initialData }: Props) => {
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const {
    control,
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<DetailedDiagnosisFormData>({
    resolver: yupResolver(schema),
    defaultValues: {
      categories: [],
      free_text: '',
    },
  });

  const onSubmit = async (data: DetailedDiagnosisFormData) => {
    try {
      setLoading(true);
      
      // 初期データと組み合わせてリクエスト
      const requestData = {
        ...initialData,
        ...data,
      };
      
      console.log('Submitting detailed diagnosis:', requestData);
      const response = await diagnosisApi.createDetailedDiagnosis(requestData);
      console.log('API Response:', response);
      
      onComplete(response);
      
      toast({
        title: '診断が完了しました',
        description: '結果をご確認ください',
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

  return (
    <Box maxW="600px" mx="auto" p={4}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <Stack spacing={6}>
          <FormControl isInvalid={!!errors.categories}>
            <FormLabel>占いたい分野(複数選択可)</FormLabel>
            <Controller
              name="categories"
              control={control}
              render={({ field: { onChange, value } }) => (
                <CheckboxGroup
                  colorScheme="purple"
                  value={value}
                  onChange={(values: CategoryId[]) => onChange(values)}
                >
                  <Stack spacing={3}>
                    {FORTUNE_CATEGORIES.map((category) => (
                      <Checkbox
                        key={category.id}
                        value={category.id}
                        isDisabled={loading}
                      >
                        {category.label}
                      </Checkbox>
                    ))}
                  </Stack>
                </CheckboxGroup>
              )}
            />
            {errors.categories && (
              <Text color="red.500" fontSize="sm" mt={1}>
                {errors.categories.message}
              </Text>
            )}
          </FormControl>

          <FormControl isInvalid={!!errors.free_text}>
            <FormLabel>具体的な悩みや状況</FormLabel>
            <Textarea
              {...register('free_text')}
              placeholder="現在の状況や、特に気になっていることを具体的にお書きください。"
              rows={6}
              resize="vertical"
              isDisabled={loading}
            />
            {errors.free_text && (
              <Text color="red.500" fontSize="sm" mt={1}>
                {errors.free_text.message}
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
            詳細診断を実行
          </Button>
        </Stack>
      </form>
    </Box>
  );
};
