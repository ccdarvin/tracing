'use client'
import { Avatar, Form, Input, Table,  Skeleton } from 'antd'
import { WEBSITE_API, WEBSITE_WS, GAME_API } from '@/hooks/atoms'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'


export default function Page() {
  const { data: websites, isLoading, isError, refetch } = useQuery({
    // @ts-ignore
    queryKey: [WEBSITE_API],
    queryFn: async () => {
      const res = await fetch(WEBSITE_API)
      return res.json()
    },
  })
  const [selectedGames, setSelectedGames] = useState<any[]>([])

  const [form] = Form.useForm()
  const name = Form.useWatch('name', form)
  const { data: games, isLoading: isLoadingGames, isError: isErrorGames, refetch: refetchGames } = useQuery({
    // @ts-ignore
    queryKey: [GAME_API, name],
    queryFn: async () => {
      let result: any[] = []
      if (name && name.length >= 2) {
        const data = await (await fetch(`${GAME_API}?q=${name}`)).json()
        result.push(...data)
      }
      // add selected games if not exists
      selectedGames.forEach((game: any) => {
        if (!result.find((item: any) => item.id === game.id)) {
          result.unshift(game)
        }
      })
      return result
    },
  })
  console.log(websites)
  return <div className="flex flex-col gap-4">
    <div>
      <h1 className="text-xl font-bold">Crear y relacionar juegos</h1>
      <h2>Relacionar los juegos en las distintas casas de apuesta</h2>
    </div>
    <div>
      <Form
        form={form}
      >
        <Form.Item
          label="Nombre de juego"
          name="name"
        >
          <Input className="block max-w-sm" />
        </Form.Item>
      </Form>
    </div>
    <div className="flex gap-4">
      {
        isLoading ? <><Skeleton active /><Skeleton active /><Skeleton active /></> :
        websites.map((website: any) => <div key={website.id} className="max-w-sm w-full">
          <Table
            loading={isLoadingGames}
            rowSelection={{
              type: 'radio',
              onChange: (selectedRowKeys, selectedRows) => {
                // add if not esists
                setSelectedGames(selectedGames.filter((game: any) => game.websiteId !== website.id).concat(selectedRows))
              }
            }}
            columns={[
              {
                title: <div className="flex gap-2 items-center">
                  <Avatar size="small" src={website.icon} />
                  <div>{website.id}</div>
                  <div><span className="text-xs text-primary-400">{website.gameCount}</span></div>
                </div>,
                dataIndex: 'fullName',
                key: 'fullName',
              },
            ]}
            dataSource={games?.filter((game: any) => game.websiteId === website.id)}
          />
        </div>)
      }
    </div>
  </div>
}