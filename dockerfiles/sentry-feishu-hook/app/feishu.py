import json
import datetime
import requests

from fastapi import FastAPI, Query, Body
from urllib.parse import urlparse

app = FastAPI(
    docs_url='/api/v1/docs',
    redoc_url='/api/v1/redoc',
    openapi_url='/api/v1/openapi.json'
)

@app.post('/hook', status_code=201)
async def sentry_hook(
    feishu: str = Query('https://open.feishu.cn/open-apis/bot/v2/hook/640a8182-7ca4-4e10-8140-6183c359613a'),
    data=Body(...),
):

    level = data['level'].upper()
    color = {
        'ERROR': 'red',
        'WARNING': 'yellow',
        'INFO': 'blue',
    }.get(data['level'], 'red')
    project_name = data['project']
    env = data['event'].get('environment', 'UNKNOWN')
    timestamp = datetime.datetime.fromtimestamp(data['event']['timestamp'])
    issue_id = data['id']
    error_type = data['event']['metadata'].get('type', '')
    exception_title = data['culprit']
    exception_value = data['event']['metadata'].get('value', '')
    message = data['message']
    issue_url = data['url']
    parsed_uri = urlparse(issue_url)
    sentry_url = f'{parsed_uri.scheme}://{parsed_uri.netloc}/'

    data = {
        'msg_type': 'interactive',
        'card': {
            'config': {
                'wide_screen_mode': True,
                'enable_forward': True,
            },
            'header': {
                'template': color,
                'title': {
                    'content': f'【{env}】Sentry告警通知',
                    'tag': 'plain_text'
                }
            },
            'elements': [
                {
                    'fields': [
                        {
                            'is_short': False,
                            'text': {
                                'content': f'**项目：**{project_name}',
                                'tag': 'lark_md'
                            }
                        },
                        {
                            'is_short': False,
                            'text': {
                                'content': f'**环境：**{env}',
                                'tag': 'lark_md'
                            }
                        },
                        {
                            'is_short': False,
                            'text': {
                                'content': f'**事件：**{issue_id}',
                                'tag': 'lark_md'
                            }
                        },
                        {
                            'is_short': False,
                            'text': {
                                'content': f'**时间：**{timestamp.strftime("%Y-%m-%d %H:%M:%S")}',
                                'tag': 'lark_md'
                            }
                        }
                    ],
                    'tag': 'div'
                },
                {
                    'tag': 'hr'
                },
                {
                    'tag': 'div',
                    'text': {
                        'content': f'**异常：**\n**{error_type} {exception_title}**\n{exception_value}\n\n**Message: **\n{message}',
                        'tag': 'lark_md'
                    }
                },
                {
                    'actions': [
                        {
                            'tag': 'button',
                            'text': {
                                'content': '开始处理',
                                'tag': 'plain_text'
                            },
                            'type': 'primary',
                            'url': issue_url,
                            'value': {
                                'key': 'value'
                            }
                        }
                    ],
                    'tag': 'action'
                },
                {
                    'tag': 'hr'
                },
                {
                    'elements': [
                        {
                            'content': f'[来自Sentry日志平台]({sentry_url})',
                            'tag': 'lark_md'
                        }
                    ],
                    'tag': 'note'
                }
            ]
        }
    }

    headers = {
        'Content-Type': 'application/json',
    }

    requests.post(feishu, headers=headers, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))

