import pkg_resources

def _get_image_path(image_name: str) -> str:
    image_path = pkg_resources.resource_filename(__name__, image_name)
    
    return image_path

BANCAMIGA  = _get_image_path('bancamiga.png')
MERCANTIL  = _get_image_path('banco-mercantil.png')
PROVINCIAL = _get_image_path('banco-provincial.png')
BDV        = _get_image_path('banco-venezuela.png')
BANESCO    = _get_image_path('banesco.png')
BANPLUS    = _get_image_path('banplus.png')
BNC        = _get_image_path('bnc.png')

ENPARALELOVZLA = _get_image_path('vmo.png')
UPHOLD         = _get_image_path('veuph.png')
SKRILL         = _get_image_path('veskr.png')
BCV            = _get_image_path('ves.png')
PAYPAL         = _get_image_path('vepay.png')
AMAZON         = _get_image_path('veamz.png')
DOLARTODAY     = _get_image_path('vdt.png')
CRIPTODOLAR    = _get_image_path('vcrip.png')
BINANCE        = _get_image_path('vbin.png')