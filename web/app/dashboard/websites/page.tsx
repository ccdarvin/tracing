'use client'

import { WEBSITE_API, WEBSITE_WS } from '../../../hooks/atoms'
import { Skeleton, List, Alert, Avatar, Tag } from 'antd'  
import { MinusCircleOutlined, SyncOutlined } from '@ant-design/icons'
import { useEffect, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'



export default function Page () {
  const queryClient = useQueryClient()
  const { data: websites, isLoading, isError } = useQuery({
    // @ts-ignore
    queryKey: [WEBSITE_API],
    queryFn: async () => {
      const res = await fetch(WEBSITE_API)
      return res.json()
    },
  })
  useEffect(() => {
    const ws = new WebSocket(WEBSITE_WS)
    ws.onopen = () => {
      console.log('connected')
    }
    ws.onclose = () => {
      console.log('disconnected')
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
    return () => {
      if (ws.readyState == WebSocket.OPEN) {
        ws.close()
      }
    }
  }, [queryClient])


  return <div className="flex justify-center items-center">
    <div className="w-96">
      <h1 className="text-xl font-bold py-8">Sitio Web que se estan procesando</h1>
      { isError && <Alert message="Error" type="error" /> }
      { isLoading ? <Skeleton active />:
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
      }
    </div>
  </div>
}