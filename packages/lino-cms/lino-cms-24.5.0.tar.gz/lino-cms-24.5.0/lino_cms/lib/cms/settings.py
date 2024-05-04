# -*- coding: UTF-8 -*-
# Copyright 2016-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.projects.std.settings import *
from lino_cms import SETUP_INFO


class Site(Site):

    verbose_name = "Lino CMS"
    description = SETUP_INFO['description']
    version = SETUP_INFO['version']
    url = SETUP_INFO['url']
    # use_linod = True

    # demo_fixtures = ['std', 'demo', 'demo2', 'checkdata', 'checksummaries']
    demo_fixtures = ['std', 'demo', 'demo2', 'checkdata']
    user_types_module = 'lino_cms.lib.cms.user_types'
    custom_layouts_module = 'lino_cms.lib.cms.layouts'
    migration_class = 'lino_cms.lib.cms.migrate.Migrator'
    # default_ui = "lino_react.react"

    default_ui = None
    web_front_ends = [(None, "lino.modlib.publisher"),
                      ('admin', "lino_react.react")]

    # ('ext', "lino.modlib.extjs")]

    def get_installed_plugins(self):
        """Implements :meth:`lino.core.site.Site.get_installed_plugins`.

        """
        yield super().get_installed_plugins()
        yield 'lino_cms.lib.cms'
        yield 'lino_cms.lib.users'
        yield 'lino_xl.lib.contacts'
        # yield 'lino_cms.lib.cal'
        # yield 'lino_xl.lib.calview'
        yield 'lino_xl.lib.pages'
        yield 'lino_xl.lib.blogs'
        yield 'lino_xl.lib.albums'
        yield 'lino_xl.lib.topics'
        yield 'lino_xl.lib.sources'
        yield 'lino.modlib.comments'
        # yield 'lino.modlib.uploads'
        yield 'lino.modlib.help'
        yield 'lino.modlib.publisher'
        # yield 'lino.modlib.summaries'
        yield 'lino.modlib.checkdata'  # fill body_preview during prep

    # def setup_quicklinks(self, ut, tb):
    #     super(Site, self).setup_quicklinks(ut, tb)

    def get_plugin_configs(self):
        yield super().get_plugin_configs()
        # yield ('system', 'use_dashboard_layouts', True)
        # yield ('linod', 'use_channels', True)
        yield ('users', 'allow_online_registration', True)
        yield 'users', 'third_party_authentication', True
        # yield ('cal', 'with_demo_appointments', False)
        yield ('help', 'make_help_pages', True)
        yield ('help', 'use_contacts', True)
        yield ('help', 'include_useless', True)
        yield ('memo', 'short_preview_length', 1200)
        yield ('publisher', 'locations',
               (('b', 'blogs.LatestEntries'),
                ('p', 'pages.Pages'),
                ('r', 'uploads.Uploads'),
                ('s', 'sources.Sources'),
                ('t', 'topics.Topics'),
                ('u', 'users.Users')))


from lino.core.auth.utils import activate_social_auth_testing

activate_social_auth_testing(globals())
