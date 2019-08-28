# -*- coding: utf-8 -*-
from xadmin import views
import xadmin
class BaseSetting(object):
    enable_themes = True  # 开启主题功能
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '后台管理'
    site_footer = '@'
    menu_style = 'accordion'  # 左边导航栏 收缩 手风琴


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)