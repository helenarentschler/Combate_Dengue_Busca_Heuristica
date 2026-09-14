import unittest
from a_star import encontrar_caminho


class TestAEstrela(unittest.TestCase):
    def test_prefere_grama(self):
        mapa = [list("GGGGG"), list("GMMMG"), list("GGGGG")]
        caminho, custo = encontrar_caminho(mapa, (0, 1), (4, 1))
        self.assertEqual(custo, 6)
        self.assertTrue(all(mapa[y][x] == "G" for x, y in caminho))

    def test_usa_lama_se_precisar(self):
        mapa = [list("G#G"), list("GMG"), list("G#G")]
        caminho, custo = encontrar_caminho(mapa, (0, 0), (2, 0))
        self.assertEqual(custo, 6)
        self.assertIn((1, 1), caminho)

    def test_sem_caminho(self):
        mapa = [list("G#G"), list("G#G")]
        self.assertEqual(encontrar_caminho(mapa, (0, 0), (2, 0)), (None, None))


if __name__ == "__main__":
    unittest.main()
