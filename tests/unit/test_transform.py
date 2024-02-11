"""Test transformation functions."""


from llmask.transform import parse_transformations_string, simplify, thesaurus


def test_parse_transformations_string():
    transformations = "sst"

    transformation_functions = parse_transformations_string(
        transformations=transformations,
    )

    assert simplify in transformation_functions
    assert thesaurus in transformation_functions
