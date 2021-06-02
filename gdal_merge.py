
#!/usr/bin/env python
###############################################################################
# $Id: gdal_merge.py 18669 2010-01-27 02:07:32Z chaitanya $
#
# Project:  InSAR Peppers
# Purpose:  Module to extract data from many rasters into one output.
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
# Copyright (c) 2000, Atlantis Scientific Inc. (www.atlsci.com)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
###############################################################################

try:
    from osgeo import gdal
    gdal.TermProgress = gdal.TermProgress_nocb
except ImportError:
    import gdal

import sys
import glob

__version__ = '$id$'[5:-1]
verbose = 0
quiet = 0


# =============================================================================
def raster_copy( s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
                 t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
                 nodata=None ):

    if nodata is not None:
        return raster_copy_with_nodata(
            s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
            t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
            nodata )

    if verbose != 0:
        print('Copy %d,%d,%d,%d to %d,%d,%d,%d.' \
              % (s_xoff, s_yoff, s_xsize, s_ysize,
             t_xoff, t_yoff, t_xsize, t_ysize ))

    s_band = s_fh.GetRasterBand( s_band_n )
    t_band = t_fh.GetRasterBand( t_band_n )

    data = s_band.ReadRaster( s_xoff, s_yoff, s_xsize, s_ysize,
                              t_xsize, t_ysize, t_band.DataType )
    t_band.WriteRaster( t_xoff, t_yoff, t_xsize, t_ysize,
                        data, t_xsize, t_ysize, t_band.DataType )
        

    return 0
    
# =============================================================================
def raster_copy_with_nodata( s_fh, s_xoff, s_yoff, s_xsize, s_ysize, s_band_n,
                             t_fh, t_xoff, t_yoff, t_xsize, t_ysize, t_band_n,
                             nodata ):
    try:
        import numpy as Numeric
    except ImportError:
        import Numeric
    
    if verbose != 0:
        print('Copy %d,%d,%d,%d to %d,%d,%d,%d.' \
              % (s_xoff, s_yoff, s_xsize, s_ysize,
             t_xoff, t_yoff, t_xsize, t_ysize ))

    s_band = s_fh.GetRasterBand( s_band_n )
    t_band = t_fh.GetRasterBand( t_band_n )

    data_src = s_band.ReadAsArray( s_xoff, s_yoff, s_xsize, s_ysize,
                                   t_xsize, t_ysize )
    data_dst = t_band.ReadAsArray( t_xoff, t_yoff, t_xsize, t_ysize )

    nodata_test = Numeric.equal(data_src,nodata)
    to_write = Numeric.choose( nodata_test, (data_src, data_dst) )
                               
    t_band.WriteArray( to_write, t_xoff, t_yoff )

    return 0
    
# =============================================================================
def names_to_fileinfos( names ):
    """
    Translate a list of GDAL filenames, into file_info objects.

    names -- list of valid GDAL dataset names.