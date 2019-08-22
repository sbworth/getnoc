# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
# ConfDB media sources video syntax
# ----------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from __future__ import absolute_import

# NOC modules
from ....defs import DEF
from ....patterns import ANY, INTEGER, BOOL

MEDIA_SOURCES_VIDEO_SYNTAX = DEF(
    "video",
    [
        DEF(
            ANY,
            [
                DEF(
                    "settings",
                    [
                        DEF(
                            "brightness",
                            [
                                DEF(
                                    INTEGER,
                                    name="brightness",
                                    required=True,
                                    gen="make_video_brightness",
                                )
                            ],
                        ),
                        DEF(
                            "saturation",
                            [
                                DEF(
                                    INTEGER,
                                    name="saturation",
                                    required=True,
                                    gen="make_video_saturation",
                                )
                            ],
                        ),
                        DEF(
                            "contrast",
                            [
                                DEF(
                                    INTEGER,
                                    name="contrast",
                                    required=True,
                                    gen="make_video_contrast",
                                )
                            ],
                        ),
                        DEF(
                            "sharpness",
                            [
                                DEF(
                                    INTEGER,
                                    name="sharpness",
                                    required=True,
                                    gen="make_video_sharpness",
                                )
                            ],
                        ),
                        DEF(
                            "white-balance",
                            [
                                DEF(
                                    "admin-status",
                                    [
                                        DEF(
                                            BOOL,
                                            required=True,
                                            name="admin_status",
                                            gen="make_video_white_balance_admin_status",
                                        )
                                    ],
                                ),
                                DEF("auto", gen="make_video_white_balance_auto"),
                                DEF(
                                    "cr-gain",
                                    [
                                        DEF(
                                            INTEGER,
                                            name="cr_gain",
                                            required=True,
                                            gen="make_video_white_balance_cr_gain",
                                        )
                                    ],
                                ),
                                DEF(
                                    "gb-gain",
                                    [
                                        DEF(
                                            INTEGER,
                                            name="gb_gain",
                                            required=True,
                                            gen="make_video_white_balance_gb_gain",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        DEF(
                            "black-light-compensation",
                            [
                                DEF(
                                    "admin-status",
                                    [
                                        DEF(
                                            BOOL,
                                            required=True,
                                            name="admin_status",
                                            gen="make_video_black_light_compensation_admin_status",
                                        )
                                    ],
                                )
                            ],
                        ),
                        DEF(
                            "wide-dynamic-range",
                            [
                                DEF(
                                    "admin-status",
                                    [
                                        DEF(
                                            BOOL,
                                            required=True,
                                            name="admin_status",
                                            gen="make_video_wide_dynamic_range_admin_status",
                                        )
                                    ],
                                ),
                                DEF(
                                    "level",
                                    [
                                        DEF(
                                            INTEGER,
                                            name="level",
                                            required=True,
                                            gen="make_video_wide_dynamic_range_level",
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
            name="name",
            multi=True,
        )
    ],
)