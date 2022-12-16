'use client'

import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useSetRecoilState, useRecoilValue } from 'recoil'
import { List, Descriptions, Avatar } from 'antd'
import { 
  GAME_RELATED_API, 
  GAME_BETS_API, 
  gamesBetsState,
  gamesRelatedState,
  filterBestBetsState, 
  getIcon
} from '@/hooks/atoms'


export default function Page () {
  const bestBets = useRecoilValue(filterBestBetsState)
  console.log('best bets', bestBets)

  const Label = (url: any, name: string) => {
    return <div className="flex gap-2 items-center justify-between">
      {url && <Avatar src={getIcon(url)} />}
      <span>{name}</span>
    </div>
  }

  return <div className="md:container mx-auto py-8">
    <h1>Las mejores apuestas</h1>
    <List 
      itemLayout="vertical"
      dataSource={bestBets}
      renderItem={(item: any) => <List.Item key={item.id}>
          <List.Item.Meta title={item.name} />
          <div>
            <Descriptions bordered size="small" layout="horizontal" column={3} title="1x2">
              <Descriptions.Item label={<Label url={item?.bets?.regular_1x2_1?.gameId} name ="1"/>}>{item?.bets?.regular_1x2_1?.bet}</Descriptions.Item>
              <Descriptions.Item label="x">{item?.bets?.regular_1x2_X?.bet}</Descriptions.Item>
              <Descriptions.Item label="2">{item?.bets?.regular_1x2_2?.bet}</Descriptions.Item>
            </Descriptions>
          </div>
        </List.Item>
      }
    />
  </div>
}