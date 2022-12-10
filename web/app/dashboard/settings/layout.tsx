'use client'
import { Segmented, Avatar } from 'antd'
import { useRouter, usePathname } from 'next/navigation'


export default function Layout (
  { children }: 
  { children: React.ReactNode }
){
  
  const router = useRouter() 
  const pathname = usePathname() || '/dashboard/settings'

  return <div className="md:container mx-auto py-4">
    <div className="flex justify-end">
      <Segmented
        onChange={(value: any) => router.push(value)}
        defaultValue={pathname}
        options={[
          { label: <div className="py-2 px-4 mx-4 flex flex-col gap-1 items-center max-w-sm">
              <span className="text-xl">Juegos</span>
              <span className="text-xs">Relacionar juegos </span>
            </div>, value: '/dashboard/settings'
          },
          { label: <div className="py-2 px-4 mx-4  flex flex-col gap-1 items-center">
              <span className="text-lg">Apuestas</span>
              <span className="text-xs">Estructura de apuestas</span>
            </div>, value: '/dashboard/settings/structure'
          }
        ]}
      />
    </div>
    <div>{children}</div>
  </div>
}