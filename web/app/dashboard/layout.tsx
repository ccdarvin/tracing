'use client'
import { Layout } from 'antd'
import Link from 'next/link'


export default function LayoutDashboard (
  { children }: 
  { children: React.ReactNode }) {
  return <Layout className="h-screen">
    <div className="bg-slate-800">
      <div className="flex justify-between md:container mx-auto">
        <div className="flex">
          <Link href="/dashboard" className="text-white px-6 py-4"><span>Dasboard</span></Link>
          <Link href="/dashboard/settings" className="text-white px-6 py-4"><span>Configurar</span></Link>
        </div>
      </div>
    </div>
    <Layout.Content>
    {children}
    </Layout.Content>
  </Layout>
}