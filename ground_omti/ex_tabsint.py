
import pytplot
import matplotlib.pyplot as plt

from pyspedas.erg.ground.camera.camera_omti_asi import camera_omti_asi
from pyspedas.erg.ground.camera.tabsint import tabsint
from pyspedas.erg.ground.camera.rm_star_absint import rm_star_absint
from pyspedas.erg.ground.camera.plot_omti_image import plot_omti_image


def ex_tabsint():
    data = {
        't_range': ['2012-12-19 06:30:00', '2012-12-19  07:00:00'],
        'site': 'ath',
        'wavelength': [6300, 5725],
        'time': None,
        'x_min': 0,
        'y_min': 0,
        'x_max': None,
        'y_max': None
    }
    pytplot.del_data()

    camera_omti_asi(trange=data['t_range'],
                    site=data['site'],
                    wavelength=data['wavelength'])
    
    tabsint(data['site'], data['wavelength'])


if __name__ == '__main__':
    ex_tabsint()
