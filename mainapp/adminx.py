# -*- coding: utf-8 -*-
from xadmin import views
import xadmin
class BaseSetting:
    enable_themes = True  # 开启主题功能
    use_bootswatch = True
    menu_style = 'accordion'   # 启用菜单样式
    site_title = ''             #设置标题
    site_footer = ''            #设置页尾


xadmin.site.register(views.BaseAdminView, BaseSetting)