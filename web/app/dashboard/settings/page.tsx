'use client'
import { Avatar, Form, Input, AutoComplete, Table,  Skeleton, Button, message } from 'antd'
import { WEBSITE_API, GAME_RELATED_API, GAME_API } from '@/hooks/atoms'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import slugify from 'slugify'


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
  return <div className="flex flex-col gap-4">
    <div>
      <h1 className="text-xl font-bold">Crear y relacionar juegos</h1>
      <h2>Relacionar los juegos en las distintas casas de apuesta</h2>
    </div>
    <div>
      <Form
        form={form}
        className="flex gap-4 max-w-lg"
        onFinish={async (values:any) => {
          if (selectedGames.length === 0) {
            message.error('Por favor seleccione un juego en cada casa de apuesta')
            return
          }
          const related = selectedGames.map((game: any) => game.key)
          const body = { ...values, related, id: slugify(values.name) }
          const res = await fetch(GAME_RELATED_API, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
          })
          if (res.ok) {
            form.resetFields()
            setSelectedGames([])
            refetch()
            message.success('Juego creado')
          }

        }}
      >
        <Form.Item
          label="Nombre de juego"
          name="name"
          className="grow"
          rules={[{ required: true, message: 'Por favor ingrese el nombre del juego' }]}
        >
          <AutoComplete 
            options={games?.map((game: any) => ({ value: game.fullName }))}
          />
        </Form.Item>
        <Button htmlType="submit">Guardar</Button>
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