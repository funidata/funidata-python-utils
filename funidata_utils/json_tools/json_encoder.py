#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import datetime

import simplejson
from pydantic import BaseModel


class CustomJsonEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        if isinstance(o, datetime.date):
            return o.isoformat()

        if isinstance(o, BaseModel):
            return o.model_dump()

        return simplejson.JSONEncoder.default(self, o)
