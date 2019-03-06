# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function
import plyxproto.model as m
from plyxproto.helpers import Visitor
import argparse
import plyxproto.parser as plyxproto
import traceback
import sys
import jinja2
import os
import copy
import pdb

# Options that are always allowed
COMMON_OPTIONS = ["help_text", "gui_hidden"]

class XProtoValidator(object):
    def __init__(self, models):
        self.models = models

    def error(self, model, field, message):
        # TODO: Line number information
        print("Model '%s' Field '%s': %s" % (model["name"], field["name"], message), file=sys.stderr)

    def allow_options(self, model, field, options):
        """ Only allow the options specified in `options`. Throw error otherwise.
        """
        options = COMMON_OPTIONS + options

        for (k, v) in field.get("options", {}).items():
            allowed = False
            for option in options:
                if "=" in option:
                    (optname, optval) = option.split("=")
                    if optname==k and optval==v:
                        allowed = True
                else:
                    if option==k:
                        allowed = True

            if not allowed:
                self.error(model, field, "Option %s=%s is not allowed" % (k,v))

    def validate_field_date(self, model, field):
        pass

    def validate_field_string(self, model, field):
        self.allow_options(model, field, ["blank", "choices", "content_type", "db_index", "default", "max_length", "modifier", "null", "unique", "varchar"])

        # A string with a "content_type=date" is actually a date
        content_type = field.get("content_type")
        if content_type == "date":
            self.validate_field_date(self, model, field)
            return

        if content_type and content_type != "stripped":
            self.error(model, field, "Content type %s is not allowed" % content_type)

    def validate_field_bool(self, model, field):
        self.allow_options(model, field, ["db_index", "default=True", "default=False", "modifier", "null=False"])

    def validate_field_float(self, model, field):
        self.allow_options(model, field, ["default"])

    def validate_field_link_onetomany(self, model, field):
        self.allow_options(model, field,
                           ["blank", "db_index", "default", "model", "link_type=manytoone",
                            "modifier", "null", "port", "type=link", "unique"])

    def validate_field_link_manytomany(self, model, field):
        self.allow_options(model, field,
                           ["blank", "db_index", "default", "model", "link_type=manytomany",
                            "modifier", "null", "port", "type=link", "unique"])

    def validate_field_link(self, model, field):
        link_type = field.get("options",{}).get("link_type")
        if link_type == "manytoone":
            self.validate_field_link_onetomany(model, field)
        elif link_type == "manytomany":
            self.validate_field_link_manytomany(model, field)
        else:
            self.error("Unknown link_type %s" % link_type)

    def validate_field_integer(self, model, field):
        # An integer with an option "type=link" is actually a link
        if field.get("options", {}).get("type") == "link":
            self.validate_field_link(model, field)
            return

        self.allow_options(model, field, ["blank", "db_index", "default", "modifier", "null"])

    def validate_field(self, model, field):
        if field["type"] == "string":
            self.validate_field_string(model, field)
        elif field["type"] in ["int32", "uint32"]:
            self.validate_field_integer(model, field)
        elif field["type"] == "float":
            self.validate_field_float(model, field)
        elif field["type"] == "bool":
            self.validate_field_bool(model, field)
        else:
            self.error(model, field, "Unknown field type %s" % field["type"])

    def validate_model(self, model):
        for field in model["fields"]:
            self.validate_field(model, field)
        import pdb;
        pdb.set_trace()

    def validate(self):
        for (name, model) in self.models.items():
            self.validate_model(model)