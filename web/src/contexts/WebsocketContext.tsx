import { ReactNode, createContext, useEffect } from "react"
import { socket } from "../socket"

type Context = {}

const WebsocketContext = createContext<Context>({})

export const WebsocketProvider = ({ children }: { children: ReactNode }) => {
  useEffect(() => {
    socket.on("message", (data: any) => {
      console.log(data)
    })
  })

  return (
    <WebsocketContext.Provider value={{}}>{children}</WebsocketContext.Provider>
  )
}
