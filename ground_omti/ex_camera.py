import pytplot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from pyspedas.erg.ground.camera.camera_omti_asi import camera_omti_asi
from pyspedas.erg.ground.camera.plot_omti_image import plot_omti_image
from pyspedas.erg.ground.camera.plot_omti_gmap import plot_omti_gmap
from pyspedas.erg.ground.camera.tmake_image_dev import tmake_image_dev
from pyspedas.erg.ground.camera.tmake_map_table import tmake_map_table
from pyspedas.erg.ground.camera.tasi2gmap import tasi2gmap
from pyspedas.erg.ground.camera.keogram_image import keogram_image
from pyspedas.erg.ground.camera.rm_star_absint import rm_star_absint


def ex_camera():
    data = {
        't_range': ['2012-12-19 06:00:00', '2012-12-19 08:00:00'],
        'site': 'ath',
        'wavelength_ag': '6300',
        'wavelength_bg': '5577',
        'time': None,
        'pixels': {'x_min': 0,
                   'y_min': 0,
                   'x_max': None,
                   'y_max': None},
        'coords': {'x_min': None,
                   'y_min': None,
                   'x_max': None,
                   'y_max': None},
        'raw': {'z_min': 0,
                'z_max': 20000},
        'dev': {'z_min': -0.2,
                'z_max': 0.2},
        'mapping_alt': '400',
        'grid': 0.1,
        'map_size': None,
        'in_km': False,
        'lat': 60.0,
        'lon': 240.0
    }

    def get_time(v_name):
        times, ag_data = pytplot.get_data(v_name)
        time = data['time']
        if time is None:
            time = times[16]
        return time

    def make_dev_var(v_name):
        tmake_image_dev(v_name)
        return f'{v_name}_dev'

    def make_gmap_var(v_name):
        tmake_map_table(v_name,
                        mapping_alt=data['mapping_alt'],
                        grid=data['grid'],
                        map_size=data['map_size'],
                        in_km=data['in_km'])
        gmap_table_name = f"omti_asi_{data['site']}_{data['wavelength_ag']}_gmap_table_{int(data['mapping_alt'])}"
        tasi2gmap(v_name, gmap_table_name)
        return f"{v_name}_gmap_{str(int(data['mapping_alt']))}"

    pytplot.del_data()
    camera_omti_asi(trange=data['t_range'],
                    site=data['site'],
                    wavelength=data['wavelength_ag'])

    image_raw_name = f"omti_asi_{data['site']}_{data['wavelength_ag']}_image_raw"
    if image_raw_name not in pytplot.tplot_names():
        print('Image data variable is absent. Please, check the input data.')
        return

    print('\n======== Testing of functions ========\n')
    print('1. Plot a raw image in pixels')
    print('2. Plot a dev image in pixels')
    print('3. Plot a raw image in geographic coordinates')
    print('4. Plot a dev image in geographic coordinates')
    print('5. Plot raw keograms')
    print('6. Plot dev keograms')
    print('7. Remove star lights from a raw image (for demonstration only)')
    num = int(input('Please, pick the number: '))

    if num == 1:
        plot_omti_image(image_raw_name, time=get_time(image_raw_name),
                        x_max=data['pixels']['x_max'], y_max=data['pixels']['y_max'],
                        x_min=data['pixels']['x_min'], y_min=data['pixels']['y_min'],
                        z_min=data['raw']['z_min'], z_max=data['raw']['z_max'],
                        factor=1.2)

    elif num == 2:
        image_dev_name = make_dev_var(image_raw_name)
        plot_omti_image(image_dev_name, time=get_time(image_dev_name),
                        x_max=data['pixels']['x_max'], y_max=data['pixels']['y_max'],
                        x_min=data['pixels']['x_min'], y_min=data['pixels']['y_min'],
                        z_min=data['dev']['z_min'], z_max=data['dev']['z_max'],
                        factor=1.2)

    elif num == 3:
        image_gmap_name = make_gmap_var(image_raw_name)
        plot_omti_gmap(image_gmap_name, time=get_time(image_raw_name),
                       x_min=data['coords']['x_min'], x_max=data['coords']['x_max'],
                       y_min=data['coords']['y_min'], y_max=data['coords']['y_max'],
                       z_min=data['raw']['z_min'], z_max=data['raw']['z_max'],
                       factor=1.2)

    elif num == 4:
        image_dev_name = make_dev_var(image_raw_name)
        image_gmap_name = make_gmap_var(image_dev_name)
        plot_omti_gmap(image_gmap_name, time=get_time(image_dev_name),
                       x_min=data['coords']['x_min'], x_max=data['coords']['x_max'],
                       y_min=data['coords']['y_min'], y_max=data['coords']['y_max'],
                       z_min=data['dev']['z_min'], z_max=data['dev']['z_max'],
                       factor=1.2)

    elif num == 5:
        image_gmap_name = make_gmap_var(image_raw_name)
        keogram_image(image_gmap_name, lat=data['lat'], lon=data['lon'])
        keogram_lon_name = f"{image_gmap_name}_keogram_lon_{int(data['lon'])}"
        keogram_lat_name = f"{image_gmap_name}_keogram_lat_{int(data['lat'])}"
        pytplot.options(keogram_lon_name,
                        'zrange', [data['raw']['z_min'], data['raw']['z_max']])
        pytplot.options(keogram_lat_name,
                        'zrange', [data['raw']['z_min'], data['raw']['z_max']])
        pytplot.tplot([keogram_lon_name, keogram_lat_name])

    elif num == 6:
        image_dev_name = make_dev_var(image_raw_name)
        image_gmap_name = make_gmap_var(image_dev_name)
        keogram_image(image_gmap_name, lat=data['lat'], lon=data['lon'])
        keogram_lon_name = f"{image_gmap_name}_keogram_lon_{int(data['lon'])}"
        keogram_lat_name = f"{image_gmap_name}_keogram_lat_{int(data['lat'])}"
        pytplot.options(keogram_lon_name,
                        'zrange', [data['dev']['z_min'], data['dev']['z_max']])
        pytplot.options(keogram_lat_name,
                        'zrange', [data['dev']['z_min'], data['dev']['z_max']])
        pytplot.tplot([keogram_lon_name, keogram_lat_name])

    elif num == 7:
        times, ag_data = pytplot.get_data(image_raw_name)
        img0 = ag_data[16]
        img_out = rm_star_absint(img0)
        fig = plt.figure()
        ax1 = fig.add_subplot(121)  # left side
        ax2 = fig.add_subplot(122)  # right side

        _colors = pytplot.spedas_colorbar
        spd_map = [(np.array([r, g, b])).astype(np.float64) / 256
                   for r, g, b in zip(_colors.r, _colors.g, _colors.b)]
        cmap = LinearSegmentedColormap.from_list('spedas', spd_map)

        im1 = ax1.imshow(img0, cmap=cmap)
        ax1.set_title('Before')
        im2 = ax2.imshow(img_out, cmap=cmap)
        ax2.set_title('After')
        plt.colorbar(im1, location='bottom')
        plt.colorbar(im2, location='bottom')
        plt.tight_layout()
        plt.show()

    else:
        print('The number is incorrect.')


if __name__ == '__main__':
    ex_camera()
