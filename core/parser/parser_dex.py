import json

import requests
import pprint

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
    'cookeis': 'cf_clearance=9hIGhBvXnEWVX9QvEpu5Ix2quaBYO4Vl8fsfTQJLOU0-1730032322-1.2.1.1-V5paFlubqmQ_ndbMtn3LdDF2QNJcLysDAkNhgTPnTLdjkWZEJCHV4AcDlEbeufIqsVChFDp1.TreNtO_uGDoTjsOW7JHvPQ_OtYKKJgWJKSIR_tNP683B0eeGZdn7ociVvxPVz9NWw4fxJOB9GGe_p.cs_pXvBkRazJPs9FbVX6JCWgrQGCJA7u_QjgPhKk6Ie7CLc_Md.ZyNQGTgOvZEehE4WVNpuODyAlhV0daSOcaXPyKfabv9ttZZj.59W38aZsW6cyDec5Qrnd1oKA65KFQJ6n01JW_TZsE0buN1abtnMoN_rBhC1tMBEK4pr7Qag.6YCMpZQxDlRNHQc.8bd_5xwvfl8n0MEC3F.KKjBW2606pXfyheM4LcEMmPNq.ARw6bzaGPNw8F8dLHgDVC8_f14xZ8pTtIfrqaPcPMtDb.1IRSgjWt_u7Zml60_B0; chakra-ui-color-mode=dark; __cf_bm=wBfRXaYLMs6NxVXa4d9N5TiH6LCEI0p1bbCt9Y7srP8-1730032456-1.0.1.1-aQ5js33y8qH28X7_LR0rW5aWP9lCDyHGK2T2aXaUy0UZB8gG5YThWnQ74el1r0tLMzUk2DjucswZBajY9rIHoKW.p88JGiooHfIKXFC9yYA',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
}

# url = 'https://api.dexscreener.com/latest/dex/pairs/ton/eqc0ocg895i5hqqa2opwsh8x7zbreujt-xmmcqspliztlwez'
url = 'https://api.dexscreener.com/orders/v1/ton/EQCtfhymElS-Sql9UuI3ZvOmGbK1T8psFQyh2BdGAirmqJ21'
response = requests.get(url=url, headers=headers)

resp = response.text

pprint.pprint(resp)


