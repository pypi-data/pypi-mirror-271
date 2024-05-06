from augmolino import utils

def test_quickPlotSpectrogram():

    test_file = "tests/sounds/impulse_response.wav"

    utils.quickPlotSpectrogram(test_file)