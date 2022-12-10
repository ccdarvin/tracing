'use client'

import { Segmented, Avatar } from 'antd'



export default function Layout (
  { children }: 
  { children: React.ReactNode }) {
  return <div className="md:container mx-auto">
    <div className="flex justify-center">
      <Segmented 
        options={[
          { label: <div className="py-2 px-4 mx-4 flex flex-col gap-1 items-center">
              <Avatar size="large"></Avatar>
              <span className="text-xl">Dasboard</span>
            </div>, value: '/'
          },
          { label: <div className="py-2 px-4 mx-4  flex flex-col gap-1 items-center">
              <Avatar size="large" className="bg-blue-700">B</Avatar>
              <span className="text-xl">La mejor</span>
            </div>, value: '/best'
          },
          { label: <div className="py-2 px-4 mx-4 flex flex-col gap-1 items-center bg-green-600-400">
              <Avatar size="large" className="bg-green-700">S</Avatar>
              <span className="text-xl">Segura</span>
            </div>, value: '/safe'
          },
        ]}
      />
    </div>
    <div>{children}</div>
  </div>
}