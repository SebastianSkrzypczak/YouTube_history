from service_layer.data_manipulation import iso8601_to_seconds
from icecream import ic


class Test_iso8601_to_seconds:
    def test_basic_case(self):
        time = "PT1H30M"
        result = iso8601_to_seconds(time)
        assert result == (30.0 * 60 + 60.0 * 60)

    def test_case_without_days(self):
        time = "PT3H45M"
        result = iso8601_to_seconds(time)
        assert result == (45.0 * 60 + 3 * 60 * 60)

    def test_case_with_days(self):
        time = "PT2DT3H45M"
        result = iso8601_to_seconds(time)
        assert result == (45.0 * 60 + 3 * 60 * 60 + 2 * 24 * 60 * 60)

    def test_case_with_only_days(self):
        time = "PT5D"
        result = iso8601_to_seconds(time)
        assert result == (5 * 24 * 60 * 60)

    def test_case_with_only_hours(self):
        time = "PT6H"
        result = iso8601_to_seconds(time)
        assert result == (6 * 60 * 60.0)

    def test_case_with_only_minutes(self):
        time = "PT45M"
             result = iso8601_to_seconds(time)
        assert result == (6 * 60 * 60.0)

    # def test_case_with_only_seconds(self):
    #     time = "PT120S"

    # def test_case_with_all_units(self):
    #     time = "P3DT4H15M30S"

    # def test_case_with_empty_input(self):
    #     time = ""

    # def test_case_with_invalid_format(self):
    #     time = "ABC"

    # def test_case_with_floating_point_values(self):
    #     time = "PT1.5H"

    # def test_case_with_whitespace(self):
    #     time = "  PT2H  "

    # def test_case_with_lowercase_letters(self):
    #     time = "pt2h30m"

    # def test_case_with_negative_values(self):
    #     time = "-PT2H30M"
