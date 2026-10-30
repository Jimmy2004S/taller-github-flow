import logging

logger = logging.getLogger(__name__)

UMBRAL_DESCUENTO_VIP = 1000
DESCUENTO_VIP_ALTO = 0.20
DESCUENTO_VIP_BAJO = 0.10
SIN_DESCUENTO = 0.0
SIN_IMPUESTO = 0.0

IMPUESTOS_POR_PAIS = {
    "CO": 0.19,
    "MX": 0.16,
    "CL": 0.19,
}


def calcular_descuento(monto, es_vip):
    if not es_vip:
        return SIN_DESCUENTO
    if monto > UMBRAL_DESCUENTO_VIP:
        return DESCUENTO_VIP_ALTO
    return DESCUENTO_VIP_BAJO


def calcular_impuesto(pais):
    return IMPUESTOS_POR_PAIS.get(pais, SIN_IMPUESTO)


def calcular_monto_final(monto, pais, es_vip):
    monto_con_descuento = monto * (1 - calcular_descuento(monto, es_vip))
    return monto_con_descuento * (1 + calcular_impuesto(pais))


def procesar_pago_usuario(usuario, tarjeta, monto, pais, es_vip):
    if usuario is None:
        logger.warning("Usuario inexistente")
        return False
    if not usuario['activo']:
        logger.warning("Usuario inactivo")
        return False

    monto_final = calcular_monto_final(monto, pais, es_vip)
    if tarjeta['saldo'] < monto_final:
        logger.warning("Saldo insuficiente")
        return False

    tarjeta['saldo'] -= monto_final
    return True
