import {IParams, IRequest} from "core/api/model/model";

export const LOCAL_URL = 'http://127.0.0.1:8000';
export const GLOBAL_URL = 'https://api.ru-notion.ru';
export const IS_PROD = false;
// export const CURRENT_URL = GLOBAL_URL;
export const CURRENT_URL = LOCAL_URL;
export const URL_API = `${CURRENT_URL}/api`;

export const HEADERS: Record<string, string> = {
    'Content-Type': 'application/json',
    'Accept': '*/*',
}

// Получение заголовков для запросов
export function getHeaders(forAuth: boolean = false) {
    if (forAuth)
        return {
            ...HEADERS,
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
        }
    return HEADERS
}


export const getParams = (params?: IParams) => {
    if (params === undefined) return ''
    let paramsStr: string[] = []
    Object.entries(params).forEach(([key, value]) => {
        paramsStr.push(`${key}=${value}`)
    })

    if (paramsStr.length > 0)
        return `?${paramsStr.join('&')}`
    return ''
}

export function getURL(url: string, params?: IParams) {
    if (!params)
        return url
    return url + getParams(params)
}

export async function request({method, url, body, headers}: IRequest) {
    const data: Record<string, any> = {
        method: method,
        credentials: 'include',
        headers: getHeaders(),
        body: body,
    }

    if (headers !== undefined) {
        data.headers = headers
    }
    const res = await fetch(url, data)
    if (res.ok) {
        if (res.status === 204)
            return null
        return await res.json();
    }
    return Promise.reject(res);
}
