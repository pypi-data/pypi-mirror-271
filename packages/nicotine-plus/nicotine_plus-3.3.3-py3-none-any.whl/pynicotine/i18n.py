# COPYRIGHT (C) 2020-2024 Nicotine+ Contributors
#
# GNU GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gettext
import locale
import os
import sys

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.normpath(os.path.join(CURRENT_PATH, ".."))
LOCALE_PATH = os.path.join(CURRENT_PATH, "locale")
TRANSLATION_DOMAIN = "nicotine"
LANGUAGES = (
    ("ca", "Català"),
    ("de", "Deutsch"),
    ("en", "English"),
    ("es_CL", "Español (Chile)"),
    ("es_ES", "Español (España)"),
    ("et", "Eesti"),
    ("fr", "Français"),
    ("hu", "Magyar"),
    ("it", "Italiano"),
    ("lv", "Latviešu"),
    ("nl", "Nederlands"),
    ("pl", "Polski"),
    ("pt_BR", "Português (Brasil)"),
    ("pt_PT", "Português (Portugal)"),
    ("ru", "Русский"),
    ("tr", "Türkçe"),
    ("uk", "Українська"),
    ("zh_CN", "汉语")
)


def _set_system_language(language=None):
    """Extracts the default system language and applies it on systems that
    don't set the 'LANGUAGE' environment variable by default (Windows,
    macOS)"""

    if not language and "LANGUAGE" not in os.environ:
        if sys.platform == "win32":
            import ctypes
            windll = ctypes.windll.kernel32
            language = locale.windows_locale.get(windll.GetUserDefaultUILanguage())

        elif sys.platform == "darwin":
            try:
                import subprocess
                language_output = subprocess.check_output(("defaults", "read", "-g", "AppleLanguages"))
                languages = language_output.decode("utf-8").strip('()\n" ').split(",")
                language = next(iter(languages), None)

            except Exception as error:
                print("Cannot load translations for default system language: %s", error)

    if language:
        os.environ["LANGUAGE"] = language


def apply_translations(language=None):

    # Use the same language as the rest of the system
    _set_system_language(language)

    # Install translations for Python
    gettext.install(TRANSLATION_DOMAIN, LOCALE_PATH)
