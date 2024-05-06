
from .gsm08 import GlobalSkyModel
from .gsm08 import GSMObserver

from .gsm16 import GlobalSkyModel16
from .gsm16 import GSMObserver16

from .lfsm import LowFrequencySkyModel
from .lfsm import LFSMObserver

from .haslam import HaslamSkyModel
from .haslam import HaslamObserver

# Add aliases
GlobalSkyModel08 = GlobalSkyModel
GSMObserver08    = GSMObserver

def init_gsm(gsm_name: str='gsm08'):
    """ Initialize a GDSM object by ID/name

    Returns a diffuse sky model (subclass of BaseSkyModel), based on one of:
      * **GSM08:** A model of diffuse Galactic radio emission from 10 MHz to 100 GHz,
                   [Oliveira-Costa et. al., (2008)](https://ui.adsabs.harvard.edu/abs/2008MNRAS.388..247D/abstract).
      * **GSM16:** An improved model of diffuse galactic radio emission from 10 MHz to 5 THz,
                   [Zheng et. al., (2016)](https://ui.adsabs.harvard.edu/abs/2017MNRAS.464.3486Z/abstract).
      * **LFSM:** The LWA1 Low Frequency Sky Survey (10-408 MHz)
                  [Dowell et. al. (2017)](https://ui.adsabs.harvard.edu/abs/2017MNRAS.469.4537D/abstract).
      * **Haslam:** A frequency-scaled model using a spectral index, based on the Haslam 408 MHz map
                   [Haslam 408 MHz](https://lambda.gsfc.nasa.gov/product/foreground/fg_2014_haslam_408_info.cfm).

    Args:
        gsm_name (str): One of 'gsm08', 'gsm16', 'lfsm' or 'haslam'

    Returns:
        sky_model (various): Corresponding sky model
    """
    gsm_name = gsm_name.lower().strip()
    match gsm_name:
        case 'gsm': # Shorthand for GSM08
            return GlobalSkyModel()
        case 'gsm08':
            return GlobalSkyModel()
        case 'gsm16':
            return GlobalSkyModel16()
        case 'lfsm':
            return LowFrequencySkyModel()
        case 'haslam':
            return HaslamSkyModel()


def init_observer(gsm_name: str='gsm08'):
    """ Initialize a GDSM Observer object by ID/name

    Returns an observer (subclass of BaseObserver), where the diffuse sky is created from one of:
      * **GSM08:** A model of diffuse Galactic radio emission from 10 MHz to 100 GHz,
                   [Oliveira-Costa et. al., (2008)](https://ui.adsabs.harvard.edu/abs/2008MNRAS.388..247D/abstract).
      * **GSM16:** An improved model of diffuse galactic radio emission from 10 MHz to 5 THz,
                   [Zheng et. al., (2016)](https://ui.adsabs.harvard.edu/abs/2017MNRAS.464.3486Z/abstract).
      * **LFSM:** The LWA1 Low Frequency Sky Survey (10-408 MHz)
                  [Dowell et. al. (2017)](https://ui.adsabs.harvard.edu/abs/2017MNRAS.469.4537D/abstract).
      * **Haslam:** A frequency-scaled model using a spectral index, based on the Haslam 408 MHz map
                   [Haslam 408 MHz](https://lambda.gsfc.nasa.gov/product/foreground/fg_2014_haslam_408_info.cfm).

    Args:
        gsm_name (str): One of 'gsm08', 'gsm16', 'lfsm' or 'haslam'

    Returns:
        observer (various): Corresponding sky model observer
    """
    gsm_name = gsm_name.lower().strip()
    match gsm_name:
        case 'gsm': # Shorthand for GSM08
            return GSMObserver()
        case 'gsm08':
            return GSMObserver()
        case 'gsm16':
            return GSMObserver16()
        case 'lfsm':
            return LFSMObserver()
        case 'haslam':
            return HaslamObserver()