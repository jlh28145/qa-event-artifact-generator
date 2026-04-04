from qa_event_artifact_generator.utils import safe_filename


def test_safe_filename_removes_unsafe_characters():
    assert safe_filename("Hello World!") == "Hello_World"
    assert safe_filename("../name") == "name"
