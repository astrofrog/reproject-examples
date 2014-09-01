import glob
import time

from astropy import log
log.setLevel('WARN')
from reproject import reproject
from astropy.io import fits
from astropy.wcs import WCS

from montage_wrapper import reproject as reproject_montage

hdu = fits.open('MSX_E.fits')[0]
wcs_in = WCS(hdu.header)

print('{0:10s} {1:9s} {2:9s}'.format(' header', 'reproject', ' montage '))
print('---------- --------- ---------')

for header in glob.glob('*.hdr'):
    
    name = header.split('.')[0]

    # With 'reproject' package

    header_out = fits.Header.fromtextfile(header)
    wcs_out = WCS(header_out)

    time1 = time.time()
    array_out = reproject(hdu, wcs_out, shape_out=hdu.data.shape, projection_type='flux-conserving')
    time2 = time.time()

    fits.writeto(name + '_reproject.fits', array_out, header_out, clobber=True)
    
    # With montage

    time3 = time.time()
    reproject_montage('MSX_E.fits', name + '_montage.fits', header=header)
    time4 = time.time()
    
    print("{0:10s} {1:9.3f} {2:9.3f}".format(name, time2-time1, time4-time3))