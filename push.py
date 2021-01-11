# -*- coding: utf-8 -*-

import jpush
from jpush import common

# 此处换成各自的app_key和master_secret
app_key = '228a772f477c0357d92c64d1'
master_secret = 'b0e838dd26364ead8ad98402'

_jpush = jpush.JPush(app_key, master_secret)


def all(alertMessage, titleMessage, href):
    push = _jpush.create_push()
    push.audience = jpush.audience(
        jpush.alias('45145')
    )
    android = jpush.android(alert=alertMessage, title=titleMessage, extras={'href': href})
    push.notification = jpush.notification(alert=alertMessage, android=android)
    push.platform = jpush.all_
    try:
        response = push.send()
        print('push success')
    except common.Unauthorized:
        raise common.Unauthorized("Unauthorized")
    except common.APIConnectionException:
        raise common.APIConnectionException("conn")
    except common.JPushFailure:
        print("JPushFailure")
    except:
        print("Exception")
