"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""

# pylint: disable=unused-argument


import re
import hashlib
from typing import Any, ClassVar, List, Literal, Optional, Tuple, Union
from dataclasses import dataclass
from pathlib import Path
from math import inf

from mkdocs.exceptions import BuildError

from pyodide_mkdocs_theme.pyodide_macros.messages import Tip

from ... import html_builder as Html
from ...pyodide_logger import logger
from ...tools_and_constants import HtmlClass, Prefix, ScriptKind
from ...pages_and_ides_configs import IdeConfigKey
from ...parsing import build_code_fence, items_comma_joiner
from ...paths_utils import convert_url_to_utf8, to_uri
from ...plugin.maestro_IDE import MaestroIDE

from .ide_files_data import IdeFilesExtractor




#---------------------------------------------------------------------------------





@dataclass
class Ide:
    """
    Builds an editor + a terminal + the buttons and extra logistic needed for them.
    """

    # Defined on instantiation:
    #--------------------------

    my_env: MaestroIDE
    """ The MaestroEnv singleton """

    py_name: str
    """ Base name for the files to use (first argument passed to the macros)
        Partial path from the directory holding the sujet.md file, to the one holding all the
        other required files, ending with the common prefix for the exercice.
        Ex:   "exo" to extract:   "exo.py", "exo_corr.py", "exo_test.py", ...
                "sub_exA/exo" for:  "sub_exA/exo.py", "sub_exA/exo_corr.py", ...
    """

    mode: Union[Literal[""],Literal["_v"]]
    """ The terminal will be below (mode="") or on the right (mode="_v") of the editor.
        (what an awful interface, yeah... x) )
    """

    max_attempts: Optional[Union[int, Literal["+"]]]
    """ Maximum number of attempts before the solution admonition will become available.
        If None, use the global default value.
    """

    excluded: str
    """ String of spaces or coma separated python functions or modules/packages that are forbidden
        at runtime. By default, nothing is forbidden.
            - Every string section that matches a builtin callable forbid that function by
              replacing it with another function which will raise an error if called.
            - Every string section prefixed with a fot forbids a method call. Here a simple
              string containment check is done opn the user's code, to check it does not
              contain the desired method name with the dot before it.
            - Any other string section is considered as a module name and doing an import (in
              any way/syntax) involving that name will raise an error.

        Note that the restrictions are rather strict, and may have unexpected side effects, such
        as, forbidding `exec` will also forbid to import numpy, because the package relies on exec
        for some operations at import time.
        To circumvent such a kind of problems, use the white_list argument.
    """

    max_size: int
    """ Max height of the editor (in number of lines) """

    white_list: str
    """ String of spaces or coma separated python modules/packages names the have to be
        preloaded before the code restrictions are enforced on the user's side.
    """

    id: Optional[int]
    """ Used to disambiguate the ids of two IDEs, if the same file is used several times
        in the document.
    """

    auto_log_assert: Optional[bool]
    """ If True, failing assertions without feedback during the private tests will be
        augmented automatically with the code of the assertion itself. If None, use
        the global `show_assertion_code_on_failed_test` plugin value and defined in
        `CONFIG.showAssertionCodeOnFailedTest` in the JS runtime.
    """

    rec_limit: int
    """ If used, the recursion limit of the pyodide runtime will be updated before the user's
        code or the tests are run.
        Note that this also forbids the use of the `sys.setrecurionlimit` at runtime.
    """

    term_height: int
    """ Number of lines to define the height of the terminal (unless it's vertical) """


    # defined during post_init
    #-------------------------


    files_data: IdeFilesExtractor = None

    editor_name: str = ''
    """ tail part of most ids, in the shape of 'editor_{32 bits hexadecimal}' """

    max_attempts_symbol: str = ''
    """ Actual string representation to use when creating the counter under the IDE """

    indentation: str = ''
    """ Indentation on the left of the macro call, as str """


    #-------------------------


    MIN_IDE_ID_DIGITS: ClassVar[str] = 8

    INFINITY_SYMBOL: ClassVar[str] = "∞"


    ICON_TEMPLATE: ClassVar[str] = (
        "{lvl_up}/pyodide-mkdocs/IDE-and-buttons/images/icons8-{button_name}-64.png"
    )


    @property               # pylint: disable-next=all
    def has_corr(self):     return self.files_data.has_corr
    @property               # pylint: disable-next=all
    def has_secrets(self):  return self.files_data.has_secrets
    @property               # pylint: disable-next=all
    def has_rem(self):      return self.files_data.has_rem
    @property               # pylint: disable-next=all
    def has_vis_rem(self):  return self.files_data.has_vis_rem

    @property               # pylint: disable-next=all
    def has_any_corr_rem(self):
        return self.has_corr or self.has_rem or self.has_vis_rem



    def __post_init__(self):

        to_globals_if_none = (
            ('max_attempts', 'max_attempts_before_corr_available'),
            ('max_size',     'default_ide_height_lines'),
        )
        for prop,conf_prop in to_globals_if_none:
            if getattr(self, prop) is None:
                def_val = getattr(self.my_env, conf_prop)
                setattr(self, prop, def_val)

        self.files_data = IdeFilesExtractor(self.my_env, self.py_name, self.id)

        # Extract max number of attempts from file or macro argument, clean up the file if needed,
        # then pick the correct number of attempts and set it in the global structure.
        # Also defines self.ide_content.
        max_attempts = self._define_max_attempts_symbols_and_value()

        self._validate_config(max_attempts)


        if 0 <= self.rec_limit < self.my_env.MIN_RECURSION_LIMIT:
            raise BuildError(
                f"The recursion limit for {self} is set too low and may causes runtime troubles. "
                f"Please set it to at least { self.my_env.MIN_RECURSION_LIMIT }."
            )

        if self.id is not None and not isinstance(self.id, int):
            raise BuildError(f'The ID argument should be an integer, for {self}')


        # Extract python content and compute editor name:
        exo_py: Optional[Path] = self.files_data.exo_py
        id_ide: str = self._generate_id_ide(exo_py)
        self.editor_name = f"{ Prefix.editor_ }{ id_ide }"


        # Compute all code exclusions and white list of imports:
        white_list = self._compute_exclusions_and_white_list("white_list")
        excluded = self._compute_exclusions_and_white_list("excluded")
        excluded_methods = [ meth for meth in excluded if     meth.startswith('.') ]
        excluded =         [ meth for meth in excluded if not meth.startswith('.') ]


        # Search the indentation level for the current IDE:
        is_v = self.mode.strip('_')
        quotes = """['"]"""
        script_pattern = "" if not self.py_name else f"{quotes}{ self.py_name }{quotes}"
        id_pattern = r'(?!.*?ID\s*=)' if self.id is None else rf".*?ID\s*=\s*{ self.id }\b"

        ide_jinja_reg = re.compile( rf"IDE{ is_v }\(\s*{ script_pattern }{ id_pattern }" )
        self.indentation = self.my_env.get_indent_in_current_page(ide_jinja_reg)



        to_register: List[Tuple[IdeConfigKey,Any]] = [
            ('env_content',         self.files_data.env_content),
            ('user_content',        self.files_data.user_content),
            ('public_tests',        self.files_data.public_tests),
            ('secret_tests',        self.files_data.secret_tests),
            ('post_content',        self.files_data.post_content),
            ('corr_rem_config',     self.files_data.corr_rem_bit_mask),
            ('attempts_left',       max_attempts),
            ("excluded",            excluded),
            ("excluded_methods",    excluded_methods),
            ("white_list",          white_list),
            ("auto_log_assert",     self.auto_log_assert),
            ("rec_limit",           self.rec_limit),
        ]
        for field,value in to_register:
            self.my_env.set_current_page_js_data(self.editor_name, field, value)



    #-----------------------------------------------------------------------------


    def __str__(self):
        with_id = '' if self.id is None else f', ID={self.id}'
        return f"IDE('{self.py_name}'{with_id}), in file {self.my_env.page.file.src_uri}"


    def _define_max_attempts_symbols_and_value(self):
        """
        Any MAX value defined in the file takes precedence, because it's not possible to know
        if the value coming from the macro is the default one or not.
        """
        max_ide = str(self.max_attempts)        # from macro call

        # If something about MAX in the file, it has precedence (if exists -> legacy...)
        max_from_file = self.files_data.file_max_attempts
        if max_from_file != "":
            max_ide = max_from_file

        is_inf = max_ide in ("+", "1000")     # 1000: legacy...

        # If ever there are neither correction nor remark, or if no tests, use also inf:
        is_inf = is_inf or not self.has_any_corr_rem or not self.has_secrets

        self.max_attempts_symbol = self.INFINITY_SYMBOL if is_inf else str(max_ide)

        max_attempts = inf if is_inf else int(max_ide)
        return max_attempts



    def _validate_config(self, max_attempts: Union[int,float]):
        msg: Optional[Tuple[str,str]] = None

        if (self.my_env.forbid_secrets_without_corr_or_REMs
            and self.has_secrets and not self.has_any_corr_rem
        ):
            msg = (
                "A `secrets` section exist but there are no `corr` section, REM or VIS_REM file.",
                "forbid_secrets_without_corr_or_REMs"
            )

        elements = [*filter(bool,(
            "a correction"   * (not self.has_corr),
            "a REM file"     * (not self.has_rem),
            "a VIS_REM file" * (not self.has_vis_rem),
        ))]
        elt_msg = items_comma_joiner(elements, 'and')
        single  = len(elements)==1
        elt_msg = f"{ elt_msg } exist{ 's' * (single)}".capitalize()

        if (self.my_env.forbid_hidden_corr_and_REMs_without_secrets
            and self.has_any_corr_rem and not self.has_secrets
        ):
            msg = (
                f"{ elt_msg }, but there is no `secrets` section.",
                'forbid_hidden_corr_and_REMs_without_secrets'
            )

        if (self.my_env.forbid_corr_and_REMs_with_infinite_attempts
            and max_attempts==inf and self.has_any_corr_rem
        ):
            subject = "it" if single else "they"
            msg = (
                f"{ elt_msg }, but {subject} will never be visible because the number of "
                "attempts is set to infinity.",
                'forbid_corr_and_REMs_with_infinite_attempts'
            )

        if msg:
            msg, opt = msg
            msg = (
                f"Invalid configuration\n    {self}:\n    {msg}\n    You can deactivate this "
                f"check by setting plugins.pyodide_macros.build.{opt} to false in `mkdocs.yml`."
            )
            if self.my_env._dev_mode:       # pylint: disable=protected-access
                logger.error("DEV_MODE (expected x2) - " + msg)
            else:
                raise BuildError(msg)



    def _compute_exclusions_and_white_list(self, prop:str):
        """
        Convert a string argument (exclusions or white list) tot he equivalent list of data.
        """
        rule = (getattr(self, prop) or "").strip(' ;,')       # (never allow None)
        lst = re.split(r'[ ;,]+', rule) if rule else []
        return lst



    def _generate_id_ide(self, py_path:Optional[Path]):
        """
        Generate an id number for the current IDE (editor+terminal), as a "prefix_hash(32bits)".

        This id must be:
            - Unique to every IDE used throughout the whole website.
            - Stable, so that it can be used to identify what IDE goes with what file or what
              localeStorage data.

        Current strategy:
            - If the file exists, hash its path.
            - If there is no file, use the current global IDE_counter and hash its value as string.
            - The "mode" of the IDE is appended to the string before hashing.
            - Any ID value (macro argument) is also appended to the string before hashing.

        Uniqueness of the resulting hash is verified and a BuildError is raised if two identical
        hashes are encountered.
        """
        if py_path:
            path = str(py_path)
        else:
            path = str(self.my_env.ide_count)

        if self.mode:
            path += self.mode

        if self.id is not None:
            path += str(self.id)

        id_ide = hashlib.sha1(path.encode("utf-8")).hexdigest()

        if not self.my_env.register_if_unique(id_ide):
            raise BuildError(
                "The same editor ID got generated twice. If you are trying to use the same set"
                "of files for different IDEs, use the ID argument to disambiguate their id.\n"
               f"  Problematic call:  { self }\n"
               f"  Possible solution: add the ID:int keyword argument or change its value"
            )
        return id_ide




    #-----------------------------------------------------------------------------




    def make_ide(self) -> str:
        """
        Create an IDE (Editor+Terminal) within an Mkdocs document. {py_name}.py is loaded on
        the editor if present.
        NOTES:
            - Two modes are available : vertical or horizontal. Buttons are added through
                functional calls.
            - The last span hides the code content of the IDE when loaded.
        """
        # Mark the page as needing this kind of scripts in the body section:
        self.my_env.set_current_page_insertion_needs(ScriptKind.pyodide)

        ide_layout = self.generate_empty_ide()
        buttons = self.generate_buttons_row()
        global_layout = Html.div(
            ide_layout+buttons,
            id = f"{ Prefix.global_ }{ self.editor_name }",
            kls = HtmlClass.py_mk_ide,
        )
        solution_div = self._build_corr_and_rem()

        return global_layout + solution_div



    def generate_empty_ide(self) -> str:
        """
        Generate the global layout that will receive later the ace elements.
        """
        is_v = self.mode == '_v'
        toggle_txt = '###'
        tip: Tip = self.my_env.lang.comments
        msg = str(tip)

        shortcut_comment_asserts = Html.span(
            toggle_txt + Html.tooltip(msg, tip.em, shift=95),
            id = Prefix.comment_ + self.editor_name,
            kls = f'{HtmlClass.comment} {HtmlClass.tooltip}',
        )
        editor_div = Html.div(
            id = self.editor_name,
            is_v = str(is_v).lower(),
            mode = self.mode,
            max_size = self.max_size,
            py_name = self.py_name,
        )
        editor_wrapper = Html.div(
            editor_div + shortcut_comment_asserts,
            kls = Prefix.comment_ + HtmlClass.py_mk_wrapper
        )

        separator = Html.div(
            kls= HtmlClass.ide_separator + self.mode
        )
        terminal_div = Html.terminal(
            Prefix.term_ + self.editor_name ,
            kls = f"{ HtmlClass.term_editor }{ self.mode } { HtmlClass.py_mk_terminal }",
            n_lines_h = self.term_height * (not is_v),
            is_v = is_v,
            env=self.my_env,
        )

        return Html.div(
            f"{ editor_wrapper }{ separator }{ terminal_div }",
            kls = f"{ HtmlClass.py_mk_wrapper }{ self.mode }",
        )





    def _build_corr_and_rem(self):
        """
        Build the correction and REM holders. The rendered template is something like the
        following, with the indentation level of the most outer div equal to the indentation
        level of the IDE macro text in the markdown file.
        Depending on the presence/absence of corr, REM and VIS_REM files, some elements may
        be missing. In this method:

        | var | meaning |
        |-|-|
        | `at_least_one` | corr or REM (=> inside admonition) |
        | `anything` | corr or REM or VIS_REM |

        Overall structure of the generated markdown (mixed with html):

                <div markdown="1" id="solution_editor_id"       <<< ALWAYS
                     class="py_mk_hidden" >

                ENCRYPTION_TOKEN                                <<< at least one and encryption ON

                ??? tip "Solution"                              <<< at least one

                    <div markdown="1" style="padding:1em">      <<< at least one

                    ```python linenums="1"'                     <<< solution
                    --8<-- "{ corr_uri }"                       <<< solution
                    ```                                         <<< solution

                    ___Remarques :___                           <<< remark & solution

                    --8<-- "{ rem_uri }"                        <<< remark

                    </div>                                      <<< at least one

                --8<-- "{ vis_rem_uri }"                        <<< vis_rem

                ENCRYPTION_TOKEN                                <<< at least one and encryption ON

                </div>                                          <<< ALWAYS

        Don't forget that empty lines are mandatory to render the "md in html" as expected.
        """

        # Prepare data first (to ease reading of the below sections)
        sol_title = ' & '.join(filter(bool, [
            str(self.my_env.lang.title_corr) * self.has_corr,
            str(self.my_env.lang.title_rem) * self.has_rem
        ]))
        corr_content = self.files_data.corr_content
        at_least_one = self.has_corr or self.has_rem
        anything     = at_least_one or self.has_vis_rem
        with_encrypt = self.my_env.encrypt_corrections_and_rems and anything
        extra_tokens = ( self.my_env.ENCRYPTION_TOKEN, ) * with_encrypt


        # Build the whole div content:
        md_div = [         '',   # Extra empty line to enforce proper rendering of the md around
                           f'<div markdown="1" id="{ Prefix.solution_ }{ self.editor_name }" '
                           f'     class="{ HtmlClass.py_mk_hidden }" data-search-exclude >',
                            *extra_tokens ]
        if at_least_one:
            md_div.append( f'??? tip "{ sol_title }"' )
            md_div.append(  '    <div markdown="1" style="margin:1.7em 1em" >' )

        if self.has_corr:
            # first indentation must be removed, EXCEPT one level, because handled lower
            # for the whole block
            one_level = '    '
            fence = build_code_fence(
                corr_content,
                one_level + self.indentation,
                title=str(self.my_env.lang.corr)
            )
            md_div.append(  one_level+fence.strip())

        if self.has_corr and self.has_rem:
            rem = self.my_env.lang.rem
            md_div.append( f'    <span class="{ HtmlClass.rem_fake_h3 }">{ rem } :</span>')

        if self.has_rem:
            rem = self._rem_inclusion('rem_rel_path')
            md_div.append( f'    { rem }' )

        if at_least_one:
            md_div.append(  '    </div>')

        if self.has_vis_rem:
            vis_rem = self._rem_inclusion('vis_rem_rel_path')
            md_div.append(  vis_rem )

        md_div.extend((     *extra_tokens,
                            '</div>\n',    ))
                # The extra linefeed is there to enforce md rendering of the following sections

        # Add extra indentation according to IDE's insertion:
        if self.indentation:
            md_div = [ s and self.indentation + s for s in md_div ]

        # Join every item with extra gaps, to following md rendering requirements
        out = '\n\n'.join(md_div)
        return out


    def _rem_inclusion(self, rem_path_kind:str):
        path_str = str(getattr(self.files_data, rem_path_kind))
        rem_uri  = to_uri( convert_url_to_utf8(path_str) )
        return f'--8<-- "{ rem_uri }"'



    def generate_buttons_row(self) -> str:
        """
        Build all buttons below an "ide" (editor+terminal).
        """
        cnt_txt, cnt_or_inf = self.my_env.lang.attempts_left.msg, self.max_attempts_symbol
        cnt_txt_span = Html.span(cnt_txt + " : ", kls=HtmlClass.compteur_txt)
        cnt_n_span = Html.span(cnt_or_inf, id=f'{ Prefix.compteur_ }{ self.editor_name }')

        buttons = [
            self.create_button("play"),
            self.create_button("check", btn_kind="validate") if self.has_secrets else "",
            self.create_button("download", margin_left=1 ),
            self.create_upload_button(margin_right=1),
            self.create_button("restart"),
            self.create_button("save"),
            Html.span(f"{ cnt_txt_span }{ cnt_n_span }/{ cnt_or_inf }", kls=HtmlClass.compteur),
        ]
        buttons_div = Html.div( ''.join(buttons), kls=HtmlClass.ide_buttons_div )
        return buttons_div



    def create_button(
        self, button_name: str,
        *,
        btn_kind:str=None,
        margin_left:float=0.2, margin_right:float=0.2,
        extra_content:str = "",
        **kwargs
    ) -> str:
        """
        Build one button, given its name.

        @btn_kind:      The name of the JS function to bind the button click event to. If not
                        given, use the lowercase version of button_name.
        @margin_...:    CSS formatting as floats (em units). By default, 0.2 on each side.
        @extra_content: Allow to inject some additional html inside the button tag.
        @**kwargs:      All the remaining kwargs are attributes added to the button tag.
        """
        if btn_kind is None:
            btn_kind = button_name.lower()

        tip: Tip     = getattr(self.my_env.lang, button_name)
        span_tooltip = Html.tooltip(tip, tip.em)
        lvl_up       = self.my_env.level_up_from_current_page()
        img_link     = self.ICON_TEMPLATE.format(lvl_up=lvl_up, button_name=button_name)
        img          = Html.img(src=img_link, kls=HtmlClass.skip_light_box)
        button_html  = Html.button(
            f'{ img }{ span_tooltip }{ extra_content }',
            kls = HtmlClass.tooltip,
            btn_kind = btn_kind,
            style = f"margin-left:{margin_left}em; margin-right:{margin_right}em;",
            **kwargs,
            type='button',
                # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#notes
        )
        return button_html



    def create_upload_button(self, margin_right:float = 1) -> str:
        """
        @brief : Create upload button for an IDE number {id_ide}.
        @details : Use an HTML input to upload a file from user. The user clicks on the button to
        fire a JS event that triggers the hidden input.
        """

        input_button_controller = Html.input(
            id = f"{ Prefix.input_ }{ self.editor_name }",
            kls = HtmlClass.py_mk_hidden,
            type = 'file',
            name = 'file',
            enctype = "multipart/form-data",
        )
        button = self.create_button(
            "upload",
            margin_right = margin_right,
            extra_content = input_button_controller,
        )
        return button
