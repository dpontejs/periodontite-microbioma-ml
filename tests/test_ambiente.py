def test_dependencias_importam():
    import gradio  # noqa: F401
    import joblib  # noqa: F401
    import pandas  # noqa: F401
    import scipy  # noqa: F401
    import seaborn  # noqa: F401
    import sklearn

    assert sklearn.__version__
