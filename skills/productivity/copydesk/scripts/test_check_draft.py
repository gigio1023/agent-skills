"""Unit tests for check_draft.py: each category must trigger on a positive example
and stay silent on a nearby negative, so the tool doesn't cry wolf on legitimate text."""

from __future__ import annotations

import unittest

from check_draft import analyze


def categories(text: str, max_cell: int = 60) -> set[str]:
    return {f.category for f in analyze(text, max_cell)}


class TestSelfDescription(unittest.TestCase):
    def test_positive(self) -> None:
        text = "# T\n\n이 문서는 시스템 구조를 설명한다.\n"
        self.assertIn("self_description", categories(text))

    def test_negative_subject_is_the_system(self) -> None:
        text = "# T\n\n시스템은 세 개의 계층으로 구성된다.\n"
        self.assertNotIn("self_description", categories(text))


class TestStatusPlan(unittest.TestCase):
    def test_positive(self) -> None:
        text = "# T\n\n이 지표는 아직 검증하지 않았다.\n"
        self.assertIn("status_plan", categories(text))

    def test_negative(self) -> None:
        text = "# T\n\n이 지표는 지난 분기에 검증을 완료했다.\n"
        self.assertNotIn("status_plan", categories(text))


class TestOrderNarration(unittest.TestCase):
    def test_positive(self) -> None:
        text = "# T\n\n최신 항목부터 나열한 목록이다.\n"
        self.assertIn("order_narration", categories(text))

    def test_negative(self) -> None:
        text = "# T\n\n이 목록은 팀별로 묶어서 정리했다.\n"
        self.assertNotIn("order_narration", categories(text))


class TestNegationDefinition(unittest.TestCase):
    def test_positive(self) -> None:
        text = "# T\n\n이것은 버그가 아니라 의도된 동작이다.\n"
        self.assertIn("negation_definition", categories(text))

    def test_negative_real_limit_is_not_flagged(self) -> None:
        # "대신하지 못한다" states an actual limitation, not a negated identity claim.
        text = "# T\n\n이 도구는 사람의 최종 판단을 대신하지 못한다.\n"
        self.assertNotIn("negation_definition", categories(text))


class TestLongCell(unittest.TestCase):
    def test_positive_over_max(self) -> None:
        long_cell = "이" * 65
        text = f"# T\n\n| 이름 | 설명 |\n| --- | --- |\n| foo | {long_cell} |\n"
        self.assertIn("long_cell", categories(text))

    def test_positive_hides_second_sentence(self) -> None:
        text = "# T\n\n| 이름 | 설명 |\n| --- | --- |\n| foo | 첫 문장이다. 두 번째 문장도 있다 |\n"
        self.assertIn("long_cell", categories(text))

    def test_negative_short_cell(self) -> None:
        short_cell = "이" * 40
        text = f"# T\n\n| 이름 | 설명 |\n| --- | --- |\n| foo | {short_cell} |\n"
        self.assertNotIn("long_cell", categories(text))

    def test_negative_caption_line_is_not_prose(self) -> None:
        # A figure caption ("그림 1. ...") must not be counted as an over-long prose paragraph.
        text = "# T\n\n그림 1. 시스템 구조와 각 계층의 역할, 배포 경계, 데이터 흐름까지 모두 담은 도식이다. 두 번째 설명. 세 번째 설명.\n"
        self.assertNotIn("first_screen_prose", categories(text))


class TestFirstScreenProse(unittest.TestCase):
    def test_positive(self) -> None:
        text = (
            "# T\n\n"
            "첫 문장이 여기 있다. 두 번째 문장도 이어진다. 세 번째 문장까지 붙는다.\n"
        )
        self.assertIn("first_screen_prose", categories(text))

    def test_negative_two_sentences_ok(self) -> None:
        text = "# T\n\n첫 문장이 여기 있다. 두 번째 문장도 이어진다.\n"
        self.assertNotIn("first_screen_prose", categories(text))

    def test_negative_list_item_not_counted_as_prose(self) -> None:
        text = "# T\n\n- 첫 항목이다. 두 번째 문장도 있다. 세 번째 문장도 있다.\n"
        self.assertNotIn("first_screen_prose", categories(text))


class TestScopeExclusions(unittest.TestCase):
    def test_code_fence_is_out_of_scope(self) -> None:
        text = "# T\n\n```\n이 문서는 코드 안 텍스트다.\n```\n"
        self.assertNotIn("self_description", categories(text))

    def test_blockquote_is_out_of_scope(self) -> None:
        text = "# T\n\n> 이 문서는 인용문 안 텍스트다.\n"
        self.assertNotIn("self_description", categories(text))


class TestJsonAndExitCode(unittest.TestCase):
    def test_json_mode_returns_list(self) -> None:
        import io
        import json as json_module
        from contextlib import redirect_stdout

        import check_draft

        with open("/tmp/_cd_test.md", "w", encoding="utf-8") as f:
            f.write("# T\n\n이 문서는 설명한다.\n")
        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = check_draft.main(["/tmp/_cd_test.md", "--json"])
        self.assertEqual(exit_code, 0)
        parsed = json_module.loads(buf.getvalue())
        self.assertIsInstance(parsed, list)


if __name__ == "__main__":
    unittest.main()
