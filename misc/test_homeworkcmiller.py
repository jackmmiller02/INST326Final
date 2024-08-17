from homeworkcmiller import get_fret, get_frets


def test_get_fret():
    assert get_fret("A", "A") == 0
    assert get_fret("G#", "A") == 11
    assert get_fret("A#", "G#") == 2
    assert get_fret("C#", "B") == get_fret("Db", "B")

test_get_fret()


def test_get_frets():
    frets_result = get_frets("C", ["F"])
    assert len(frets_result) == 1
    assert "F" in frets_result
    assert frets_result["F"] == 7
    frets_result2 = get_frets("C", ["F", "G", "B"])
    assert len(frets_result2) == 3
    assert "F" and "G" and "B" in frets_result2
    assert frets_result2["F"] == 7
    assert frets_result2["G"] == 5
    assert frets_result2["B"] == 1
    



if __name__ == "__main__":
    test_get_frets()
