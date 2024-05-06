# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-app-ui
# FileName:     platforms.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/04/24
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
from capp_ui.device import get_minicap_url, get_default_url
from capp_ui.mobile_terminals import Phone, DEFAULT_PLATFORM, WINDOWS_PLATFORM


class PlatformService(object):

    def __init__(self, device_id: str, port: int, enable_debug: bool = False, platform: str = "Android") -> None:
        # 暂时支持Android和Windows平台
        self.default_device = get_default_url(device_id=device_id)
        if platform == DEFAULT_PLATFORM:
            self.device = Phone(
                device_id=device_id,
                port=port,
                device_conn=self.default_device,
                platform=platform,
                enable_debug=enable_debug
            )
        elif platform == WINDOWS_PLATFORM:
            pass
        else:
            raise ValueError("The platform configuration only supports Andriod and Windows.")

    @classmethod
    def minicap_device(cls, device_id: str, enable_debug: bool, platform: str, port: int) -> Phone:
        min_device = get_minicap_url(device_id=device_id)
        return Phone(
            port=port,
            device_id=device_id,
            device_conn=min_device,
            platform=platform,
            enable_debug=enable_debug,
        )
