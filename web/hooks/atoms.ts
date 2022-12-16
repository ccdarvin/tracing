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
    }).filter((related: any) => Object.keys(related.bets).length > 0)
  }
})


const safeBets = <any>[
  ['regular_1x2_1', 'regular_doble-oportunidad_X2'],
]


export const filterSafeBetsState = selector({
  key: 'filterSafeBets',
  get: ({ get }) => {
    const bestBets = get(filterBestBetsState)
    return bestBets.map((relateGame) => {
      const safe = <any>[]
      const bets = relateGame.bets
      safeBets.forEach((safeBet: any) => {

        if ( !safeBet.every((id: string) => bets[id]) ) return

        let total = 0
        safeBet.forEach((id: string) => {
          total += bets[id].bet
        })
        
        safe.push(safeBet.map((id: string) => {
          const betPercent = bets[id].bet / total
          const profit = (1-betPercent) * bets[id].bet
          return { id, betPercent, profit, detail: bets[id], safe: profit>0 }
        }))
      })
      return { ...relateGame, safe }
    }).filter((relateGame: any) => relateGame.safe.length > 0)
  },
})

export const getIcon = (url: string) => {
  console.log(url)
  const uri = new URL(url)
  const googleIcon = `https://www.google.com/s2/favicons?domain=${uri.host}&sz=64`
  return googleIcon
}