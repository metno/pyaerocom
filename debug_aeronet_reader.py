
def main():
    import matplotlib.pyplot as plt
    plt.close("all")

    from pyaerocom import const
    from pyaerocom.io.readgridded import ReadGridded
    import pyaerocom.io as pio
    from pyaerocom.io import FileConventionRead
    filename = 'aerocom3_IPSL-CM6A-LR-INCA_piClim-control_od550dust_Column_9999_monthly.nc'

    print(FileConventionRead().from_file(filename))
    #pio.ReadUngridded()
    reader = ReadGridded("UKESM1-0-LL")
    files = "/home/oveh/MyPyaerocom/testdata-minimal/obsdata/AeronetSunV3Lev2.daily/renamed/Thessaloniki.lev30"
    od = reader.read(vars_to_retrieve="od550dust")
    print(od)

    # ETOPO1_Ice_g_gmt4.grd
if __name__ == "__main__":
    main()
