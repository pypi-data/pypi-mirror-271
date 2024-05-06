# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-app-ui
# FileName:     device.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from airtest.core.android.constant import TOUCH_METHOD, CAP_METHOD


def get_default_url(device_id: str) -> str:
    return "android://127.0.0.1:5037/{}?cap_method={}&touch_method={}".format(
        device_id, CAP_METHOD.JAVACAP, TOUCH_METHOD.ADBTOUCH
    )


def get_minicap_url(device_id: str) -> str:
    return "android://127.0.0.1:5037/{}?cap_method={}&touch_method={}".format(
        device_id, CAP_METHOD.MINICAP, TOUCH_METHOD.ADBTOUCH
    )
