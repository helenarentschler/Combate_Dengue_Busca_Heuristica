import unittest

from greedy import find_path


class TestBuscaGulosa(unittest.TestCase):
    def test_encontra_caminho_direto(self):
        mapa = [list("GGGGG")]
        self.assertEqual(
            find_path((0, 0), (4, 0), mapa),
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
        )

    def test_contorna_obstaculo(self):
        mapa = [list("GGGGG"), list("G###G"), list("GGGGG")]
        caminho = find_path((0, 1), (4, 1), mapa)
        self.assertIsNotNone(caminho)
        self.assertEqual(caminho[0], (0, 1))
        self.assertEqual(caminho[-1], (4, 1))

    def test_sem_caminho(self):
        mapa = [list("G#G"), list("G#G")]
        self.assertIsNone(find_path((0, 0), (2, 0), mapa))


if __name__ == "__main__":
    unittest.main()
