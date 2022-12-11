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
