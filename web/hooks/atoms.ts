import { atom, selector } from 'recoil'


const API = process.env.NEXT_PUBLIC_API
const WS = process.env.NEXT_PUBLIC_WS

export const fetcher = (url: string) => {
  return fetch(url).then(r => r.json())
}


export const WEBSITE_WS = `${WS}/websites`
export const WEBSITE_API = `${API}/websites`
export const GAME_API = `${API}/games`
export const GAME_WS = `${WS}/games`
export const GAME_RELATED_API = `${API}/games/related`
export const GAME_BETS_API = `${API}/games/bets`

// atoms

export const gamesRelatedState = atom({
  key: 'gamesRelatedState',
  default: [],
})

export const gamesBetsState = atom({
  key: 'gamesBetsState',
  default: [],
})

export const filterBestBetsState = selector({
  key: 'filterBestBets',
  get: ({ get }) => {
    const gamesBets = get(gamesBetsState)
    const gamesRelated = get(gamesRelatedState)
    return gamesRelated.map((related: any) => {
      const bets= <any>{}
      const gamesIds = related.related.map((game: any) => game.id)
      gamesBets.forEach((bet: any) => {
        if (gamesIds.includes(bet.gameId)) {
          //check if bet is better than the previous one
          if (bets[bet.id]) {
            if (bet.bet > bets[bet.id].bet) {
              bets[bet.id] = bet
            }
          } else {
            bets[bet.id] = bet
          }
        }
      })
      return { ...related, bets }
    })
  }
})
