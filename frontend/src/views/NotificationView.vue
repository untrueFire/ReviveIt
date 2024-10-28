<template>
    <n-flex vertical class="notifications-container">
        <n-tabs type="line" placement="left">
            <n-tab-pane name="unread" tab="未读通知">
                <n-data-table
                    v-if="store.unreadNotifications.length > 0"
                    :columns="columns"
                    :data="store.unreadNotifications"
                    virtual-scroll
                    :max-height="600"
                    striped
                />
                <p v-else>暂无未读通知</p>
            </n-tab-pane>
            <n-tab-pane name="read" tab="已读通知">
                <n-data-table
                    v-if="store.readNotifications.length > 0"
                    :columns="columns2"
                    :data="store.readNotifications"
                    virtual-scroll
                    :max-height="600"
                    striped
                />
                <p v-else>暂无已读通知</p>
            </n-tab-pane>
        </n-tabs>
    </n-flex>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, h } from 'vue'
import { useStore } from '../stores'
import {
    updateUnread,
    updateRead,
    acceptNotification,
    rejectNotification,
    setRead,
} from '../utils/api'
import {
    useMessage,
    NFlex,
    NButton,
    NTime,
    type DataTableColumn,
} from 'naive-ui'
import { type Notification } from '../types/Api'
const store = useStore()
const message = useMessage()
const intervalId = ref<ReturnType<typeof setInterval>>()

const relativeTime = (notification: Notification) =>
    h(NTime, {
        time: new Date(notification.timestamp as string),
        to: Date.now(),
        type: 'relative',
    })

const format = (notification: Notification, type: number) => {
    let str = '',
        res = ''
    switch (notification.verb) {
        case 'proposed':
            str = `${notification.actor.username} 请求以 ${notification.action_object.price} 功德的代价复活 ${notification.action_object.target.name}`
            if (type == 1) {
                switch (notification.data) {
                    case 'accepted':
                        res = '已同意'
                        break
                    case 'rejected':
                        res = '已拒绝'
                        break
                    case 'sold out':
                        res = '已被先行复活'
                        break
                }
            }
            break
        case 'accepted':
            str = `${notification.actor.username} 同意了你以 ${notification.action_object.price} 功德的代价复活 ${notification.action_object.target.name} 的请求`
            if (type == 1) res = '已同意'
            break
        case 'rejected':
            str = `${notification.actor.username} 拒绝了你以 ${notification.action_object.price} 功德的代价复活 ${notification.action_object.target.name} 的请求`
            if (type == 1) res = '已拒绝'
            break
        case 'sold out':
            str = `你向 ${notification.actor.username} 请求的 ${notification.action_object.target.name} 已被先行复活`
            if (type == 1) res = '已被先行复活'
            break
    }
    if (type == 1) return [str, res]
    return str
}

const handleAcceptNotification = async (notificationId: number) => {
    try {
        await acceptNotification(notificationId)
        message.success('同意请求成功')
    } catch {
        message.error('同意请求失败')
    }
    await updateUnread()
}

const handleRejectNotification = async (notificationId: number) => {
    try {
        await rejectNotification(notificationId)
        message.success('拒绝请求成功')
    } catch {
        message.error('拒绝请求失败')
    }
    await updateUnread()
}

const handleSetRead = async (notificationId: number) => {
    try {
        await setRead(notificationId)
    } catch {
        message.error('设置已读失败')
    }
    const notification = store.unreadNotifications.filter(
        item => item.id == notificationId,
    )[0]
    store.unreadNotifications = store.unreadNotifications.filter(
        item => item.id != notificationId,
    )
    store.readNotifications.unshift(notification)
}

const columns = [
    {
        title: '时间',
        key: 'time',
        resizable: true,
        ellipsis: true,
        sorter: (row1: Notification, row2: Notification) =>
            new Date(row1.timestamp as string).getTime() -
            new Date(row2.timestamp as string).getTime(),
        render: relativeTime,
    },
    {
        title: '内容',
        key: 'content',
        ellipsis: true,
        resizable: true,
        render: (row: Notification) => format(row, 0),
    },
    {
        title: '操作',
        key: 'actions',
        resizable: true,
        ellipsis: true,
        render(row: Notification) {
            if (row.verb == 'proposed') {
                return h(NFlex, null, () => [
                    h(
                        NButton,
                        {
                            strong: true,
                            tertiary: true,
                            size: 'small',
                            onClick: () => handleAcceptNotification(row.id),
                        },
                        { default: () => '同意' },
                    ),
                    h(
                        NButton,
                        {
                            strong: true,
                            tertiary: true,
                            size: 'small',
                            onClick: () => handleRejectNotification(row.id),
                        },
                        { default: () => '拒绝' },
                    ),
                ])
            } else {
                return h(
                    NButton,
                    {
                        strong: true,
                        tertiary: true,
                        size: 'small',
                        onClick: () => handleSetRead(row.id),
                    },
                    { default: () => '已读' },
                )
            }
        },
    },
]

const columns2: DataTableColumn<Notification>[] = [
    {
        title: '时间',
        key: 'time',
        resizable: true,
        ellipsis: true,
        sorter: (row1, row2) =>
            new Date(row1.timestamp).getTime() -
            new Date(row2.timestamp).getTime(),
        render: relativeTime,
    },
    {
        title: '内容',
        key: 'content',
        resizable: true,
        ellipsis: true,
        render: row => format(row, 1)[0],
    },
    {
        title: '结果',
        key: 'result',
        resizable: true,
        ellipsis: true,
        render: row => format(row, 1)[1],
        filterOptions: [
            {
                label: '已同意',
                value: '已同意',
            },
            {
                label: '已拒绝',
                value: '已拒绝',
            },
            {
                label: '已被先行复活',
                value: '已被先行复活',
            },
        ],
        filter(value, row) {
            return Boolean(~format(row, 1)[1].indexOf(value as string))
        },
    },
]

onMounted(() => {
    intervalId.value = setInterval(updateRead, 30000)
    updateRead()
})

onUnmounted(() => {
    clearInterval(intervalId.value)
})
</script>

<style scoped>
.notifications-container {
  margin-top: 20px;
  border: 1px solid #ccc;
  padding: 10px;
}
</style>
