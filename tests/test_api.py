from fox.api.form_types import CodedOptions


def test_option_decode():
    data = {
        0: "校級",
        1: "醫學院",
        2: "牙醫學院",
    }
    result = [
        CodedOptions(code="0", value="校級"),
        CodedOptions(code="1", value="醫學院"),
        CodedOptions(code="2", value="牙醫學院"),
    ]
    assert CodedOptions.from_coded_dict(data) == result
