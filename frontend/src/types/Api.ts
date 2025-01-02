/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface PublicUser {
    /** ID */
    id?: number
    /**
     * 用户名
     * 必填；长度为150个字符或以下；只能包含字母、数字、特殊字符“@”、“.”、“-”和“_”。
     * @minLength 1
     * @maxLength 150
     * @pattern ^[\w.@+-]+$
     */
    username: string
}

export interface Item {
    /** ID */
    id: number
    /**
     * Name
     * @minLength 1
     * @maxLength 100
     */
    name: string
    /**
     * Description
     * @minLength 1
     */
    description: string
    /**
     * Contact info
     * @minLength 1
     * @maxLength 200
     */
    contactInfo: string
    owner: PublicUser
    tags: string[]
}

export interface User {
    group: 'admin' | 'user' | 'guest'
    /** ID */
    id: number
    /**
     * 用户名
     * 必填；长度为150个字符或以下；只能包含字母、数字、特殊字符“@”、“.”、“-”和“_”。
     * @minLength 1
     * @maxLength 150
     * @pattern ^[\w.@+-]+$
     */
    username: string
    /**
     * Balance
     * @min 0
     * @max 9223372036854776000
     */
    balance: number
}

export interface SimpleItem {
    /** ID */
    id?: number
    /**
     * Name
     * @minLength 1
     * @maxLength 100
     */
    name: string
}

export interface Transaction {
    /** ID */
    id?: number
    target: SimpleItem
    /**
     * Price
     * @min 0
     * @max 9223372036854776000
     */
    price: number
}

export interface Notification {
    /** ID */
    id: number
    /** Unread */
    unread: boolean
    actor: PublicUser
    /**
     * Verb
     * @minLength 1
     * @maxLength 255
     */
    verb: string
    action_object: Transaction
    /**
     * Timestamp
     * @format date-time
     */
    timestamp: string
    /** Data */
    data?: string | null
}

export type QueryParamsType = Record<string | number, any>
export type ResponseFormat = keyof Omit<Body, 'body' | 'bodyUsed'>

export interface FullRequestParams extends Omit<RequestInit, 'body'> {
    /** set parameter to `true` for call `securityWorker` for this request */
    secure?: boolean
    /** request path */
    path: string
    /** content type of request body */
    type?: ContentType
    /** query params */
    query?: QueryParamsType
    /** format of response (i.e. response.json() -> format: "json") */
    format?: ResponseFormat
    /** request body */
    body?: unknown
    /** base url */
    baseUrl?: string
    /** request cancellation token */
    cancelToken?: CancelToken
}

export type RequestParams = Omit<
    FullRequestParams,
    'body' | 'method' | 'query' | 'path'
>

export interface ApiConfig<SecurityDataType = unknown> {
    baseUrl?: string
    baseApiParams?: Omit<RequestParams, 'baseUrl' | 'cancelToken' | 'signal'>
    securityWorker?: (
        securityData: SecurityDataType | null,
    ) => Promise<RequestParams | void> | RequestParams | void
    customFetch?: typeof fetch
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown>
    extends Response {
    data: D
    error: E
}

type CancelToken = Symbol | string | number

export enum ContentType {
    Json = 'application/json',
    FormData = 'multipart/form-data',
    UrlEncoded = 'application/x-www-form-urlencoded',
    Text = 'text/plain',
}

export class HttpClient<SecurityDataType = unknown> {
    public baseUrl: string = 'http://localhost:8000/api'
    private securityData: SecurityDataType | null = null
    private securityWorker?: ApiConfig<SecurityDataType>['securityWorker']
    private abortControllers = new Map<CancelToken, AbortController>()
    private customFetch = (...fetchParams: Parameters<typeof fetch>) =>
        fetch(...fetchParams)

    private baseApiParams: RequestParams = {
        credentials: 'same-origin',
        headers: {},
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
    }

    constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
        Object.assign(this, apiConfig)
    }

    public setSecurityData = (data: SecurityDataType | null) => {
        this.securityData = data
    }

    protected encodeQueryParam(key: string, value: any) {
        const encodedKey = encodeURIComponent(key)
        return `${encodedKey}=${encodeURIComponent(typeof value === 'number' ? value : `${value}`)}`
    }

    protected addQueryParam(query: QueryParamsType, key: string) {
        return this.encodeQueryParam(key, query[key])
    }

    protected addArrayQueryParam(query: QueryParamsType, key: string) {
        const value = query[key]
        return value.map((v: any) => this.encodeQueryParam(key, v)).join('&')
    }

    protected toQueryString(rawQuery?: QueryParamsType): string {
        const query = rawQuery || {}
        const keys = Object.keys(query).filter(
            key => 'undefined' !== typeof query[key],
        )
        return keys
            .map(key =>
                Array.isArray(query[key])
                    ? this.addArrayQueryParam(query, key)
                    : this.addQueryParam(query, key),
            )
            .join('&')
    }

    protected addQueryParams(rawQuery?: QueryParamsType): string {
        const queryString = this.toQueryString(rawQuery)
        return queryString ? `?${queryString}` : ''
    }

    private contentFormatters: Record<ContentType, (input: any) => any> = {
        [ContentType.Json]: (input: any) =>
            input !== null &&
            (typeof input === 'object' || typeof input === 'string')
                ? JSON.stringify(input)
                : input,
        [ContentType.Text]: (input: any) =>
            input !== null && typeof input !== 'string'
                ? JSON.stringify(input)
                : input,
        [ContentType.FormData]: (input: any) =>
            Object.keys(input || {}).reduce((formData, key) => {
                const property = input[key]
                formData.append(
                    key,
                    property instanceof Blob
                        ? property
                        : typeof property === 'object' && property !== null
                          ? JSON.stringify(property)
                          : `${property}`,
                )
                return formData
            }, new FormData()),
        [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
    }

    protected mergeRequestParams(
        params1: RequestParams,
        params2?: RequestParams,
    ): RequestParams {
        return {
            ...this.baseApiParams,
            ...params1,
            ...(params2 || {}),
            headers: {
                ...(this.baseApiParams.headers || {}),
                ...(params1.headers || {}),
                ...((params2 && params2.headers) || {}),
            },
        }
    }

    protected createAbortSignal = (
        cancelToken: CancelToken,
    ): AbortSignal | undefined => {
        if (this.abortControllers.has(cancelToken)) {
            const abortController = this.abortControllers.get(cancelToken)
            if (abortController) {
                return abortController.signal
            }
            return void 0
        }

        const abortController = new AbortController()
        this.abortControllers.set(cancelToken, abortController)
        return abortController.signal
    }

    public abortRequest = (cancelToken: CancelToken) => {
        const abortController = this.abortControllers.get(cancelToken)

        if (abortController) {
            abortController.abort()
            this.abortControllers.delete(cancelToken)
        }
    }

    public request = async <T = any, E = any>({
        body,
        secure,
        path,
        type,
        query,
        format,
        baseUrl,
        cancelToken,
        ...params
    }: FullRequestParams): Promise<HttpResponse<T, E>> => {
        const secureParams =
            ((typeof secure === 'boolean'
                ? secure
                : this.baseApiParams.secure) &&
                this.securityWorker &&
                (await this.securityWorker(this.securityData))) ||
            {}
        const requestParams = this.mergeRequestParams(params, secureParams)
        const queryString = query && this.toQueryString(query)
        const payloadFormatter =
            this.contentFormatters[type || ContentType.Json]
        const responseFormat = format || requestParams.format

        return this.customFetch(
            `${baseUrl || this.baseUrl || ''}${path}${queryString ? `?${queryString}` : ''}`,
            {
                ...requestParams,
                headers: {
                    ...(requestParams.headers || {}),
                    ...(type && type !== ContentType.FormData
                        ? { 'Content-Type': type }
                        : {}),
                },
                signal:
                    (cancelToken
                        ? this.createAbortSignal(cancelToken)
                        : requestParams.signal) || null,
                body:
                    typeof body === 'undefined' || body === null
                        ? null
                        : payloadFormatter(body),
            },
        ).then(async response => {
            const r = response.clone() as HttpResponse<T, E>
            r.data = null as unknown as T
            r.error = null as unknown as E

            const data = !responseFormat
                ? r
                : await response[responseFormat]()
                      .then(data => {
                          if (r.ok) {
                              r.data = data
                          } else {
                              r.error = data
                          }
                          return r
                      })
                      .catch(e => {
                          r.error = e
                          return r
                      })

            if (cancelToken) {
                this.abortControllers.delete(cancelToken)
            }

            if (!response.ok) throw data
            return data
        })
    }
}

/**
 * @title ReviveIt API
 * @version v1
 * @baseUrl http://localhost:8000/api
 *
 * API documentation for ReviveIt
 */
export class Api<
    SecurityDataType extends unknown,
> extends HttpClient<SecurityDataType> {
    items = {
        /**
         * No description
         *
         * @tags items
         * @name ItemsAddCreate
         * @summary 添加物品
         * @request POST:/items/add/
         * @secure
         */
        itemsAddCreate: (
            data: {
                /** 物品名称 */
                name: string
                /** 物品描述 */
                description: string
                /** 联系人信息 */
                contactInfo: string
            },
            params: RequestParams = {},
        ) =>
            this.request<void, void>({
                path: `/items/add/`,
                method: 'POST',
                body: data,
                secure: true,
                ...params,
            }),

        /**
         * No description
         *
         * @tags items
         * @name ItemsDeleteCreate
         * @summary 删除指定ID的物品
         * @request POST:/items/delete/{item_id}/
         * @secure
         */
        itemsDeleteCreate: (itemId: number, params: RequestParams = {}) =>
            this.request<void, void>({
                path: `/items/delete/${itemId}/`,
                method: 'POST',
                secure: true,
                ...params,
            }),

        /**
         * No description
         *
         * @tags items
         * @name ItemsReviveCreate
         * @summary 复活指定ID的物品
         * @request POST:/items/revive/{item_id}/
         * @secure
         */
        itemsReviveCreate: (
            itemId: number,
            data: {
                /** 为了复活物品愿意消耗的功德 */
                price: number
            },
            params: RequestParams = {},
        ) =>
            this.request<void, void>({
                path: `/items/revive/${itemId}/`,
                method: 'POST',
                body: data,
                secure: true,
                type: ContentType.Json,
                ...params,
            }),

        /**
         * No description
         *
         * @tags items
         * @name ItemsUpdateCreate
         * @summary 更新指定ID的物品
         * @request POST:/items/update/{item_id}/
         * @secure
         */
        itemsUpdateCreate: (
            itemId: number,
            data: {
                /** 物品名称 */
                name: string
                /** 物品描述 */
                description: string
                /** 联系人信息 */
                contactInfo: string
            },
            params: RequestParams = {},
        ) =>
            this.request<Item, any>({
                path: `/items/update/${itemId}/`,
                method: 'POST',
                body: data,
                secure: true,
                format: 'json',
                ...params,
            }),

        /**
         * No description
         *
         * @tags items
         * @name ItemsRead
         * @summary 查询指定ID的物品
         * @request GET:/items/{item_id}/
         * @secure
         */
        itemsRead: (itemId: number, params: RequestParams = {}) =>
            this.request<Item, void>({
                path: `/items/${itemId}/`,
                method: 'GET',
                secure: true,
                format: 'json',
                ...params,
            }),
    }
    notification = {
        /**
         * No description
         *
         * @tags notification
         * @name NotificationAcceptCreate
         * @summary 同意指定ID的通知
         * @request POST:/notification/accept/{notification_id}/
         * @secure
         */
        notificationAcceptCreate: (
            notificationId: number,
            params: RequestParams = {},
        ) =>
            this.request<void, void>({
                path: `/notification/accept/${notificationId}/`,
                method: 'POST',
                secure: true,
                ...params,
            }),

        /**
         * No description
         *
         * @tags notification
         * @name NotificationReadCreate
         * @summary 将指定ID的通知标为已读
         * @request POST:/notification/read/{notification_id}/
         * @secure
         */
        notificationReadCreate: (
            notificationId: number,
            params: RequestParams = {},
        ) =>
            this.request<void, void>({
                path: `/notification/read/${notificationId}/`,
                method: 'POST',
                secure: true,
                ...params,
            }),

        /**
         * No description
         *
         * @tags notification
         * @name NotificationRejectCreate
         * @summary 拒绝指定ID的通知
         * @request POST:/notification/reject/{notification_id}/
         * @secure
         */
        notificationRejectCreate: (
            notificationId: number,
            params: RequestParams = {},
        ) =>
            this.request<void, void>({
                path: `/notification/reject/${notificationId}/`,
                method: 'POST',
                secure: true,
                ...params,
            }),
    }
    search = {
        /**
         * No description
         *
         * @tags search
         * @name SearchList
         * @summary 根据关键字查询物品
         * @request GET:/search/
         * @secure
         */
        searchList: (
            query?: {
                /** 物品名称或描述 */
                q?: string
                /** 返回数量上限 */
                limit?: number
                /** 起始下标 */
                offset?: number
                /** 排序字段 */
                orderby?: string
            },
            params: RequestParams = {},
        ) =>
            this.request<Item, any>({
                path: `/search/`,
                method: 'GET',
                query: query,
                secure: true,
                format: 'json',
                ...params,
            }),
    }
    user = {
        /**
         * No description
         *
         * @tags user
         * @name UserList
         * @summary 查询当前用户的信息
         * @request GET:/user/
         * @secure
         */
        userList: (params: RequestParams = {}) =>
            this.request<User, void>({
                path: `/user/`,
                method: 'GET',
                secure: true,
                format: 'json',
                ...params,
            }),

        /**
         * No description
         *
         * @tags user
         * @name UserChallengeCreate
         * @summary 生成一个PoW（工作量证明）
         * @request POST:/user/challenge/
         * @secure
         */
        userChallengeCreate: (params: RequestParams = {}) =>
            this.request<
                {
                    challenge?: string
                    difficulty?: number
                },
                void
            >({
                path: `/user/challenge/`,
                method: 'POST',
                secure: true,
                format: 'json',
                ...params,
            }),

        /**
         * No description
         *
         * @tags user
         * @name UserItemsList
         * @summary 查询当前用户的物品
         * @request GET:/user/items/
         * @secure
         */
        userItemsList: (
            query?: {
                /** 返回数量上限 */
                limit?: number
                /** 起始下标 */
                offset?: number
                /** 排序字段 */
                orderby?: string
            },
            params: RequestParams = {},
        ) =>
            this.request<Item[], any>({
                path: `/user/items/`,
                method: 'GET',
                query: query,
                secure: true,
                format: 'json',
                ...params,
            }),

        /**
         * @description 验证规则是`sha256(challenge + nonce)`以`difficulty`个`0`结尾
         *
         * @tags user
         * @name UserKnockCreate
         * @summary 验证一个PoW
         * @request POST:/user/knock/
         * @secure
         */
        userKnockCreate: (
            data: {
                /** 满足challenge的答案 */
                nonce: string
            },
            params: RequestParams = {},
        ) =>
            this.request<void, void>({
                path: `/user/knock/`,
                method: 'POST',
                body: data,
                secure: true,
                type: ContentType.Json,
                ...params,
            }),

        /**
         * No description
         *
         * @tags user
         * @name UserNotificationsList
         * @summary 获取当前用户所有通知
         * @request GET:/user/notifications/
         * @secure
         */
        userNotificationsList: (params: RequestParams = {}) =>
            this.request<Notification[], any>({
                path: `/user/notifications/`,
                method: 'GET',
                secure: true,
                format: 'json',
                ...params,
            }),

        /**
         * No description
         *
         * @tags user
         * @name UserNotificationsReadList
         * @summary 获取当前用户所有已读通知
         * @request GET:/user/notifications/read/
         * @secure
         */
        userNotificationsReadList: (params: RequestParams = {}) =>
            this.request<Notification[], any>({
                path: `/user/notifications/read/`,
                method: 'GET',
                secure: true,
                format: 'json',
                ...params,
            }),

        /**
         * No description
         *
         * @tags user
         * @name UserNotificationsUnreadList
         * @summary 获取当前用户所有未读通知
         * @request GET:/user/notifications/unread/
         * @secure
         */
        userNotificationsUnreadList: (params: RequestParams = {}) =>
            this.request<Notification[], any>({
                path: `/user/notifications/unread/`,
                method: 'GET',
                secure: true,
                format: 'json',
                ...params,
            }),
    }
}
