
'use client'

import { WEBSITE_API, WEBSITE_WS } from '@/hooks/atoms'
import { Skeleton, Alert, Avatar, Badge, Segmented } from 'antd'
import { useEffect, useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useSelectedLayoutSegment, useRouter } from 'next/navigation'


export default function Layout(
  { children }: { children: React.ReactNode }
){
  const queryClient = useQueryClient()
  const { data: websites, isLoading, isError, refetch } = useQuery({
    // @ts-ignore
    queryKey: [WEBSITE_API],
    queryFn: async () => {
      const res = await fetch(WEBSITE_API)
      return res.json()
    },
  })
  const router = useRouter()
  const [connected, setConnected] = useState(false)
  const [count, setCount] = useState(1)
  const websiteId = useSelectedLayoutSegment()
  useEffect(() => {
    const ws = new WebSocket(WEBSITE_WS)
    ws.onopen = () => {
      console.log('connected')
      setConnected(true)
    }
    ws.onclose = () => {
      console.log('disconnected')
      setConnected(false)
      setTimeout(() => {
        setCount(count + 1)
      }, 1000)
    }
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log(data)
      queryClient.setQueryData([WEBSITE_API], (oldData: any) => {
        return oldData.map((website: any) => {
          if (website.id === data.id) {
            return { ...website, ...data }
          }
          return website
        })
      })
    }
    ws.onerror = (event) => {
      console.log('error', event)
      refetch()
    }
    return () => {
      if (ws.readyState == WebSocket.OPEN) {
        ws.close()
        setConnected(false)
      }
    }
  }, [count])

  console.log(connected, count)
  return <div className="flex justify-center items-center">
    <div className="w-96">
      <Badge.Ribbon 
        text={count}
        color={connected? 'green': 'red'}
      >
        <h1 className="text-xl font-bold py-8">Sitio Web que se estan procesando</h1>
      </Badge.Ribbon>
      { isError && <Alert message="Error" type="error" /> }
      { isLoading ? <Skeleton active />: <Segmented
        onChange={(value) => {
          value? router.push(`/dashboard/websites/${value}`): router.push('/dashboard/websites')
        }}
        defaultValue={websiteId||''}
        options={websites.map((website: any) => ({
          value: website.id,
          label: <div className="flex flex-col items-center gap-1 py-2">
            
                <Avatar src={website.icon} />
            <div>{website.id} <Badge status={website.scraping? 'processing': 'default'} /> </div>
          </div>
        }))}
        />
      }
    </div>
    <div>
      {children}
    </div>
  </div>
}
/*
<List 
          itemLayout="horizontal"
          //@ts-ignore
          dataSource={websites}
          renderItem={(website:any) => <List.Item>
              <List.Item.Meta
                avatar={<Avatar src={website.icon} />}
                title={website.name} />
              <div>
                {website.scraping?  <Tag className="flex items-center" icon={<SyncOutlined spin />} color="processing">
                    Procesando
                  </Tag>:
                  <Tag className="flex items-center" icon={<MinusCircleOutlined />} color="default">
                    Espera
                  </Tag>
                }
              </div>
            </List.Item>
          }
        />
        */