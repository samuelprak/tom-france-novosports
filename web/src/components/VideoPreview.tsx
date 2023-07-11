import { SERVER_URL } from "../constants"

const PREVIEW_URL = `${SERVER_URL}/video`

const VideoPreview = () => {
  return <img src={PREVIEW_URL} />
}

export default VideoPreview
