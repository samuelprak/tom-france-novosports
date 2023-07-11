import { useState } from "react"
import VideoPreview from "./components/VideoPreview"
import { Button } from "antd"
import Settings from "./components/Settings"
import { WebsocketProvider } from "./contexts/WebsocketContext"

const App = () => {
  const [showSettings, setShowSettings] = useState(false)

  return (
    <WebsocketProvider>
      <div className="h-full">
        {showSettings && <Settings />}
        <div>Hello</div>
        <Button onClick={() => setShowSettings(!showSettings)}>Settings</Button>
        <div className="w-100">
          <VideoPreview />
        </div>
      </div>
    </WebsocketProvider>
  )
}

export default App
