'use client'
import './globals.css'
import { ConfigProvider } from 'antd'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

export default function Layout({ children }: { children: React.ReactNode }) {

  return <html lang="es">
    <head></head>
    <body>
      <ConfigProvider>
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      </ConfigProvider>
    </body>
  </html>
}