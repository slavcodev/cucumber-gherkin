# This file is generated. Do not edit! Edit gherkin-python.razor instead.
from __future__ import annotations

from collections import deque
from collections.abc import Callable
from typing import TypeVar, cast

from .ast_builder import AstBuilder
from .errors import (
    CompositeParserException,
    ParserException,
    UnexpectedEOFException,
    UnexpectedTokenException,
)
from .parser_types import GherkinDocument
from .token import Token
from .token_matcher import TokenMatcher
from .token_scanner import TokenScanner

_T = TypeVar("_T")
_U = TypeVar("_U")
_V = TypeVar("_V")

RULE_TYPE = [
    "None",
    "_EOF",  # #EOF
    "_Empty",  # #Empty
    "_Comment",  # #Comment
    "_TagLine",  # #TagLine
    "_FeatureLine",  # #FeatureLine
    "_RuleLine",  # #RuleLine
    "_BackgroundLine",  # #BackgroundLine
    "_ScenarioLine",  # #ScenarioLine
    "_ExamplesLine",  # #ExamplesLine
    "_StepLine",  # #StepLine
    "_DocStringSeparator",  # #DocStringSeparator
    "_TableRow",  # #TableRow
    "_Language",  # #Language
    "_Other",  # #Other
    "GherkinDocument",  # GherkinDocument! := Feature?
    "Feature",  # Feature! := FeatureHeader Background? ScenarioDefinition* Rule*
    "FeatureHeader",  # FeatureHeader! := #Language? Tags? #FeatureLine DescriptionHelper
    "Rule",  # Rule! := RuleHeader Background? ScenarioDefinition*
    "RuleHeader",  # RuleHeader! := Tags? #RuleLine DescriptionHelper
    "Background",  # Background! := #BackgroundLine DescriptionHelper Step*
    "ScenarioDefinition",  # ScenarioDefinition! [#Empty|#Comment|#TagLine->#ScenarioLine] := Tags? Scenario
    "Scenario",  # Scenario! := #ScenarioLine DescriptionHelper Step* ExamplesDefinition*
    "ExamplesDefinition",  # ExamplesDefinition! [#Empty|#Comment|#TagLine->#ExamplesLine] := Tags? Examples
    "Examples",  # Examples! := #ExamplesLine DescriptionHelper ExamplesTable?
    "ExamplesTable",  # ExamplesTable! := #TableRow #TableRow*
    "Step",  # Step! := #StepLine StepArg?
    "StepArg",  # StepArg := (DataTable | DocString)
    "DataTable",  # DataTable! := #TableRow+
    "DocString",  # DocString! := #DocStringSeparator #Other* #DocStringSeparator
    "Tags",  # Tags! := #TagLine+
    "DescriptionHelper",  # DescriptionHelper := #Empty* Description?
    "Description",  # Description! := (#Other | #Comment)+
]


class ParserContext:
    def __init__(
        self,
        token_scanner: TokenScanner,
        token_matcher: TokenMatcher,
        token_queue: deque[Token],
        errors: list[ParserException],
    ) -> None:
        self.token_scanner = token_scanner
        self.token_matcher = token_matcher
        self.token_queue = token_queue
        self.errors = errors


class Parser:
    def __init__(self, ast_builder: AstBuilder | None = None) -> None:
        self.ast_builder = ast_builder if ast_builder is not None else AstBuilder()
        self.stop_at_first_error = False

    def parse(
        self,
        token_scanner_or_str: TokenScanner | str,
        token_matcher: TokenMatcher | None = None,
    ) -> GherkinDocument:
        token_scanner = (
            TokenScanner(token_scanner_or_str)
            if isinstance(token_scanner_or_str, str)
            else token_scanner_or_str
        )
        self.ast_builder.reset()
        if token_matcher is None:
            token_matcher = TokenMatcher()
        token_matcher.reset()
        context = ParserContext(token_scanner, token_matcher, deque(), [])

        self.start_rule(context, "GherkinDocument")
        state = 0
        token = None
        while True:
            token = self.read_token(context)
            state = self.match_token(state, token, context)
            if token.eof():
                break

        self.end_rule(context, "GherkinDocument")

        if context.errors:
            raise CompositeParserException(context.errors)

        return cast(GherkinDocument, self.get_result())

    def build(self, context: ParserContext, token: Token) -> None:
        self.handle_ast_error(context, token, self.ast_builder.build)

    def add_error(self, context: ParserContext, error: ParserException) -> None:
        if str(error) not in (str(e) for e in context.errors):
            context.errors.append(error)
            if len(context.errors) > 10:
                raise CompositeParserException(context.errors)

    def start_rule(self, context: ParserContext, rule_type: str) -> None:
        self.handle_ast_error(context, rule_type, self.ast_builder.start_rule)

    def end_rule(self, context: ParserContext, rule_type: str) -> None:
        self.handle_ast_error(context, rule_type, self.ast_builder.end_rule)

    def get_result(self) -> object:
        return self.ast_builder.get_result()

    def read_token(self, context: ParserContext) -> Token:
        if context.token_queue:
            return context.token_queue.popleft()
        return context.token_scanner.read()

    def match_EOF(self, context: ParserContext, token: Token) -> bool:
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_EOF
        )

    def match_Empty(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_Empty
        )

    def match_Comment(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_Comment
        )

    def match_TagLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_TagLine
        )

    def match_FeatureLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_FeatureLine
        )

    def match_RuleLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_RuleLine
        )

    def match_BackgroundLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_BackgroundLine
        )

    def match_ScenarioLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_ScenarioLine
        )

    def match_ExamplesLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_ExamplesLine
        )

    def match_StepLine(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_StepLine
        )

    def match_DocStringSeparator(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_DocStringSeparator
        )

    def match_TableRow(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_TableRow
        )

    def match_Language(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_Language
        )

    def match_Other(self, context: ParserContext, token: Token) -> bool:
        if token.eof():
            return False
        return self.handle_external_error(
            context, False, token, context.token_matcher.match_Other
        )

    def match_token(self, state: int, token: Token, context: ParserContext) -> int:
        state_map: dict[int, Callable[[Token, ParserContext], int]] = {
            0: self.match_token_at_0,
            1: self.match_token_at_1,
            2: self.match_token_at_2,
            3: self.match_token_at_3,
            4: self.match_token_at_4,
            5: self.match_token_at_5,
            6: self.match_token_at_6,
            7: self.match_token_at_7,
            8: self.match_token_at_8,
            9: self.match_token_at_9,
            10: self.match_token_at_10,
            11: self.match_token_at_11,
            12: self.match_token_at_12,
            13: self.match_token_at_13,
            14: self.match_token_at_14,
            15: self.match_token_at_15,
            16: self.match_token_at_16,
            17: self.match_token_at_17,
            18: self.match_token_at_18,
            19: self.match_token_at_19,
            20: self.match_token_at_20,
            21: self.match_token_at_21,
            22: self.match_token_at_22,
            23: self.match_token_at_23,
            24: self.match_token_at_24,
            25: self.match_token_at_25,
            26: self.match_token_at_26,
            27: self.match_token_at_27,
            28: self.match_token_at_28,
            29: self.match_token_at_29,
            30: self.match_token_at_30,
            31: self.match_token_at_31,
            32: self.match_token_at_32,
            33: self.match_token_at_33,
            35: self.match_token_at_35,
            36: self.match_token_at_36,
            37: self.match_token_at_37,
            38: self.match_token_at_38,
            39: self.match_token_at_39,
            40: self.match_token_at_40,
            41: self.match_token_at_41,
            42: self.match_token_at_42,
        }

        if state not in state_map:
            raise RuntimeError("Unknown state: " + str(state))

        return state_map[state](token, context)

    # Start
    def match_token_at_0(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.build(context, token)
            return 34
        if self.match_Language(context, token):
            self.start_rule(context, "Feature")
            self.start_rule(context, "FeatureHeader")
            self.build(context, token)
            return 1
        if self.match_TagLine(context, token):
            self.start_rule(context, "Feature")
            self.start_rule(context, "FeatureHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 2
        if self.match_FeatureLine(context, token):
            self.start_rule(context, "Feature")
            self.start_rule(context, "FeatureHeader")
            self.build(context, token)
            return 3
        if self.match_Comment(context, token):
            self.build(context, token)
            return 0
        if self.match_Empty(context, token):
            self.build(context, token)
            return 0

        state_comment = "State: 0 - Start"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Language",
            "#TagLine",
            "#FeatureLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 0

    # GherkinDocument:0>Feature:0>FeatureHeader:0>#Language:0
    def match_token_at_1(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 2
        if self.match_FeatureLine(context, token):
            self.build(context, token)
            return 3
        if self.match_Comment(context, token):
            self.build(context, token)
            return 1
        if self.match_Empty(context, token):
            self.build(context, token)
            return 1

        state_comment = "State: 1 - GherkinDocument:0>Feature:0>FeatureHeader:0>#Language:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#FeatureLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 1

    # GherkinDocument:0>Feature:0>FeatureHeader:1>Tags:0>#TagLine:0
    def match_token_at_2(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.build(context, token)
            return 2
        if self.match_FeatureLine(context, token):
            self.end_rule(context, "Tags")
            self.build(context, token)
            return 3
        if self.match_Comment(context, token):
            self.build(context, token)
            return 2
        if self.match_Empty(context, token):
            self.build(context, token)
            return 2

        state_comment = "State: 2 - GherkinDocument:0>Feature:0>FeatureHeader:1>Tags:0>#TagLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#FeatureLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 2

    # GherkinDocument:0>Feature:0>FeatureHeader:2>#FeatureLine:0
    def match_token_at_3(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "FeatureHeader")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Empty(context, token):
            self.build(context, token)
            return 3
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 4
        if self.match_BackgroundLine(context, token):
            self.end_rule(context, "FeatureHeader")
            self.start_rule(context, "Background")
            self.build(context, token)
            return 5
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "FeatureHeader")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "FeatureHeader")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "FeatureHeader")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "FeatureHeader")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 4

        state_comment = "State: 3 - GherkinDocument:0>Feature:0>FeatureHeader:2>#FeatureLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#BackgroundLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 3

    # GherkinDocument:0>Feature:0>FeatureHeader:3>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_4(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "FeatureHeader")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Comment(context, token):
            self.build(context, token)
            return 4
        if self.match_BackgroundLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "FeatureHeader")
            self.start_rule(context, "Background")
            self.build(context, token)
            return 5
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "FeatureHeader")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "FeatureHeader")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "FeatureHeader")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "FeatureHeader")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.build(context, token)
            return 4

        state_comment = "State: 4 - GherkinDocument:0>Feature:0>FeatureHeader:3>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#BackgroundLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 4

    # GherkinDocument:0>Feature:1>Background:0>#BackgroundLine:0
    def match_token_at_5(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Background")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Empty(context, token):
            self.build(context, token)
            return 5
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 6
        if self.match_StepLine(context, token):
            self.start_rule(context, "Step")
            self.build(context, token)
            return 7
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 6

        state_comment = "State: 5 - GherkinDocument:0>Feature:1>Background:0>#BackgroundLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 5

    # GherkinDocument:0>Feature:1>Background:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_6(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Background")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Comment(context, token):
            self.build(context, token)
            return 6
        if self.match_StepLine(context, token):
            self.end_rule(context, "Description")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 7
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.build(context, token)
            return 6

        state_comment = "State: 6 - GherkinDocument:0>Feature:1>Background:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 6

    # GherkinDocument:0>Feature:1>Background:2>Step:0>#StepLine:0
    def match_token_at_7(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.start_rule(context, "DataTable")
            self.build(context, token)
            return 8
        if self.match_DocStringSeparator(context, token):
            self.start_rule(context, "DocString")
            self.build(context, token)
            return 41
        if self.match_StepLine(context, token):
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 7
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Step")
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 7
        if self.match_Empty(context, token):
            self.build(context, token)
            return 7

        state_comment = "State: 7 - GherkinDocument:0>Feature:1>Background:2>Step:0>#StepLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#DocStringSeparator",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 7

    # GherkinDocument:0>Feature:1>Background:2>Step:1>StepArg:0>__alt0:0>DataTable:0>#TableRow:0
    def match_token_at_8(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.build(context, token)
            return 8
        if self.match_StepLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 7
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "DataTable")
                self.end_rule(context, "Step")
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 8
        if self.match_Empty(context, token):
            self.build(context, token)
            return 8

        state_comment = "State: 8 - GherkinDocument:0>Feature:1>Background:2>Step:1>StepArg:0>__alt0:0>DataTable:0>#TableRow:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 8

    # GherkinDocument:0>Feature:2>ScenarioDefinition:0>Tags:0>#TagLine:0
    def match_token_at_9(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.build(context, token)
            return 9
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Tags")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_Comment(context, token):
            self.build(context, token)
            return 9
        if self.match_Empty(context, token):
            self.build(context, token)
            return 9

        state_comment = "State: 9 - GherkinDocument:0>Feature:2>ScenarioDefinition:0>Tags:0>#TagLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#ScenarioLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 9

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:0>#ScenarioLine:0
    def match_token_at_10(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Empty(context, token):
            self.build(context, token)
            return 10
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 11
        if self.match_StepLine(context, token):
            self.start_rule(context, "Step")
            self.build(context, token)
            return 12
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 14
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 15
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 11

        state_comment = "State: 10 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:0>#ScenarioLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 10

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_11(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Comment(context, token):
            self.build(context, token)
            return 11
        if self.match_StepLine(context, token):
            self.end_rule(context, "Description")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 12
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "Description")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 14
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Description")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 15
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.build(context, token)
            return 11

        state_comment = "State: 11 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 11

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:2>Step:0>#StepLine:0
    def match_token_at_12(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.start_rule(context, "DataTable")
            self.build(context, token)
            return 13
        if self.match_DocStringSeparator(context, token):
            self.start_rule(context, "DocString")
            self.build(context, token)
            return 39
        if self.match_StepLine(context, token):
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 12
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "Step")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 14
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Step")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Step")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 15
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 12
        if self.match_Empty(context, token):
            self.build(context, token)
            return 12

        state_comment = "State: 12 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:2>Step:0>#StepLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#DocStringSeparator",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 12

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:0>DataTable:0>#TableRow:0
    def match_token_at_13(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.build(context, token)
            return 13
        if self.match_StepLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 12
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "DataTable")
                self.end_rule(context, "Step")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 14
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "DataTable")
                self.end_rule(context, "Step")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 15
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 13
        if self.match_Empty(context, token):
            self.build(context, token)
            return 13

        state_comment = "State: 13 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:0>DataTable:0>#TableRow:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 13

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:0>Tags:0>#TagLine:0
    def match_token_at_14(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.build(context, token)
            return 14
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Tags")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 15
        if self.match_Comment(context, token):
            self.build(context, token)
            return 14
        if self.match_Empty(context, token):
            self.build(context, token)
            return 14

        state_comment = "State: 14 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:0>Tags:0>#TagLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#ExamplesLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 14

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:0>#ExamplesLine:0
    def match_token_at_15(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Empty(context, token):
            self.build(context, token)
            return 15
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 16
        if self.match_TableRow(context, token):
            self.start_rule(context, "ExamplesTable")
            self.build(context, token)
            return 17
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 14
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 15
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 16

        state_comment = "State: 15 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:0>#ExamplesLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#TableRow",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 15

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_16(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Comment(context, token):
            self.build(context, token)
            return 16
        if self.match_TableRow(context, token):
            self.end_rule(context, "Description")
            self.start_rule(context, "ExamplesTable")
            self.build(context, token)
            return 17
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 14
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 15
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.build(context, token)
            return 16

        state_comment = "State: 16 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#TableRow",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 16

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:2>ExamplesTable:0>#TableRow:0
    def match_token_at_17(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.build(context, token)
            return 17
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "ExamplesTable")
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 14
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "ExamplesTable")
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 15
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 17
        if self.match_Empty(context, token):
            self.build(context, token)
            return 17

        state_comment = "State: 17 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:2>ExamplesTable:0>#TableRow:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 17

    # GherkinDocument:0>Feature:3>Rule:0>RuleHeader:0>Tags:0>#TagLine:0
    def match_token_at_18(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.build(context, token)
            return 18
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Tags")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 18
        if self.match_Empty(context, token):
            self.build(context, token)
            return 18

        state_comment = "State: 18 - GherkinDocument:0>Feature:3>Rule:0>RuleHeader:0>Tags:0>#TagLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 18

    # GherkinDocument:0>Feature:3>Rule:0>RuleHeader:1>#RuleLine:0
    def match_token_at_19(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "RuleHeader")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Empty(context, token):
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 20
        if self.match_BackgroundLine(context, token):
            self.end_rule(context, "RuleHeader")
            self.start_rule(context, "Background")
            self.build(context, token)
            return 21
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "RuleHeader")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "RuleHeader")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "RuleHeader")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "RuleHeader")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 20

        state_comment = "State: 19 - GherkinDocument:0>Feature:3>Rule:0>RuleHeader:1>#RuleLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#BackgroundLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 19

    # GherkinDocument:0>Feature:3>Rule:0>RuleHeader:2>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_20(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "RuleHeader")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Comment(context, token):
            self.build(context, token)
            return 20
        if self.match_BackgroundLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "RuleHeader")
            self.start_rule(context, "Background")
            self.build(context, token)
            return 21
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "RuleHeader")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "RuleHeader")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "RuleHeader")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "RuleHeader")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.build(context, token)
            return 20

        state_comment = "State: 20 - GherkinDocument:0>Feature:3>Rule:0>RuleHeader:2>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#BackgroundLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 20

    # GherkinDocument:0>Feature:3>Rule:1>Background:0>#BackgroundLine:0
    def match_token_at_21(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Empty(context, token):
            self.build(context, token)
            return 21
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 22
        if self.match_StepLine(context, token):
            self.start_rule(context, "Step")
            self.build(context, token)
            return 23
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 22

        state_comment = "State: 21 - GherkinDocument:0>Feature:3>Rule:1>Background:0>#BackgroundLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 21

    # GherkinDocument:0>Feature:3>Rule:1>Background:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_22(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Comment(context, token):
            self.build(context, token)
            return 22
        if self.match_StepLine(context, token):
            self.end_rule(context, "Description")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 23
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.build(context, token)
            return 22

        state_comment = "State: 22 - GherkinDocument:0>Feature:3>Rule:1>Background:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 22

    # GherkinDocument:0>Feature:3>Rule:1>Background:2>Step:0>#StepLine:0
    def match_token_at_23(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.start_rule(context, "DataTable")
            self.build(context, token)
            return 24
        if self.match_DocStringSeparator(context, token):
            self.start_rule(context, "DocString")
            self.build(context, token)
            return 37
        if self.match_StepLine(context, token):
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 23
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Step")
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 23
        if self.match_Empty(context, token):
            self.build(context, token)
            return 23

        state_comment = "State: 23 - GherkinDocument:0>Feature:3>Rule:1>Background:2>Step:0>#StepLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#DocStringSeparator",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 23

    # GherkinDocument:0>Feature:3>Rule:1>Background:2>Step:1>StepArg:0>__alt0:0>DataTable:0>#TableRow:0
    def match_token_at_24(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.build(context, token)
            return 24
        if self.match_StepLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 23
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "DataTable")
                self.end_rule(context, "Step")
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 24
        if self.match_Empty(context, token):
            self.build(context, token)
            return 24

        state_comment = "State: 24 - GherkinDocument:0>Feature:3>Rule:1>Background:2>Step:1>StepArg:0>__alt0:0>DataTable:0>#TableRow:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 24

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:0>Tags:0>#TagLine:0
    def match_token_at_25(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.build(context, token)
            return 25
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Tags")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_Comment(context, token):
            self.build(context, token)
            return 25
        if self.match_Empty(context, token):
            self.build(context, token)
            return 25

        state_comment = "State: 25 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:0>Tags:0>#TagLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#ScenarioLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 25

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:0>#ScenarioLine:0
    def match_token_at_26(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Empty(context, token):
            self.build(context, token)
            return 26
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 27
        if self.match_StepLine(context, token):
            self.start_rule(context, "Step")
            self.build(context, token)
            return 28
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 30
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 31
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 27

        state_comment = "State: 26 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:0>#ScenarioLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 26

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_27(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Comment(context, token):
            self.build(context, token)
            return 27
        if self.match_StepLine(context, token):
            self.end_rule(context, "Description")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 28
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "Description")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 30
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Description")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 31
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.build(context, token)
            return 27

        state_comment = "State: 27 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 27

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:2>Step:0>#StepLine:0
    def match_token_at_28(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.start_rule(context, "DataTable")
            self.build(context, token)
            return 29
        if self.match_DocStringSeparator(context, token):
            self.start_rule(context, "DocString")
            self.build(context, token)
            return 35
        if self.match_StepLine(context, token):
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 28
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "Step")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 30
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Step")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Step")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 31
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 28
        if self.match_Empty(context, token):
            self.build(context, token)
            return 28

        state_comment = "State: 28 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:2>Step:0>#StepLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#DocStringSeparator",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 28

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:0>DataTable:0>#TableRow:0
    def match_token_at_29(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.build(context, token)
            return 29
        if self.match_StepLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 28
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "DataTable")
                self.end_rule(context, "Step")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 30
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "DataTable")
                self.end_rule(context, "Step")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 31
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "DataTable")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 29
        if self.match_Empty(context, token):
            self.build(context, token)
            return 29

        state_comment = "State: 29 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:0>DataTable:0>#TableRow:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 29

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:0>Tags:0>#TagLine:0
    def match_token_at_30(self, token: Token, context: ParserContext) -> int:
        if self.match_TagLine(context, token):
            self.build(context, token)
            return 30
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Tags")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 31
        if self.match_Comment(context, token):
            self.build(context, token)
            return 30
        if self.match_Empty(context, token):
            self.build(context, token)
            return 30

        state_comment = "State: 30 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:0>Tags:0>#TagLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#TagLine",
            "#ExamplesLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 30

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:0>#ExamplesLine:0
    def match_token_at_31(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Empty(context, token):
            self.build(context, token)
            return 31
        if self.match_Comment(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 32
        if self.match_TableRow(context, token):
            self.start_rule(context, "ExamplesTable")
            self.build(context, token)
            return 33
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 30
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 31
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.start_rule(context, "Description")
            self.build(context, token)
            return 32

        state_comment = "State: 31 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:0>#ExamplesLine:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Empty",
            "#Comment",
            "#TableRow",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 31

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0
    def match_token_at_32(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_Comment(context, token):
            self.build(context, token)
            return 32
        if self.match_TableRow(context, token):
            self.end_rule(context, "Description")
            self.start_rule(context, "ExamplesTable")
            self.build(context, token)
            return 33
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 30
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "Description")
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 31
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "Description")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Other(context, token):
            self.build(context, token)
            return 32

        state_comment = "State: 32 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:1>DescriptionHelper:1>Description:0>__alt1:0>#Other:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#Comment",
            "#TableRow",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 32

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:2>ExamplesTable:0>#TableRow:0
    def match_token_at_33(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_TableRow(context, token):
            self.build(context, token)
            return 33
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "ExamplesTable")
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 30
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "ExamplesTable")
                self.end_rule(context, "Examples")
                self.end_rule(context, "ExamplesDefinition")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 31
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "ExamplesTable")
            self.end_rule(context, "Examples")
            self.end_rule(context, "ExamplesDefinition")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 33
        if self.match_Empty(context, token):
            self.build(context, token)
            return 33

        state_comment = "State: 33 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:3>ExamplesDefinition:1>Examples:2>ExamplesTable:0>#TableRow:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#TableRow",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 33

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0
    def match_token_at_35(self, token: Token, context: ParserContext) -> int:
        if self.match_DocStringSeparator(context, token):
            self.build(context, token)
            return 36
        if self.match_Other(context, token):
            self.build(context, token)
            return 35

        state_comment = "State: 35 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#DocStringSeparator",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 35

    # GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0
    def match_token_at_36(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_StepLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 28
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "DocString")
                self.end_rule(context, "Step")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 30
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "DocString")
                self.end_rule(context, "Step")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 31
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 36
        if self.match_Empty(context, token):
            self.build(context, token)
            return 36

        state_comment = "State: 36 - GherkinDocument:0>Feature:3>Rule:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 36

    # GherkinDocument:0>Feature:3>Rule:1>Background:2>Step:1>StepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0
    def match_token_at_37(self, token: Token, context: ParserContext) -> int:
        if self.match_DocStringSeparator(context, token):
            self.build(context, token)
            return 38
        if self.match_Other(context, token):
            self.build(context, token)
            return 37

        state_comment = "State: 37 - GherkinDocument:0>Feature:3>Rule:1>Background:2>Step:1>StepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#DocStringSeparator",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 37

    # GherkinDocument:0>Feature:3>Rule:1>Background:2>Step:1>StepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0
    def match_token_at_38(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_StepLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 23
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "DocString")
                self.end_rule(context, "Step")
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 25
        if self.match_TagLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 26
        if self.match_RuleLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Rule")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 38
        if self.match_Empty(context, token):
            self.build(context, token)
            return 38

        state_comment = "State: 38 - GherkinDocument:0>Feature:3>Rule:1>Background:2>Step:1>StepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 38

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0
    def match_token_at_39(self, token: Token, context: ParserContext) -> int:
        if self.match_DocStringSeparator(context, token):
            self.build(context, token)
            return 40
        if self.match_Other(context, token):
            self.build(context, token)
            return 39

        state_comment = "State: 39 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#DocStringSeparator",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 39

    # GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0
    def match_token_at_40(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_StepLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 12
        if self.match_TagLine(context, token):
            if self.lookahead_1(context, token):
                self.end_rule(context, "DocString")
                self.end_rule(context, "Step")
                self.start_rule(context, "ExamplesDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 14
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "DocString")
                self.end_rule(context, "Step")
                self.end_rule(context, "Scenario")
                self.end_rule(context, "ScenarioDefinition")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ExamplesLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.start_rule(context, "ExamplesDefinition")
            self.start_rule(context, "Examples")
            self.build(context, token)
            return 15
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Scenario")
            self.end_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 40
        if self.match_Empty(context, token):
            self.build(context, token)
            return 40

        state_comment = "State: 40 - GherkinDocument:0>Feature:2>ScenarioDefinition:1>Scenario:2>Step:1>StepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#StepLine",
            "#TagLine",
            "#ExamplesLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 40

    # GherkinDocument:0>Feature:1>Background:2>Step:1>StepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0
    def match_token_at_41(self, token: Token, context: ParserContext) -> int:
        if self.match_DocStringSeparator(context, token):
            self.build(context, token)
            return 42
        if self.match_Other(context, token):
            self.build(context, token)
            return 41

        state_comment = "State: 41 - GherkinDocument:0>Feature:1>Background:2>Step:1>StepArg:0>__alt0:1>DocString:0>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#DocStringSeparator",
            "#Other",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 41

    # GherkinDocument:0>Feature:1>Background:2>Step:1>StepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0
    def match_token_at_42(self, token: Token, context: ParserContext) -> int:
        if self.match_EOF(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.end_rule(context, "Feature")
            self.build(context, token)
            return 34
        if self.match_StepLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.start_rule(context, "Step")
            self.build(context, token)
            return 7
        if self.match_TagLine(context, token):
            if self.lookahead_0(context, token):
                self.end_rule(context, "DocString")
                self.end_rule(context, "Step")
                self.end_rule(context, "Background")
                self.start_rule(context, "ScenarioDefinition")
                self.start_rule(context, "Tags")
                self.build(context, token)
                return 9
        if self.match_TagLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.start_rule(context, "Tags")
            self.build(context, token)
            return 18
        if self.match_ScenarioLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "ScenarioDefinition")
            self.start_rule(context, "Scenario")
            self.build(context, token)
            return 10
        if self.match_RuleLine(context, token):
            self.end_rule(context, "DocString")
            self.end_rule(context, "Step")
            self.end_rule(context, "Background")
            self.start_rule(context, "Rule")
            self.start_rule(context, "RuleHeader")
            self.build(context, token)
            return 19
        if self.match_Comment(context, token):
            self.build(context, token)
            return 42
        if self.match_Empty(context, token):
            self.build(context, token)
            return 42

        state_comment = "State: 42 - GherkinDocument:0>Feature:1>Background:2>Step:1>StepArg:0>__alt0:1>DocString:2>#DocStringSeparator:0"  # fmt: skip
        token.detach()
        expected_tokens = [
            "#EOF",
            "#StepLine",
            "#TagLine",
            "#ScenarioLine",
            "#RuleLine",
            "#Comment",
            "#Empty",
        ]
        error = (
            UnexpectedEOFException(token, expected_tokens, state_comment)
            if token.eof()
            else UnexpectedTokenException(token, expected_tokens, state_comment)
        )
        if self.stop_at_first_error:
            raise error
        self.add_error(context, error)
        return 42

    def lookahead_0(self, context: ParserContext, currentToken: Token) -> bool:
        currentToken.detach()
        token = None
        queue = []
        match = False
        # Effectively do-while
        continue_lookahead = True
        while continue_lookahead:
            token = self.read_token(context)
            token.detach()
            queue.append(token)

            if self.match_ScenarioLine(context, token):
                match = True
                break

            continue_lookahead = False

            if self.match_Empty(context, token):
                continue_lookahead = True
                continue
            if self.match_Comment(context, token):
                continue_lookahead = True
                continue
            if self.match_TagLine(context, token):
                continue_lookahead = True
                continue

        context.token_queue.extend(queue)

        return match

    def lookahead_1(self, context: ParserContext, currentToken: Token) -> bool:
        currentToken.detach()
        token = None
        queue = []
        match = False
        # Effectively do-while
        continue_lookahead = True
        while continue_lookahead:
            token = self.read_token(context)
            token.detach()
            queue.append(token)

            if self.match_ExamplesLine(context, token):
                match = True
                break

            continue_lookahead = False

            if self.match_Empty(context, token):
                continue_lookahead = True
                continue
            if self.match_Comment(context, token):
                continue_lookahead = True
                continue
            if self.match_TagLine(context, token):
                continue_lookahead = True
                continue

        context.token_queue.extend(queue)

        return match

    # private

    def handle_ast_error(
        self,
        context: ParserContext,
        argument: _T,
        action: Callable[[_T], object],
    ) -> None:
        self.handle_external_error(context, True, argument, action)

    def handle_external_error(
        self,
        context: ParserContext,
        default_value: _U,
        argument: _T,
        action: Callable[[_T], _V],
    ) -> _V | _U:
        if self.stop_at_first_error:
            return action(argument)

        try:
            return action(argument)
        except CompositeParserException as e:
            for error in e.errors:
                self.add_error(context, error)
        except ParserException as e:
            self.add_error(context, e)
        return default_value
