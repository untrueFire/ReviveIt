<template>
    <n-layout has-sider v-if="store.user">
        <n-layout-sider bordered>
            <n-layout-header>
                <n-flex
                    vertical
                    style="align-items: center; justify-content: center"
                >
                    <n-avatar
                        size="large"
                        :src="
                            '/api/file/get/' +
                            (store.user as User).avatar.filename
                        "
                        fallback-src="/api/file/get/default_avatar.png"
                        round
                    />
                    <n-space>
                        <n-text>{{ store.user?.username }}</n-text>
                        <n-highlight
                            :text="groupTable[(store.user as User).group]"
                            :patterns="Object.values(groupTable)"
                            :highlight-style="{
                                padding: '0 6px',
                                borderRadius: themeVars.borderRadius,
                                display: 'inline-block',
                                color: themeVars.baseColor,
                                background: themeVars.primaryColor,
                                transition: `all .3s ${themeVars.cubicBezierEaseInOut}`,
                            }"
                        />
                    </n-space>
                </n-flex>
            </n-layout-header>
            <n-layout-content>
                <n-row style="align-items: center; justify-content: center">
                    <n-col :span="12">
                        <n-statistic label="持有物品" :value="store.user.own_item_cnt">
                        </n-statistic>
                    </n-col>
                    <n-col :span="12">
                        <n-statistic label="复活物品" :value="store.user.buy_count">
                        </n-statistic>
                    </n-col>
                    <n-col :span="12">
                        <n-statistic label="放生物品" :value="store.user.sell_count">
                        </n-statistic>
                    </n-col>
                    <n-col :span="12">
                        <n-statistic label="功德" :value="store.user.balance">
                        </n-statistic>
                    </n-col>
                </n-row>
            </n-layout-content>
            <n-layout-footer>
                <n-menu :options="menuOptions" v-model:value="activeKey"/>
            </n-layout-footer>
        </n-layout-sider>
        <n-layout>
            <n-layout-header>
                <n-flex vertical>
                    <n-flex>
                        <n-avatar
                            :src="'/api/file/get/' + store.user.avatar.filename"
                            fallback-src="/api/file/get/default_avatar.png"
                            round
                            style="
                                width: 50px;
                                height: 50px;
                                align-self: center;
                            "
                        />
                        <n-flex vertical style="flex: 2">
                            <n-flex style="align-items: baseline">
                                <n-text style="font-size: 20px">
                                    {{ store.user?.username }}
                                </n-text>
                                <n-text style="color: #b2b2b2">
                                    UID: {{ store.user?.id }}
                                </n-text>
                            </n-flex>
                            <n-progress
                                type="line"
                                :percentage="
                                    (store.user as User)?.balance % 100
                                "
                                :height="24"
                                indicator-placement="inside"
                                processing
                            >
                                小乘
                            </n-progress>
                            <n-flex>
                                <p style="align-self: self-start">
                                    <strong> 用户组: </strong>
                                    {{ groupTable[store.user.group] }}
                                </p>
                            </n-flex>
                        </n-flex>
                        <n-progress
                            type="circle"
                            status="success"
                            :percentage="store.user.balance / 100"
                        >
                            大乘
                        </n-progress>
                    </n-flex>
                    <n-divider />
                </n-flex>
            </n-layout-header>
            <n-layout-content style="text-align: left;padding:0 20px;display: contents;">
                <n-card :bordered="false">
                    <span style="font-size: 20px">{{ get_title }}</span>
                    <component :is="get_content" />                    
                </n-card>
            </n-layout-content>
        </n-layout>
    </n-layout>
</template>

<script lang="ts" setup>
import { HomeOutlined, PublishOutlined } from '@vicons/material'
import { TransactionOutlined, UserOutlined } from '@vicons/antd'
import { useThemeVars, type MenuOption } from 'naive-ui'
import { computed, ref, type Component } from 'vue'
import { useStore } from '@/stores'
import { groupTable, renderIcon } from '@/utils/constants'
import type { User } from '@/types/Api'
import UserItems from './UserItems.vue'
import UserOrders from './UserOrders.vue'
import UserProfile from './UserProfile.vue'
import WoodenFishView from './WoodenFishView.vue'
const store = useStore()
const themeVars = useThemeVars()

const menuOptions: MenuOption[] = [
    {
        label: '首页',
        key: 'home',
        icon: renderIcon(HomeOutlined),
    },
    {
        label: '物品管理',
        key: 'item',
        icon: renderIcon(PublishOutlined),
    },
    {
        label: '交易管理',
        key: 'transaction',
        icon: renderIcon(TransactionOutlined),
    },
    {
        label: '个人资料',
        key: 'profile',
        icon: renderIcon(UserOutlined),
    },
]
const activeKey = ref('home')
const get_title = computed(() => {
    switch (activeKey.value) {
        case 'item':
            return '物品管理'
        case 'transaction':
            return '交易管理'
        case 'profile':
            return '个人资料'
        default:
            return '获取功德'
    }
})
const get_content = computed(() => {
    switch (activeKey.value) {
        case 'item':
            return UserItems
        case 'transaction':
            return UserOrders
        case 'profile':
            return UserProfile
        default:
            return WoodenFishView
    }
})
</script>

<style scoped>
.n-layout-header,
.n-layout-content,
.n-layout-footer {
    padding: 24px;
}
</style>
