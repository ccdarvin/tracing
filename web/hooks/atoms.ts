import useSWR from 'swr'

const API = process.env.NEXT_PUBLIC_API
const WS = process.env.NEXT_PUBLIC_WS

export const fetcher = (url: string) => {
  return fetch(url).then(r => r.json())
}


export const WEBSITE_WS = `${WS}/websites`
export const WEBSITE_API = `${API}/websites`

export const useWebsites = () => {
  const  url = `${API}/websites`
  console.log(url)
  const { data, error, mutate } = useSWR(url, fetcher)
  return {
    data: data,
    isLoading: !error && !data,
    isError: error, 
  }
}