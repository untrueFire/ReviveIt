<template>
    <n-data-table
        v-if="store.readNotifications.length > 0"
        :columns="columns"
        :data="store.readNotifications"
        virtual-scroll
        :max-height="600"
        striped
    />
</template>

<script setup lang="ts">
import { onMounted, h } from 'vue'
import { useStore } from '@/stores'
import { updateRead } from '@/utils/api'
import { NTime, type DataTableColumn } from 'naive-ui'
import { type Notification } from '@/types/Api'
const store = useStore()

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

const columns: DataTableColumn<Notification>[] = [
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
    updateRead()
})
</script>

<style scoped>
.notifications-container {
    margin-top: 20px;
    border: 1px solid #ccc;
    padding: 10px;
}
</style>
