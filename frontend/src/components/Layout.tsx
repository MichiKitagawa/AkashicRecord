import { Box, Container, Flex, Heading, Link as ChakraLink } from '@chakra-ui/react';
import Link from 'next/link';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout = ({ children }: LayoutProps) => {
  return (
    <Box minH="100vh" bg="gray.50">
      {/* ヘッダー */}
      <Box bg="purple.600" color="white" py={4} mb={8}>
        <Container maxW="container.xl">
          <Flex justify="space-between" align="center">
            <Link href="/" passHref>
              <ChakraLink _hover={{ textDecoration: 'none' }}>
                <Heading size="lg">アカシックAI占い</Heading>
              </ChakraLink>
            </Link>
          </Flex>
        </Container>
      </Box>

      {/* メインコンテンツ */}
      <Container maxW="container.xl" pb={8}>
        {children}
      </Container>

      {/* フッター */}
      <Box bg="gray.100" py={4} mt="auto">
        <Container maxW="container.xl">
          <Flex justify="center" align="center">
            <Box color="gray.600" fontSize="sm">
              © 2025 アカシックAI占い All rights reserved.
            </Box>
          </Flex>
        </Container>
      </Box>
    </Box>
  );
};
