#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .handlers import watchtower

URLS = [
    (r"/", watchtower.WatchtowerListHandler),
    (r"/data_watchtower/v1/watchtower", watchtower.WatchtowerHandler),
    (r"/data_watchtower/v1/watchtowers", watchtower.WatchtowerHandler),

]
