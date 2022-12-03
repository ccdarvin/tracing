'use client'

import React, { useState, useEffect } from 'react'
import { json } from 'stream/consumers';


export default function Page() {
  const [isConnected, setIsConnected] = useState(false)
  const [lastPong, setLastPong] = useState({})

  
  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:4000/ws')
    ws.onopen = () => {
      setIsConnected(true)
    }

    ws.onmessage = async (event: any) => {
      const text = await event.data.text()
      const data = JSON.parse(text)
      const key = `${data.channel}:${data.url}:${data.group}:${data.name}`
      console.log(key, data)
      setLastPong((prev) => ({ ...prev, [key]: data }))
    }

    ws.onclose = () => {
      setIsConnected(false)
    }

  }, []);
  return <div className="flex flex-col justify-center items-center">
    <h1>Dashboard</h1>
    <p>Socket connected: {isConnected ? "yes" : "no"}</p>
    <div>
      {Object.keys(lastPong).map((key: string) => <div>
        <div>
          <span>{lastPong[key].name}</span>
          <span>{lastPong[key].bid}</span>
        </div>
      </div>)}
    </div>
  </div>
}