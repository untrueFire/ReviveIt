import { type MessageApiInjection } from 'naive-ui/es/message/src/MessageProvider'
import * as Api from './Api.ts'
declare global {
    interface Window {
        $message: MessageApiInjection
    }

    type PartialItem = Partial<Api.Item>
    type Notification = Api.Notification
}
