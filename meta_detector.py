import hashlib
from bleak.backends.scanner import AdvertisementData
from bleak.backends.device import BLEDevice

TX_POWER_1M = -59.0  # RSSI moyen attendu à 1 mètre
PATH_LOSS_EXPONENT = 2.5  # Facteur d'atténuation en intérieur

def calculate_distance(rssi: int) -> float:
    """Estime la distance en mètres via la formule log-distance path loss."""
    if rssi == 0:
        return -1.0
    ratio = (TX_POWER_1M - rssi) / (10 * PATH_LOSS_EXPONENT)
    return round(pow(10, ratio), 2)

def get_virtual_angle(mac_address: str) -> float:
    """Génère un angle virtuel constant (0-360°) basé sur l'adresse MAC."""
    digest = hashlib.md5(mac_address.encode()).hexdigest()
    return int(digest, 16) % 360

def analyze_device(device: BLEDevice, adv: AdvertisementData) -> dict | None:
    """
    Simule le classifieur de ton collègue.
    Retourne les détails si l'appareil est identifié comme lunettes Meta, sinon None.
    """
    dev_name = (device.name or adv.local_name or "").lower()
    
    # Critères de détection réels ou simulés (à remplacer par la logique finale)
    is_meta = any(k in dev_name for k in ["meta", "ray-ban", "stories", "hypernova"])
    
    # Mock de test : accepte temporairement tout appareil contenant 'test' ou un fabricant précis
    if not is_meta and "test" in dev_name:
        is_meta = True

    if is_meta:
        dist = calculate_distance(adv.rssi)
        angle = get_virtual_angle(device.address)
        return {
            "address": device.address,
            "name": device.name or "Meta Ray-Ban",
            "rssi": adv.rssi,
            "distance": dist,
            "angle": angle
        }
    return None