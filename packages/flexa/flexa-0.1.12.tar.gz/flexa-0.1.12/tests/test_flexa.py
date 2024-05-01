import pytest

from flexa import Flexa


def run():
    test_flexa = TestFlexa()
    test_flexa.test_flexa()
    return True


def test_flexa_benchmark(benchmark):
    """ベンチマークを実施するテスト

    :param benchmark: pytest-benchmark がインジェクトするフィクスチャ
    """
    # テスト対象を引数として benchmark を実行する
    ret = benchmark(run)
    # 返り値を検証する
    assert ret


class TestFlexa:
    def test_flexa(self):
        flexa = Flexa()

        flexa.set("a", 1)
        flexa.set("a", 2)
        flexa.set("b", 3)
        flexa.set("b", 5)
        flexa.set("a", 6)

        with pytest.raises(ValueError) as e:
            flexa.set("err", 2)
        assert str(e.value) == "Invalid input value when set pair but input exists"

        result_6 = flexa.result(6)
        result_1 = flexa.result(1)
        result_3 = flexa.result(3)
        result_2 = flexa.result(2)

        assert result_6 == "a"
        assert result_1 == "a"
        assert result_3 == "b"
        assert result_2 == "a"

        with pytest.raises(ValueError) as e:
            flexa.result(4)
        assert str(e.value) == "Invalid input value when output result"
