'use client'
import { Layout } from 'antd'
import Link from 'next/link'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useSetRecoilState, useRecoilValue } from 'recoil'
import { 
  GAME_RELATED_API, 
  GAME_BETS_API, 
  gamesBetsState,
  gamesRelatedState,
  filterBestBetsState,
  filterSafeBetsState
} from '@/hooks/atoms'

export default function LayoutDashboard (
  { children }: 
  { children: React.ReactNode }) {
  const setGamesRelatedState = useSetRecoilState(gamesRelatedState)
  const setGamesBetsState = useSetRecoilState(gamesBetsState)
  const filterBestBets = useRecoilValue(filterBestBetsState)
  const filterSafeBets = useRecoilValue(filterSafeBetsState)
  console.log('bets', filterBestBets, filterSafeBets)
  const { 
    data: gamesRelated, isLoading: isLoadingGamesRelated 
  } = useQuery({
    queryKey: [GAME_RELATED_API],
    queryFn: async () => {
      const res = await fetch(GAME_RELATED_API)
      const data = await res.json()
      setGamesRelatedState(data)
      return data
    }
  })

  const {
    data: gamesBets, isLoading: isLoadingGameBets
  } = useQuery({
    queryKey: [GAME_BETS_API],
    queryFn: async () => {
      const res = await fetch(GAME_BETS_API)
      const data = await res.json()
      setGamesBetsState(data)
      return data
    }
  })
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