orb( trange=['2017-04-24 00:00:00', '2017-04-25 00:00:00'])
labels = pytplot.split_vec( 'erg_orb_l2_pos_iono_north' )
pytplot.options( 'erg_orb_l2_pos_iono_north_0', 'ytitle', 'lat [deg]' )
pytplot.options( 'erg_orb_l2_pos_iono_north_1', 'ytitle', 'lon [deg]' )
from pytplot import tplot, split_vec, options
tplot('pos_iono_north_TS04')