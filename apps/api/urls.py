#!/usr/bin/env python
# -*- coding: utf-8 -*-
import handlers.invitation

HANDLERS = [
    (r"/api/v1/invitation/search", handlers.invitation.InvitationSearchHandler),
    (r"/api/v1/invitation/create", handlers.invitation.InvitationCreateHandler),
]
