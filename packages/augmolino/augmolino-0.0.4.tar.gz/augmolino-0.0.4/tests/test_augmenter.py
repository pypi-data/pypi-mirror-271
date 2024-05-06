from augmolino import augmenter, augmentation
import os

source_dir = "tests/sounds/"
source_file = "tests/sounds/speech.wav"


def test_empty_augmenter_init():

    a = augmenter.augmenter()
    assert a.pipe == []


def test_filled_augmenter_init():

    augs = [
        augmentation.pitchShift(semitones=1),
        augmentation.pitchShift(semitones=2)]

    a = augmenter.augmenter(augs)

    assert len(a.pipe) == len(augs)

    for aug in a.pipe:
        assert aug.descriptor == "pitch_shift"


def test_augmenter_summary():

    augs = [
        augmentation.pitchShift(semitones=1),
        augmentation.pitchShift(semitones=2)]

    a = augmenter.augmenter(augs)

    a.summary()


def test_augmenter_run_array():

    augs = [
        augmentation.timeStretch(rate=2),
        augmentation.pitchShift(semitones=2),
        augmentation.offsetAudio(s=1)]

    a = augmenter.augmenter(augs)

    xs = a.execute(source_file)

    assert len(xs) == len(augs)


def test_augmenter_run_single_save():

    fnames = ["targetfile1.wav",
              "targetfile2.wav",
              "targetfile3.wav"]

    augs = [
        augmentation.timeStretch(rate=2),
        augmentation.pitchShift(semitones=2),
        augmentation.offsetAudio(s=1)]

    a = augmenter.augmenter(augs)

    for fname in fnames:
        xs = a.execute(source_file, fname)
        assert xs == None

    for fname in fnames:
        assert os.path.exists(fname)
        os.remove(fname)


def test_augmenter_run_multi_save():

    fnames = ["targetfile1.wav",
              "targetfile2.wav",
              "targetfile3.wav"]

    augs = [augmentation.timeStretch(rate=2),
            augmentation.pitchShift(semitones=2),
            augmentation.offsetAudio(s=1)]

    a = augmenter.augmenter(augs)

    for fname in fnames:
        xs = a.execute(source_file, fname)
        assert xs == None

    for fname in fnames:
        assert os.path.exists(fname)
        os.remove(fname)

def test_augmenter_run_folder_auto_save():

    augs = [augmentation.timeStretch(rate=2),
            augmentation.pitchShift(semitones=2),
            augmentation.offsetAudio(s=1)]

    a = augmenter.augmenter(augs)

    xs = a.execute(source_dir, dest="auto")
    assert xs == None

def test_cleanup():
    keep = ["impulse_response.wav",
            "speech.wav"]

    for file in os.listdir(source_dir):
        if file not in keep:
            os.remove(os.path.join(source_dir, file))

# this can only be tested visually by a human
test_augmenter_summary()
