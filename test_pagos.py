import unittest

from pagos import (
    calcular_descuento,
    calcular_impuesto,
    procesar_pago_usuario,
)

USUARIO_ACTIVO = {'activo': True}
USUARIO_INACTIVO = {'activo': False}


class TestCalcularDescuento(unittest.TestCase):

    def test_no_vip_sin_descuento(self):
        self.assertEqual(calcular_descuento(2000, False), 0.0)

    def test_vip_monto_alto_20_por_ciento(self):
        self.assertEqual(calcular_descuento(1500, True), 0.20)

    def test_vip_monto_bajo_10_por_ciento(self):
        self.assertEqual(calcular_descuento(1000, True), 0.10)


class TestCalcularImpuesto(unittest.TestCase):

    def test_impuestos_por_pais(self):
        self.assertEqual(calcular_impuesto("CO"), 0.19)
        self.assertEqual(calcular_impuesto("MX"), 0.16)
        self.assertEqual(calcular_impuesto("CL"), 0.19)

    def test_pais_desconocido_sin_impuesto(self):
        self.assertEqual(calcular_impuesto("US"), 0.0)


class TestProcesarPagoUsuario(unittest.TestCase):

    def test_usuario_inexistente(self):
        tarjeta = {'saldo': 500}
        self.assertFalse(
            procesar_pago_usuario(None, tarjeta, 100, "CO", False)
        )
        self.assertEqual(tarjeta['saldo'], 500)

    def test_usuario_inactivo(self):
        tarjeta = {'saldo': 500}
        self.assertFalse(
            procesar_pago_usuario(USUARIO_INACTIVO, tarjeta, 100, "CO", False)
        )
        self.assertEqual(tarjeta['saldo'], 500)

    def test_saldo_insuficiente_por_impuesto(self):
        # Antes del refactor este caso dejaba el saldo en -19
        tarjeta = {'saldo': 100}
        self.assertFalse(
            procesar_pago_usuario(USUARIO_ACTIVO, tarjeta, 100, "CO", False)
        )
        self.assertEqual(tarjeta['saldo'], 100)

    def test_pago_no_vip_con_impuesto(self):
        tarjeta = {'saldo': 500}
        self.assertTrue(
            procesar_pago_usuario(USUARIO_ACTIVO, tarjeta, 100, "MX", False)
        )
        self.assertAlmostEqual(tarjeta['saldo'], 384.0)

    def test_pago_vip_monto_alto(self):
        tarjeta = {'saldo': 5000}
        self.assertTrue(
            procesar_pago_usuario(USUARIO_ACTIVO, tarjeta, 2000, "CL", True)
        )
        self.assertAlmostEqual(tarjeta['saldo'], 3096.0)

    def test_pago_vip_monto_bajo_pais_sin_impuesto(self):
        tarjeta = {'saldo': 1000}
        self.assertTrue(
            procesar_pago_usuario(USUARIO_ACTIVO, tarjeta, 500, "US", True)
        )
        self.assertAlmostEqual(tarjeta['saldo'], 550.0)


if __name__ == '__main__':
    unittest.main()
