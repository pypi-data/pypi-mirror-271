import os
import librosa as lr
import augmolino.augmentation as aug
import numpy as np
import numpy.testing as npt

test_file = "tests/sounds/impulse_response.wav"
target_path = "tests/sounds/mysound.wav"


def test_augmentation_init():

    a = aug._augmentation()

    assert a.sample_rate == 22050
    assert a.descriptor == aug.descriptors["_augmentation"]
    assert a.function == None
    assert len(a.kwargs) == 0
    assert a.tag == ""


def test_augmentation_load():

    a = aug._augmentation()
    a._load(test_file)

    assert a.f_source == test_file

    t, _ = lr.load(path=test_file)

    assert len(a.signal) == len(t)


def test_augmentation_autoName():
    a = aug._augmentation()
    a._load(test_file)

    assert a.tag == ""

    name = a._autoName(a.descriptor, a.tag)

    assert name == test_file[:-4] + f"_{a.descriptor}_{a.tag}.wav"


def test_timeStretch_class():

    test_rate = 0.5
    a = aug.timeStretch(rate=test_rate)

    assert a.descriptor == aug.descriptors[aug.__all__[0]]
    assert a.function == lr.effects.time_stretch
    assert len(a.kwargs) == 1
    assert a.tag == "0_5"

    x = a.run(test_file)

    assert a.f_dest == None
    assert len(x) == int(len(a.signal) / test_rate)
    npt.assert_allclose(x, lr.effects.time_stretch(a.signal, rate=test_rate))

    x = a.run(test_file, target_path)

    assert x == None
    assert a.f_dest == target_path
    assert os.path.exists(target_path)

    os.remove(target_path)

    x = a.run(test_file, f_dest="auto")
    assert a.f_dest == test_file[:-4] + f"_{a.descriptor}_{a.tag}.wav"
    assert os.path.exists(a.f_dest)

    os.remove(a.f_dest)
    

def test_pitchShift_class():

    test_semitones = 2
    a = aug.pitchShift(semitones=test_semitones)

    assert a.descriptor == aug.descriptors[aug.__all__[1]]
    assert a.function == lr.effects.pitch_shift
    assert len(a.kwargs) == 2
    assert a.tag == "22050_2"

    x = a.run(test_file)

    assert len(x) == len(a.signal)
    npt.assert_allclose(x, lr.effects.pitch_shift(a.signal, 
                                                   sr=a.sample_rate,
                                                   n_steps=test_semitones))

    x = a.run(test_file, f_dest="auto")
    assert a.f_dest == test_file[:-4] + f"_{a.descriptor}_{a.tag}.wav"
    assert os.path.exists(a.f_dest)

    os.remove(a.f_dest)


def test_offsetAudio_class():

    test_s = 1
    a = aug.offsetAudio(s=test_s)

    assert a.descriptor == aug.descriptors[aug.__all__[2]]
    assert a.function == a._offset
    assert len(a.kwargs) == 1
    assert a.tag == "1"

    x = a.run(test_file)

    assert len(x) == len(a.signal) + test_s * a.sample_rate
    npt.assert_allclose(x[0:test_s * a.sample_rate],
                        np.zeros(test_s * a.sample_rate))

    test_s = -1
    a = aug.offsetAudio(s=test_s)

    x = a.run(test_file)
    assert len(x) == len(a.signal) + test_s * a.sample_rate

    x = a.run(test_file, f_dest="auto")
    assert a.f_dest == test_file[:-4] + f"_{a.descriptor}_{a.tag}.wav"
    assert os.path.exists(a.f_dest)

    os.remove(a.f_dest)


def test_fadeAudio_class():

    test_s = 1
    test_direction = "in"
    a = aug.fadeAudio(s=test_s, direction=test_direction)

    assert a.descriptor == aug.descriptors[aug.__all__[3]]
    assert a.function == a._fade
    assert len(a.kwargs) == 2
    assert a.tag == "1_in"

    x = a.run(test_file)


def test_mixAudio_class():
    test_f_mix = "tests/sounds/speech.wav"
    test_ratio = 0.5
    test_start_at = 1
    a = aug.mixAudio(test_ratio, test_start_at)

    assert a.descriptor == aug.descriptors[aug.__all__[4]]
    assert a.function == a._mix
    assert len(a.kwargs) == 2
    assert a.tag == "0_5_1"

    x = a.run(test_file, target_path, f_mix=test_f_mix)
    assert len(a.kwargs) == 3

    a = aug.mixAudio(test_ratio)
    assert a.tag == "0_5_None"
    x = a.run(test_file, target_path, f_mix=test_f_mix)


    os.remove(target_path)