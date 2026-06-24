import pytest

from src.tools.save_tool import SaveTool


@pytest.fixture
def tool():
    return SaveTool()


def test_creates_outputs_directory(tool, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    tool._run(content="# Test Report\n\nSome content.", topic="test topic")

    assert (tmp_path / "outputs").is_dir()


def test_saves_markdown_file(tool, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    tool._run(content="# Test Report", topic="test topic")

    files = list((tmp_path / "outputs").glob("*.md"))
    assert len(files) == 1


def test_file_contains_exact_content(tool, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    content = "# My Report\n\nKey findings here."

    tool._run(content=content, topic="my topic")

    files = list((tmp_path / "outputs").glob("*.md"))
    assert files[0].read_text(encoding="utf-8") == content


def test_filename_slugifies_topic(tool, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    tool._run(content="# Report", topic="AI & Machine Learning!")

    files = list((tmp_path / "outputs").glob("*.md"))
    filename = files[0].name
    assert "ai" in filename
    assert "machine" in filename
    assert "&" not in filename
    assert "!" not in filename


def test_returns_filepath_in_confirmation(tool, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = tool._run(content="# Report", topic="climate change")

    assert "outputs" in result
    assert "climate-change" in result


def test_multiple_saves_produce_separate_files(tool, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    tool._run(content="# Report 1", topic="python")
    tool._run(content="# Report 2", topic="python")

    files = list((tmp_path / "outputs").glob("*.md"))
    assert len(files) == 2
