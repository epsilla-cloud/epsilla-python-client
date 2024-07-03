import requests


def get_call(url, headers, data, timeout=None, verify=False):
    resp = requests.get(
            url=url,
            data=data,
            headers=headers,
            timeout=timeout,
            verify=verify,
        )
    body = None
    status_code = resp.status_code
    if status_code == requests.ok:
        body = resp.json()
    resp.close()
    del resp
    return status_code, body


def post_call(url, headers, data, verify=False):
    resp = requests.post(
            url=url, data=data, headers=headers, verify=verify)
    status_code = resp.status_code
    body = None
    if status_code == requests.ok:
        body = resp.json()
    resp.close()
    del resp
    return status_code, body


def delete_call(url, headers, data, verify=False):
    resp = requests.delete(
            url=url, data=data, headers=headers, verify=verify)
    status_code = resp.status_code
    body = None
    if status_code == requests.ok:
        body = resp.json()
    resp.close()
    del resp
    return status_code, body
