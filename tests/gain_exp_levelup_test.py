from base_workings.player import Player


def test_just_a_little() -> None:
    """Test that the player will actually gain exp"""
    p = Player(0, 0, [], 1, 1)
    p.gain_exp(1)
    assert p.exp == 1


def test_boundary_lower() -> None:
    """Test that the player will not break if exp is 0"""
    p = Player(0, 0, [], 1, 1)
    p.gain_exp(0)
    assert p.exp == 0


def test_unexpected() -> None:
    """Test that the player will not break if exp is unexpected value"""
    p = Player(0, 0, [], 1, 1)
    p.gain_exp(-1)
    assert p.exp == 0


def test_boundary_upper() -> None:
    """Test that the player will not break if exp is exactly on upper bound"""
    p = Player(0, 0, [], 1, 1)
    p.gain_exp(4)
    assert p.exp == 4


def test_level_up_lower_bound() -> None:
    """Test that the player will level up, and health regend"""
    p = Player(0, 0, [], 1, 1)
    p.health = 40
    p.gain_exp(5)
    assert p.exp == 0
    assert p.stamina == 110
    assert p.max_stamina == 110
    assert p.level == 2


def test_level_up_upper_bound() -> None:
    """Test that the player will only levelup once"""
    p = Player(0, 0, [], 1, 1)
    p.gain_exp(14)
    assert p.level == 2
    assert p.exp == 9


def test_level_up_multiple_times() -> None:
    """Test that the player will keep leveling up as long as it has exp"""
    level_to_get = 7
    p = Player(0, 0, [], 1, 1)
    p.gain_exp(sum(i * 5 for i in range(level_to_get)))
    assert p.level == level_to_get
    assert p.exp == 0
    assert p.max_stamina == 100 + level_to_get * 10 - 10
    assert p.max_stamina == p.stamina


def test_level_up_a_bit_at_a_time() -> None:
    """Test that player will level up if exp is added a bit at a time"""
    p = Player(0, 0, [], 1, 1)
    for _ in range(4):
        p.gain_exp(1)
        assert p.level == 1
    p.gain_exp(2)
    assert p.level == 2
    assert p.exp == 1
    p.gain_exp(5)
    p.gain_exp(7)
    assert p.level == 3
    p.gain_exp(2)
    assert p.level == 3
    assert p.exp == 5
