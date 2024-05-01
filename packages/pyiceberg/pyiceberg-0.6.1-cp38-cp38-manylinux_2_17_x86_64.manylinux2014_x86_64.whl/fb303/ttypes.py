#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#
# Autogenerated by Thrift Compiler (0.16.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#


from thrift.TRecursive import fix_spec

all_structs = []


class fb_status:
    """
    Common status reporting mechanism across all services

    """

    DEAD = 0
    STARTING = 1
    ALIVE = 2
    STOPPING = 3
    STOPPED = 4
    WARNING = 5

    _VALUES_TO_NAMES = {
        0: "DEAD",
        1: "STARTING",
        2: "ALIVE",
        3: "STOPPING",
        4: "STOPPED",
        5: "WARNING",
    }

    _NAMES_TO_VALUES = {
        "DEAD": 0,
        "STARTING": 1,
        "ALIVE": 2,
        "STOPPING": 3,
        "STOPPED": 4,
        "WARNING": 5,
    }


fix_spec(all_structs)
del all_structs
