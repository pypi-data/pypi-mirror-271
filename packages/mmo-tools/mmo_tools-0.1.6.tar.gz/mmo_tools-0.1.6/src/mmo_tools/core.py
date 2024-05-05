from . import utils
import os , re , requests

def convert_data(file) -> str:
    """
        return [{},{}]

        {
            "c_user":"",
            "password":"",
            "code":"",
            "email":"",
            "passemail":"",
            "user-agent":"",
            "cookie":"",
            "fb_dtsg":"",
            "proxy":"",
            "access_token":"",
            "headers":{key:value}
        }
    """
    try:
        data_r =  [key.strip("\n") for key in open(file , "r",encoding="UTF-8").readlines()]
    except Exception as error:
        return error
    data   = []
    for r in data_r:
        if r == "":continue
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
            if (len(rtip) > 150) and ('=' not in rtip) :rp.update({'access_token':rtip.strip('\n')})
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

def convert_headers_web(headers_text: str) :

    """
        return headers {key : value}
    """
    headers , check , name = {} , 0 , ""
    if "\n" not in headers_text:
        print("""
        Headers are not in the correct format.
              Example 1: 

                   Accept:
*/*
              Content-Type:
application/x-www-form-urlencoded
              

              Example 2 :

                   Accept:*/*,
                   Content-Type:application/x-www-form-urlencoded
              
            

              
""")
    headers_text =  headers_text.replace('\n','|').replace('"','`').replace('://','(^)').split('|')
    try:
        for temp in headers_text:
            if temp[-1:] == ':':
                name = temp[:-1].replace('\n','').replace('`','"').replace('(^)','://')
                headers.update({name:""})
                check = 1
            if temp[-1:] != ':' and check:
                headers.update({name:temp.replace('\n','').replace('`','"').replace('(^)','://')})
                check = 0
    except Exception as error:
        print(error)
        return headers
    return headers
def convert_proxy(proxy) -> str:
    """
        return {
            "https":"http://{type proxy}",
            "http":"http://{type proxy}"
            }
    """
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

def check_facebook_account(fbid):
    """
        return  / live : 1
                / die  : 0
    """
    try:
        response = requests.get(f'https://graph.facebook.com/{str(fbid)}/picture?redirect=0')
        data = response.json()
        url = data['data']['url']
        return len(url) >= 150
    except (requests.RequestException, KeyError) as e:
        print(f"Lỗi khi kiểm tra tài khoản Facebook: {e}")
        return False
