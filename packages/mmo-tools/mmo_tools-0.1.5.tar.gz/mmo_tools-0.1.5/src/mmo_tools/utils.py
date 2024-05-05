
from datetime import datetime

def type_pw(value,valueid):
    value =  value + "|"
    for index , x in enumerate(value.split("|")):
        try:
            if valueid == x and len(value.split("|")) >  1:
                return value.split("|")[index + 1]
        except Exception:pass
def type_pwemail(value,valuemail):
    value =  value + "|"
    for index , x in enumerate(value.split("|")):
        try:
            if valuemail == x and len(value.split("|")) >  1:
                return value.split("|")[index + 1]
        except Exception:pass


def headers():
    return {
            "accept":"*/*",
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"en-US,en;q=0.9",
            "content-type":"application/x-www-form-urlencoded",
            "X-Do-Not-Track": "1",
            "sec-ch-ua-mobile":"?0",
            "Connection": "keep-alive",
            "DNT": "1",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode":"cors",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "x-requested-with": "XMLHttpRequest",
            "x-response-format": "JSONStream",
            "viewport-width":"934",
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        }
def type_emailr(value):
    for x in value:
        if (x >= 'a' and x <= 'z') or (x >= 'A' and x <= 'Z'):continue
        else: return 0
    return 1
def dict_typ():
    return  {
        "c_user":"","password":"","code":"","email":"","passemail":"","user-agent":"","cookie":"","fb_dtsg":"","id":"","text":"","proxy":"","reaction":"","access_token":"","business":"","attent_id":"","feeling":"","headers":headers()
        }