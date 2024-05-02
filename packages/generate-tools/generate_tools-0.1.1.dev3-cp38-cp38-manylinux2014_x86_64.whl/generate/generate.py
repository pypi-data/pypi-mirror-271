# Copyright (C) 2022-2023 AyiinXd <https://github.com/AyiinXd>

# This file is part of GeneratorPassword.

# GeneratorPassword is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GeneratorPassword is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with GeneratorPassword.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import base64
import re
import string

from random import choice
from typing import Dict, Optional, Union

from .method import Method
from .tools import Tools


table = """
CREATE TABLE IF NOT EXISTS password(
    user_id INTEGER,
    key TEXT,
    random_id INTEGER
);
CREATE TABLE IF NOT EXISTS discount(
    user_id INTEGER,
    percent INTEGER
);
CREATE TABLE IF NOT EXISTS email(
    user_id INTEGER,
    username TEXT,
    domain TEXT
);
"""


class Generate(Method, Tools):
    def __init__(
        self,
        name: str = None,
        space_symbol: str = None,
    ):
        super().__init__()
        self.name = name if name else 'generate'
        self._space = space_symbol if space_symbol else '-_='
        
        # self.memory = Storage(name=name, extension='.db', table=table)
        self._string = string.ascii_letters
        self.loop = asyncio.get_event_loop_policy().get_event_loop()
        
        self._cache: dict = {}
        self.isAuthorize = None
        self.btnUrlRegex = re.compile(r"(\[([^\[]+?)\]\((?:/{0,2})(.+?)(:same)?\))")
        self._apiUrlPay = 'https://payinaja.vercel.app'
        self.start()

    # def authorize(self):
    #     if self.memory.is_connected:
    #         self.memory.close()

    #     self.memory.connect()

    def lock(self, key, string):
        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 128)
            encoded_chars.append(encoded_c)
        encoded_string = "".join(encoded_chars)
        arr2 = bytes(encoded_string, 'utf-8')
        return base64.urlsafe_b64encode(arr2)

    def unlock(key, encoded_string):
        decoded_chars = []
        decoded_bytes = base64.urlsafe_b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        for i in range(len(decoded_string)):
            key_c = key[i % len(key)]
            decoded_c = chr(ord(decoded_string[i]) - ord(key_c) % 128)
            decoded_chars.append(decoded_c)
        return "".join(decoded_chars)
