# weeing 복합기

import json
import requests

url = "https://www.epsonconnect.com/user/Scan2cloud/address_edit"

def lambda_handler(event, context):
    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('Request body not found.')
        }

    # event['body']를 JSON 객체로 변환
    body = json.loads(event['body'])

    # event로 받는 데이터
    # EPSONCONNECT_SID, USER_KEY_VALUE, dest_alias, dest_address, dest_note, subject, mailbody
    EPSONCONNECT_SID = body["sid"]
    USER_KEY_VALUE = body["user_key"]
    DEST_ALIAS = body["alias"]
    DEST_ADDRESS = body["email_address"]
    DEST_NOTE = body["note"]
    SUBJECT = body["subject"]
    MAILBODY = body["mail_body"]

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": f"text/plain;charset=UTF-8",
        "Cookie": f"epsonconnect_lang=ko; epsonconnect_email=wee%40ing.so; epsonconnect_sid={EPSONCONNECT_SID}",
        "Origin": "https://www.epsonconnect.com",
        "Priority": "u=1, i",
        "Referer": "https://www.epsonconnect.com/user/Device/index_scn?serial_number=X7S3",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    
    print(headers)
    print("EPSONCONNECT_SID: " + EPSONCONNECT_SID)
    print("USR_KEY: " + USER_KEY_VALUE)

    body = (
        f"dest_alias={DEST_ALIAS}&"
        f"dest_address={DEST_ADDRESS}&"
        f"dest_note={DEST_NOTE}&"
        f"subject={SUBJECT}&"
        f"mailbody={MAILBODY}&"
        "dest_type=email&"
        "serial_number=X7S3006860&"
        f"usrkey={USER_KEY_VALUE}&"
        "dest_online_auth_id="
    )
    
    response = requests.post(url, headers=headers, data=body)

    print("응갑결과 : " +  response.text)
    return {
        'statusCode': response.status_code,
        'body': response.text
    }
