<template>
    <n-upload
        action="/api/user/avatar/change/"
        directory-dnd
        :headers="headers"
        :on-finish="handleFinish"
        :on-error="handleError"
        :before-upload="beforeUpload"
        list-type="image-card"
        with-credentials
		response-type="json"
        accept=".jpg,.png,.gif,.jpeg,.jfif,.bmp,.webp,.svg"
    />
</template>

<script setup lang="ts">
import { NUpload, useMessage, type UploadFileInfo } from 'naive-ui'
import { getCsrftoken, updateUser } from '@/utils/api'
import { useRouter } from 'vue-router'
const message = useMessage()
const headers = await (async () => ({
    'X-CSRFToken': await getCsrftoken()
}))()
const router = useRouter()
const handleFinish = ({
    file,
    event,
}: {
    file: UploadFileInfo
    event?: ProgressEvent
}) => {
    const response = (event?.target as XMLHttpRequest).response
    if (response.url) {
        file.url = response.url
        message.success('头像上传成功')
		updateUser()
        return file
    } else {
        message.error(`头像上传失败：${response}`)
    }
}

const handleError = (options: {
    file: UploadFileInfo
    event?: ProgressEvent
}) => {
    message.error('头像上传失败，请重试')
    console.log(event)
    const response = (event?.target as XMLHttpRequest).response
    console.log(response)
}

const beforeUpload = (data: {
    file: UploadFileInfo
    fileList: UploadFileInfo[]
}) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
    if (
        typeof data.file.file?.type !== 'string' ||
        !allowedTypes.includes(data.file.file?.type)
    ) {
        message.error('只支持 JPG、PNG 或 GIF 格式的图片')
        return false
    }
    if (data.file.file && data.file.file.size > 5 * 1024 * 1024) {
        message.error('文件大小不能超过 5MB')
        return false
    }
    return true
}
</script>
