import pytplot
import datetime as dt
from dateutil import parser

from pyspedas.erg.ground.camera.camera_omti_asi import camera_omti_asi
from pyspedas.erg.ground.camera.plot_omti_image import plot_omti_image
from pyspedas.erg.ground.camera.plot_omti_gmap import plot_omti_gmap
from pyspedas.erg.ground.camera.tmake_map_table import tmake_map_table
from pyspedas.erg.ground.camera.tasi2gmap import tasi2gmap
from pyspedas.erg.ground.camera.keogram_image import keogram_image


def ex_raw_image():
    data = {
        't_range': ['2012-12-19 06:00:00', '2012-12-19 15:00:00'],
        'site': 'ath',
        'wavelength': 6300,
        'time': '2012-12-19 06:51:01',
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
        'mapping_alt': '400',
        'grid': 0.1,
        'map_size': None,
        'in_km': False,
        'lat': 60.0,
        'lon': 240.0
    }

    def get_time(v_name):
        time_str = data['time']
        if time_str is None:
            times, ag_data = pytplot.get_data(v_name)
            time = times[0]
        else:
            try:
                time_format = parser.isoparse(time_str)
            except ValueError:
                time_format = parser.parse(time_str)
            time_format.replace(tzinfo=dt.timezone.utc)
            time = time_format.replace(tzinfo=dt.timezone.utc).timestamp()
        return time

    def make_gmap_var(v_name):
        tmake_map_table(v_name,
                        mapping_alt=data['mapping_alt'],
                        grid=data['grid'],
                        map_size=data['map_size'],
                        in_km=data['in_km'])
        gmap_table_name = f"omti_asi_{data['site']}_{data['wavelength']}_gmap_table_{int(data['mapping_alt'])}"
        tasi2gmap(v_name, gmap_table_name)
        return f"{v_name}_gmap_{str(int(data['mapping_alt']))}"

    pytplot.del_data()
    camera_omti_asi(trange=data['t_range'],
                    site=data['site'],
                    wavelength=data['wavelength'])

    image_raw_name = f"omti_asi_{data['site']}_{data['wavelength']}_image_raw"

    if image_raw_name not in pytplot.tplot_names():
        print('Image RAW data variable not found. Please, check the input data.')
        return

    print('\n======== Testing of functions ========\n')
    print('1. Plot a raw image in pixels')
    print('2. Plot a raw image in geographic coordinates')
    print('3. Plot raw keograms')

    num = int(input('Please, pick the number: '))

    if num == 1:
        plot_omti_image(image_raw_name, time=get_time(image_raw_name),
                        x_max=data['pixels']['x_max'], y_max=data['pixels']['y_max'],
                        x_min=data['pixels']['x_min'], y_min=data['pixels']['y_min'],
                        z_min=data['raw']['z_min'], z_max=data['raw']['z_max'],
                        factor=1.2)

    elif num == 2:
        image_gmap_name = make_gmap_var(image_raw_name)
        plot_omti_gmap(image_gmap_name, time=get_time(image_raw_name),
                       x_min=data['coords']['x_min'], x_max=data['coords']['x_max'],
                       y_min=data['coords']['y_min'], y_max=data['coords']['y_max'],
                       z_min=data['raw']['z_min'], z_max=data['raw']['z_max'],
                       factor=1.2)

    elif num == 3:
        image_gmap_name = make_gmap_var(image_raw_name)
        keogram_image(image_gmap_name, lat=data['lat'], lon=data['lon'])
        keogram_lon_name = f"{image_gmap_name}_keogram_lon_{int(data['lon'])}"
        keogram_lat_name = f"{image_gmap_name}_keogram_lat_{int(data['lat'])}"
        pytplot.options(keogram_lon_name,
                        'zrange', [data['raw']['z_min'], data['raw']['z_max']])
        pytplot.options(keogram_lat_name,
                        'zrange', [data['raw']['z_min'], data['raw']['z_max']])
        pytplot.tplot([keogram_lon_name, keogram_lat_name])

    else:
        print('The number is incorrect.')


if __name__ == '__main__':
    ex_raw_image()
