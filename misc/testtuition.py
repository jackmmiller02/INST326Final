from homeworkbmiller import calculate_tuition

def test_calculate_tuition():
    assert calculate_tuition(0) == 0
    assert calculate_tuition(0, resident=False) == 0
    assert calculate_tuition(0, dt=True) == 0
    assert calculate_tuition(0, resident=False, dt=True) == 0

    assert calculate_tuition(1) == 822
    assert calculate_tuition(1, resident=False) == 1911
    assert calculate_tuition(1, dt=True) == 940
    assert calculate_tuition(1, resident=False, dt=True) == 2029

    assert calculate_tuition(8) == 3391
    assert calculate_tuition(8, resident=False) == 12103
    assert calculate_tuition(8, dt=True) == 4335
    assert calculate_tuition(8, resident=False, dt=True) == 13047

    assert calculate_tuition(9) == 4280.5
    assert calculate_tuition(9, resident=False) == 14081.5
    assert calculate_tuition(9, dt=True) == 5342.5
    assert calculate_tuition(9, resident=False, dt=True) == 15143.5

    assert calculate_tuition(11) == 5014.5
    assert calculate_tuition(11, resident=False) == 16993.5
    assert calculate_tuition(11, dt=True) == 6312.5
    assert calculate_tuition(11, resident=False, dt=True) == 18291.5

    assert calculate_tuition(12) == 5389.5
    assert calculate_tuition(12, resident=False) == 18445.5
    assert calculate_tuition(12, dt=True) == 6817.5
    assert calculate_tuition(12, resident=False, dt=True) == 19873.5


    assert calculate_tuition(15) == 5389.5
    assert calculate_tuition(15, resident=False) == 18445.5
    assert calculate_tuition(15, dt=True) == 6817.5
    assert calculate_tuition(15, resident=False, dt=True) == 19873.5

if __name__ == "__main__":
    test_calculate_tuition()