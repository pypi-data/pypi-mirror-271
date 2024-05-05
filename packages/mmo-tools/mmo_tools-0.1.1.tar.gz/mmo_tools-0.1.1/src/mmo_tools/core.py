from . import utils
import os , re , requests

def convert_data(file) -> str:
   
    try:
        data_r =  open(file , "r",encoding="UTF-8").readlines()
    except Exception as error:
        return error
    data   = []
    for r in data_r:

        rp = utils.dict_typ()
        r = r + "||"
        if ("c_user" in r) and ("i_user" not in r):user =  r.split("c_user=")[1].split(";")[0]
        elif "i_user" in r:user =  r.split("i_user=")[1].split(";")[0]
        else:user = ""
        
        rp.update({"c_user":user}) # => user id

        password = utils.type_pw(value=r , valueid=user)
        if password: rp.update({"password":password})
        
        for rtip in r.split("|"):
            if "NA" in rtip and ":" in rtip:rp.update({"fb_dtsg":rtip.strip("\n")})
            if ("c_user" in rtip) or ("i_user" in rtip):rp.update({"cookie":rtip.strip("\n")})
            if ("Mozilla" in rtip) or ("Chrome" in rtip) or ("Safari" in rtip) or ("AppleWebKit" in rtip):rp.update({"user-agent":rtip.strip("\n")})
            if (len(rtip) > 150 ) and ('=' not in rtip) :rtip.update({'access_token':rtip.strip('\n')})
            if (len(rtip.split(':')) in [2,4]) or ('http://' in rtip):rp.update({'proxy':rtip.strip('\n')}) 
            if ("c_user" not in rtip) and (len(rtip) >= 32 and len(rtip) <= 40) and ("@" not in rtip):rp.update({'code':rtip.strip('\n')})
            try:
                email = re.search(r'@(.*)\.',rtip.strip("\n"))[1]
                if utils.type_emailr(email):
                    rp.update({'email':rtip.strip('\n')})
                    pass_mail = utils.type_pwemail(value=r , valuemail=rtip.strip("\n"))
                    if pass_mail:rp.update({'passemail':pass_mail})
            except Exception:
                continue
        data.append(rp)
    return data

def convert_proxy(proxy) -> str:
    https = {}
    if len(proxy.split(":")) == 2:
        https = {
            "https":f"http://{proxy}",
            "http":f"http://{proxy}"
            }
    elif "@" in proxy:
        https = {
            "https":f"http://{proxy}",
            "http":f"http://{proxy}"
            }
    elif len(proxy.split(":")) == 4:
        ip , port , user , pass_proxy = map(str,proxy.split(":"))
        https = {
            "https":f"http://{user}:{pass_proxy}@{ip}:{ port}",
            "http":f"http://{user}:{pass_proxy}@{ip}:{ port}"
            }
    return https

def checklive(fbid):
    if len(requests.get(f'https://graph.facebook.com/{fbid}/picture?redirect=0').json()['data']['url']) >= 150: return 1
    return 0

