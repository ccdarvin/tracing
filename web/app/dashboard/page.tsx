'use client'

import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useSetRecoilState, useRecoilValue } from 'recoil'
import { 
  GAME_RELATED_API, 
  GAME_BETS_API, 
  gamesBetsState,
  gamesRelatedState,
  filterBestBetsState
} from '@/hooks/atoms'


export default function Page () {
  
  const setGamesRelatedState = useSetRecoilState(gamesRelatedState)
  const setGamesBetsState = useSetRecoilState(gamesBetsState)
  const filterBestBets = useRecoilValue(filterBestBetsState)
  console.log('bets', filterBestBets)
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
  console.log(gamesBets, gamesRelated)
  
  return <div className="md:container mx-auto py-8">
    
  </div>
}