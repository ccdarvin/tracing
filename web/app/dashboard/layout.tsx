'use client'
import { Layout } from 'antd'

export default function LayoutDashboard (
  { children }: 
  { children: React.ReactNode }) {
  return <Layout className="h-screen">
    <div className="h-24">

    </div>
    <Layout.Content>
    {children}
    </Layout.Content>
  </Layout>
}