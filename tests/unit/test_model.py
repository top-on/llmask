"""Testing model module."""

from llmask.model import Model


def test_model_filename():
    """Test filename property of Model class."""
    model = Model(name="name", url="https://test.com/test_file.html")

    filename = model.filename

    assert filename == "test_file.html"
