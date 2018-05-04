
Inspect performance of iris interpolation schemes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the Aerocom IDL tools, collocation of model data with point
observations is done using neirest neighbour interpolation. The
pyaerocom ``GridData`` class is based on (but not inherited from) the
iris ``Cube`` class, which includes an interpolation method that takes
one or multiple coordinates on input. The iris interpolation interface
supports neirest neighbour and linear grid interpolation.

This notebook was developed as a result of former tests, that revealed,
that the ``Cube`` interpolation method can be dramatically slow, since
it loads the whole grid into memory (even if only a single point is
accessed).

.. code:: ipython3

    import numpy as np
    import pyaerocom
    import time
    import iris
    
    def load_model_data():
        data = pyaerocom.GridData()
        data._init_testdata_default()
        return data.grid

Let's start with running tests for extracting a time series at a single
location using neirest neighbour. This is done in 3 ways:

1. Using the original Cube
2. Using a Cube that is cropped around the point of interest before
   interpolation
3. Extracting directly using the closest indices

We use the following coordinates:

.. code:: ipython3

    #single coordinate
    lon, lat = 10, 10

Case 1 - Iris interface original grid
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the iris interpolation interface on the original data grid stored
in the ``Cube``.

.. code:: ipython3

    %%time
    cube = load_model_data()
    s0_case1 = cube.interpolate(sample_points = [("longitude", lon), ("latitude", lat)], scheme=iris.analysis.Nearest()).data


.. parsed-literal::

    Rolling longitudes to -180 -> 180 definition
    CPU times: user 1.57 s, sys: 3.25 s, total: 4.82 s
    Wall time: 15.6 s


This took quite a while, the reason for this is, that the Interpolator
instance loads the whole grid into memory before doing the
interpolation. So for a single point (or only a few points) this does
not make a lot of sense. However, now that we have everything ready in
memory, we can do the whole thing for a lot more points, without
reloading the data, which is fast:

.. code:: ipython3

    # whole globe in 1degree resolution
    more_lons = np.arange(-180, 180, 1)
    more_lats = np.arange(-90, 90, 1)

.. code:: ipython3

    %time
    sub = cube.interpolate(sample_points = [("longitude", more_lons), ("latitude", more_lats)], scheme=iris.analysis.Nearest())
    print(sub.shape)


.. parsed-literal::

    CPU times: user 2 µs, sys: 2 µs, total: 4 µs
    Wall time: 7.15 µs
    (365, 180, 360)


Now, this gives us an instance of the ``Cube`` class. Let's just make
sure, accessing the data does not take ages again

.. code:: ipython3

    %%time
    data1 = sub.data


.. parsed-literal::

    CPU times: user 10 µs, sys: 9 µs, total: 19 µs
    Wall time: 22.9 µs


Case 2 - Iris interface cropped grid
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the iris interpolation interface after cropping the ``Cube``
within a suitable region-of-interest. For this, we first write a little
helper function that determines a suitable crop interval.

.. code:: ipython3

    def crop_around(lon, lat, stepdeg=2):
        lon_range = (lon-stepdeg, lon+stepdeg)
        lat_range = (lat-stepdeg, lat+stepdeg)
        return lon_range, lat_range
    
    print(crop_around(lon, lat))


.. parsed-literal::

    ((8, 12), (8, 12))


.. code:: ipython3

    %%time
    cube = load_model_data()
    #get grid resolution
    lonr, latr = crop_around(lon, lat)
    cropped = cube.intersection(longitude=lonr, latitude=latr)
    s0_case2 = cropped.interpolate(sample_points=[("longitude", lon), ("latitude", lat)], scheme=iris.analysis.Nearest()).data


.. parsed-literal::

    Rolling longitudes to -180 -> 180 definition
    CPU times: user 181 ms, sys: 295 ms, total: 476 ms
    Wall time: 4.14 s


Well, this was considerably faster, but only got us one point (in about
2s). I spare you the time to loop over all points in the additional
arrays. Make sure, the extracted arrays of both cases are equal.

.. code:: ipython3

    np.testing.assert_array_equal(s0_case1, s0_case2)

Case 3 - Finding and extracting closest point using numpy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let's load the data again and extract the lon / lat coordinate arrays

.. code:: ipython3

    cube = load_model_data()
    lons, lats = cube.coord("longitude").points, cube.coord("latitude").points
    print(cube.shape)


.. parsed-literal::

    Rolling longitudes to -180 -> 180 definition
    (365, 451, 900)


Write a helper method that finds the current index

.. code:: ipython3

    def get_closest_index(lons, lats, lon, lat):
        return (np.argmin(np.abs(lons - lon)), np.argmin(np.abs(lats - lat)))

And extract time series for the first point:

.. code:: ipython3

    %%time
    idx_lon, idx_lat = get_closest_index(lons, lats, lon, lat)
    s0_case3 = cube[:, idx_lat, idx_lon].data


.. parsed-literal::

    CPU times: user 111 ms, sys: 51 ms, total: 162 ms
    Wall time: 507 ms


Again, before applying this method to all coordinates in
``more_lons, more_lats``, make sure the numbers are right.

.. code:: ipython3

    np.testing.assert_array_equal(s0_case1, s0_case3)

Now for the whole thing:

.. code:: ipython3

    %%time
    data = np.empty((365, len(more_lats), len(more_lons)))
    for i in range(len(more_lons)):
        for j in range(len(more_lats)):
            lon, lat = more_lons[i], more_lats[j]
            idx_lon, idx_lat = get_closest_index(lons, lats, lon, lat)
            data[:,j,i] = cube[:, idx_lat, idx_lon].data
            


.. parsed-literal::

    CPU times: user 2h 33min 23s, sys: 1h 11min 10s, total: 3h 44min 33s
    Wall time: 8h 30min 48s


Now, this took more than 3 times as long as the case iris interface on
the original grid. Note, however, that for a single or only a few points
this method outperforms the iris method by far.

Comparing Case 1 and Case 3 based on realistic obsdata case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now comparing the two cases (i.e. iris, vs custom numpy method) based on
the approximate number of stations of the AeroNet network (i.e. using
400 data points, i.e. a 20 x 20 point grid).

.. code:: ipython3

    little_less_lons = np.linspace(-180, 180, 20)
    little_less_lats = np.linspace(-90, 90, 20)

Case1 (400 datapoints)
^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    %%time
    cube = load_model_data()
    cube.interpolate(sample_points = [("longitude", little_less_lons), 
                                                 ("latitude", little_less_lats)], scheme=iris.analysis.Nearest()).data


.. parsed-literal::

    Rolling longitudes to -180 -> 180 definition
    CPU times: user 1.28 s, sys: 3.67 s, total: 4.95 s
    Wall time: 15 s


Case 3 (400 datapoints)
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    %%time
    cube = load_model_data()
    lons, lats = cube.coord("longitude").points, cube.coord("latitude").points
    
    data = np.empty((365, len(little_less_lats), len(little_less_lons)))
    for i in range(len(little_less_lons)):
        print(i)
        for j in range(len(little_less_lats)):
            lon, lat = little_less_lons[i], little_less_lats[j]
            idx_lon, idx_lat = get_closest_index(lons, lats, lon, lat)
            data[:,j,i] = cube[:, idx_lat, idx_lon].data


.. parsed-literal::

    Rolling longitudes to -180 -> 180 definition
    0
    CPU times: user 114 ms, sys: 52.8 ms, total: 167 ms
    Wall time: 390 ms
    CPU times: user 146 ms, sys: 61.2 ms, total: 208 ms
    Wall time: 425 ms
    CPU times: user 122 ms, sys: 92.8 ms, total: 215 ms
    Wall time: 453 ms
    CPU times: user 147 ms, sys: 159 ms, total: 307 ms
    Wall time: 3.1 s
    CPU times: user 211 ms, sys: 96 ms, total: 307 ms
    Wall time: 2.99 s
    CPU times: user 189 ms, sys: 112 ms, total: 301 ms
    Wall time: 2.59 s
    CPU times: user 175 ms, sys: 85.8 ms, total: 261 ms
    Wall time: 2.56 s
    CPU times: user 173 ms, sys: 114 ms, total: 287 ms
    Wall time: 3.43 s
    CPU times: user 129 ms, sys: 131 ms, total: 260 ms
    Wall time: 2.58 s
    CPU times: user 188 ms, sys: 134 ms, total: 322 ms
    Wall time: 2.92 s
    CPU times: user 173 ms, sys: 128 ms, total: 302 ms
    Wall time: 2.51 s
    CPU times: user 145 ms, sys: 173 ms, total: 317 ms
    Wall time: 2.49 s
    CPU times: user 198 ms, sys: 133 ms, total: 331 ms
    Wall time: 2.45 s
    CPU times: user 189 ms, sys: 133 ms, total: 322 ms
    Wall time: 2.35 s
    CPU times: user 185 ms, sys: 133 ms, total: 318 ms
    Wall time: 2.53 s
    CPU times: user 212 ms, sys: 98.2 ms, total: 310 ms
    Wall time: 2.56 s
    CPU times: user 209 ms, sys: 110 ms, total: 320 ms
    Wall time: 2.85 s
    CPU times: user 159 ms, sys: 101 ms, total: 260 ms
    Wall time: 2.45 s
    CPU times: user 163 ms, sys: 110 ms, total: 273 ms
    Wall time: 2.85 s
    CPU times: user 153 ms, sys: 90.4 ms, total: 244 ms
    Wall time: 1.91 s
    1
    CPU times: user 139 ms, sys: 54 ms, total: 193 ms
    Wall time: 439 ms
    CPU times: user 124 ms, sys: 72.8 ms, total: 197 ms
    Wall time: 450 ms
    CPU times: user 147 ms, sys: 44.7 ms, total: 191 ms
    Wall time: 434 ms
    CPU times: user 144 ms, sys: 45.2 ms, total: 189 ms
    Wall time: 429 ms
    CPU times: user 119 ms, sys: 53.2 ms, total: 172 ms
    Wall time: 441 ms
    CPU times: user 156 ms, sys: 50.8 ms, total: 207 ms
    Wall time: 447 ms
    CPU times: user 165 ms, sys: 49.2 ms, total: 215 ms
    Wall time: 501 ms
    CPU times: user 155 ms, sys: 72.1 ms, total: 227 ms
    Wall time: 477 ms
    CPU times: user 142 ms, sys: 48.4 ms, total: 191 ms
    Wall time: 429 ms
    CPU times: user 132 ms, sys: 41.2 ms, total: 173 ms
    Wall time: 425 ms
    CPU times: user 157 ms, sys: 53.3 ms, total: 210 ms
    Wall time: 443 ms
    CPU times: user 142 ms, sys: 53.4 ms, total: 196 ms
    Wall time: 449 ms
    CPU times: user 167 ms, sys: 70 ms, total: 237 ms
    Wall time: 524 ms
    CPU times: user 151 ms, sys: 53 ms, total: 204 ms
    Wall time: 462 ms
    CPU times: user 118 ms, sys: 39.7 ms, total: 158 ms
    Wall time: 441 ms
    CPU times: user 118 ms, sys: 68.7 ms, total: 187 ms
    Wall time: 469 ms
    CPU times: user 129 ms, sys: 44.5 ms, total: 174 ms
    Wall time: 446 ms
    CPU times: user 137 ms, sys: 71.5 ms, total: 208 ms
    Wall time: 627 ms
    CPU times: user 109 ms, sys: 72.2 ms, total: 181 ms
    Wall time: 442 ms
    CPU times: user 104 ms, sys: 80.8 ms, total: 185 ms
    Wall time: 447 ms
    2
    CPU times: user 130 ms, sys: 66.3 ms, total: 196 ms
    Wall time: 451 ms
    CPU times: user 145 ms, sys: 51.6 ms, total: 197 ms
    Wall time: 440 ms
    CPU times: user 77.7 ms, sys: 30.6 ms, total: 108 ms
    Wall time: 382 ms
    CPU times: user 73.5 ms, sys: 21.3 ms, total: 94.8 ms
    Wall time: 335 ms
    CPU times: user 129 ms, sys: 64.6 ms, total: 194 ms
    Wall time: 430 ms
    CPU times: user 129 ms, sys: 75 ms, total: 204 ms
    Wall time: 445 ms
    CPU times: user 135 ms, sys: 52.2 ms, total: 187 ms
    Wall time: 436 ms
    CPU times: user 118 ms, sys: 65.2 ms, total: 184 ms
    Wall time: 436 ms
    CPU times: user 124 ms, sys: 64.5 ms, total: 189 ms
    Wall time: 446 ms
    CPU times: user 135 ms, sys: 55.8 ms, total: 191 ms
    Wall time: 443 ms
    CPU times: user 107 ms, sys: 60.6 ms, total: 167 ms
    Wall time: 435 ms
    CPU times: user 116 ms, sys: 64.2 ms, total: 181 ms
    Wall time: 452 ms
    CPU times: user 107 ms, sys: 68.9 ms, total: 176 ms
    Wall time: 447 ms
    CPU times: user 106 ms, sys: 57.9 ms, total: 163 ms
    Wall time: 420 ms
    CPU times: user 165 ms, sys: 56.8 ms, total: 222 ms
    Wall time: 530 ms
    CPU times: user 133 ms, sys: 66.2 ms, total: 200 ms
    Wall time: 437 ms
    CPU times: user 119 ms, sys: 84.6 ms, total: 204 ms
    Wall time: 497 ms
    CPU times: user 116 ms, sys: 56.2 ms, total: 172 ms
    Wall time: 427 ms
    CPU times: user 147 ms, sys: 70 ms, total: 217 ms
    Wall time: 492 ms
    CPU times: user 152 ms, sys: 68.4 ms, total: 221 ms
    Wall time: 708 ms
    3
    CPU times: user 145 ms, sys: 54.8 ms, total: 200 ms
    Wall time: 473 ms
    CPU times: user 146 ms, sys: 67.6 ms, total: 214 ms
    Wall time: 463 ms
    CPU times: user 124 ms, sys: 74.5 ms, total: 199 ms
    Wall time: 460 ms
    CPU times: user 139 ms, sys: 53 ms, total: 192 ms
    Wall time: 448 ms
    CPU times: user 123 ms, sys: 80.8 ms, total: 204 ms
    Wall time: 453 ms
    CPU times: user 107 ms, sys: 67 ms, total: 174 ms
    Wall time: 440 ms
    CPU times: user 150 ms, sys: 64.6 ms, total: 214 ms
    Wall time: 462 ms
    CPU times: user 119 ms, sys: 87.8 ms, total: 207 ms
    Wall time: 471 ms
    CPU times: user 136 ms, sys: 54.3 ms, total: 191 ms
    Wall time: 440 ms
    CPU times: user 124 ms, sys: 68.7 ms, total: 193 ms
    Wall time: 432 ms
    CPU times: user 145 ms, sys: 55.8 ms, total: 200 ms
    Wall time: 433 ms
    CPU times: user 108 ms, sys: 93.3 ms, total: 201 ms
    Wall time: 515 ms
    CPU times: user 137 ms, sys: 48.7 ms, total: 185 ms
    Wall time: 436 ms
    CPU times: user 120 ms, sys: 61.4 ms, total: 181 ms
    Wall time: 496 ms
    CPU times: user 129 ms, sys: 61.6 ms, total: 190 ms
    Wall time: 481 ms
    CPU times: user 144 ms, sys: 64.2 ms, total: 208 ms
    Wall time: 488 ms
    CPU times: user 126 ms, sys: 58.2 ms, total: 184 ms
    Wall time: 480 ms
    CPU times: user 135 ms, sys: 50.1 ms, total: 185 ms
    Wall time: 456 ms
    CPU times: user 152 ms, sys: 61.4 ms, total: 213 ms
    Wall time: 551 ms
    CPU times: user 143 ms, sys: 36 ms, total: 179 ms
    Wall time: 510 ms
    4
    CPU times: user 103 ms, sys: 40.2 ms, total: 143 ms
    Wall time: 406 ms
    CPU times: user 154 ms, sys: 80.1 ms, total: 234 ms
    Wall time: 484 ms
    CPU times: user 122 ms, sys: 75.5 ms, total: 198 ms
    Wall time: 466 ms
    CPU times: user 113 ms, sys: 23.3 ms, total: 136 ms
    Wall time: 397 ms
    CPU times: user 163 ms, sys: 37.2 ms, total: 200 ms
    Wall time: 457 ms
    CPU times: user 111 ms, sys: 55.9 ms, total: 166 ms
    Wall time: 454 ms
    CPU times: user 78.5 ms, sys: 23.7 ms, total: 102 ms
    Wall time: 380 ms
    CPU times: user 77 ms, sys: 58.3 ms, total: 135 ms
    Wall time: 406 ms
    CPU times: user 91.1 ms, sys: 46.4 ms, total: 137 ms
    Wall time: 389 ms
    CPU times: user 113 ms, sys: 46.5 ms, total: 160 ms
    Wall time: 423 ms
    CPU times: user 105 ms, sys: 61.5 ms, total: 167 ms
    Wall time: 462 ms
    CPU times: user 106 ms, sys: 38.6 ms, total: 144 ms
    Wall time: 428 ms
    CPU times: user 121 ms, sys: 41.4 ms, total: 163 ms
    Wall time: 447 ms
    CPU times: user 108 ms, sys: 82.2 ms, total: 191 ms
    Wall time: 470 ms
    CPU times: user 119 ms, sys: 59.7 ms, total: 179 ms
    Wall time: 450 ms
    CPU times: user 150 ms, sys: 35.6 ms, total: 186 ms
    Wall time: 477 ms
    CPU times: user 141 ms, sys: 56.1 ms, total: 197 ms
    Wall time: 462 ms
    CPU times: user 188 ms, sys: 44.6 ms, total: 233 ms
    Wall time: 486 ms
    CPU times: user 135 ms, sys: 82.1 ms, total: 217 ms
    Wall time: 461 ms
    CPU times: user 150 ms, sys: 49.5 ms, total: 199 ms
    Wall time: 435 ms
    5
    CPU times: user 137 ms, sys: 61.7 ms, total: 199 ms
    Wall time: 434 ms
    CPU times: user 121 ms, sys: 44.6 ms, total: 165 ms
    Wall time: 430 ms
    CPU times: user 160 ms, sys: 56.1 ms, total: 216 ms
    Wall time: 690 ms
    CPU times: user 141 ms, sys: 76 ms, total: 217 ms
    Wall time: 460 ms
    CPU times: user 117 ms, sys: 65.2 ms, total: 182 ms
    Wall time: 432 ms
    CPU times: user 141 ms, sys: 63.7 ms, total: 205 ms
    Wall time: 439 ms
    CPU times: user 128 ms, sys: 39.3 ms, total: 167 ms
    Wall time: 437 ms
    CPU times: user 202 ms, sys: 40.2 ms, total: 242 ms
    Wall time: 536 ms
    CPU times: user 123 ms, sys: 63.8 ms, total: 187 ms
    Wall time: 641 ms
    CPU times: user 165 ms, sys: 40.3 ms, total: 205 ms
    Wall time: 465 ms
    CPU times: user 149 ms, sys: 49.9 ms, total: 198 ms
    Wall time: 464 ms
    CPU times: user 160 ms, sys: 56.3 ms, total: 216 ms
    Wall time: 477 ms
    CPU times: user 147 ms, sys: 48.6 ms, total: 195 ms
    Wall time: 488 ms
    CPU times: user 141 ms, sys: 62.9 ms, total: 204 ms
    Wall time: 457 ms
    CPU times: user 104 ms, sys: 71.2 ms, total: 175 ms
    Wall time: 439 ms
    CPU times: user 118 ms, sys: 65.3 ms, total: 183 ms
    Wall time: 459 ms
    CPU times: user 146 ms, sys: 54 ms, total: 200 ms
    Wall time: 446 ms
    CPU times: user 168 ms, sys: 43.1 ms, total: 211 ms
    Wall time: 466 ms
    CPU times: user 150 ms, sys: 66.9 ms, total: 217 ms
    Wall time: 445 ms
    CPU times: user 134 ms, sys: 61.7 ms, total: 196 ms
    Wall time: 445 ms
    6
    CPU times: user 200 ms, sys: 82.4 ms, total: 283 ms
    Wall time: 524 ms
    CPU times: user 172 ms, sys: 73 ms, total: 245 ms
    Wall time: 496 ms
    CPU times: user 139 ms, sys: 76.8 ms, total: 215 ms
    Wall time: 448 ms
    CPU times: user 130 ms, sys: 64.3 ms, total: 194 ms
    Wall time: 443 ms
    CPU times: user 102 ms, sys: 53.7 ms, total: 156 ms
    Wall time: 445 ms
    CPU times: user 135 ms, sys: 56.3 ms, total: 192 ms
    Wall time: 452 ms
    CPU times: user 163 ms, sys: 49.3 ms, total: 212 ms
    Wall time: 472 ms
    CPU times: user 142 ms, sys: 27.4 ms, total: 169 ms
    Wall time: 425 ms
    CPU times: user 120 ms, sys: 58.1 ms, total: 178 ms
    Wall time: 426 ms
    CPU times: user 130 ms, sys: 64.2 ms, total: 195 ms
    Wall time: 466 ms
    CPU times: user 135 ms, sys: 62.2 ms, total: 198 ms
    Wall time: 498 ms
    CPU times: user 165 ms, sys: 46 ms, total: 211 ms
    Wall time: 475 ms
    CPU times: user 139 ms, sys: 59.6 ms, total: 198 ms
    Wall time: 499 ms
    CPU times: user 127 ms, sys: 56.4 ms, total: 184 ms
    Wall time: 445 ms
    CPU times: user 136 ms, sys: 21.5 ms, total: 158 ms
    Wall time: 414 ms
    CPU times: user 148 ms, sys: 59.9 ms, total: 208 ms
    Wall time: 439 ms
    CPU times: user 150 ms, sys: 55 ms, total: 205 ms
    Wall time: 436 ms
    CPU times: user 138 ms, sys: 59.9 ms, total: 197 ms
    Wall time: 649 ms
    CPU times: user 91.6 ms, sys: 52.2 ms, total: 144 ms
    Wall time: 393 ms
    CPU times: user 126 ms, sys: 62.1 ms, total: 188 ms
    Wall time: 424 ms
    7
    CPU times: user 131 ms, sys: 48 ms, total: 179 ms
    Wall time: 425 ms
    CPU times: user 118 ms, sys: 44.3 ms, total: 162 ms
    Wall time: 451 ms
    CPU times: user 156 ms, sys: 54.4 ms, total: 210 ms
    Wall time: 449 ms
    CPU times: user 140 ms, sys: 69 ms, total: 209 ms
    Wall time: 447 ms
    CPU times: user 161 ms, sys: 47.2 ms, total: 208 ms
    Wall time: 489 ms
    CPU times: user 155 ms, sys: 44.4 ms, total: 200 ms
    Wall time: 445 ms
    CPU times: user 146 ms, sys: 52.8 ms, total: 198 ms
    Wall time: 489 ms
    CPU times: user 131 ms, sys: 54 ms, total: 185 ms
    Wall time: 469 ms
    CPU times: user 141 ms, sys: 60.3 ms, total: 201 ms
    Wall time: 516 ms
    CPU times: user 123 ms, sys: 69.2 ms, total: 192 ms
    Wall time: 479 ms
    CPU times: user 151 ms, sys: 48 ms, total: 199 ms
    Wall time: 442 ms
    CPU times: user 145 ms, sys: 58.1 ms, total: 203 ms
    Wall time: 456 ms
    CPU times: user 150 ms, sys: 54.5 ms, total: 205 ms
    Wall time: 448 ms
    CPU times: user 159 ms, sys: 44.1 ms, total: 203 ms
    Wall time: 465 ms
    CPU times: user 152 ms, sys: 45 ms, total: 197 ms
    Wall time: 664 ms
    CPU times: user 140 ms, sys: 59.9 ms, total: 199 ms
    Wall time: 458 ms
    CPU times: user 124 ms, sys: 61.1 ms, total: 185 ms
    Wall time: 432 ms
    CPU times: user 143 ms, sys: 59.4 ms, total: 202 ms
    Wall time: 452 ms
    CPU times: user 129 ms, sys: 61.7 ms, total: 190 ms
    Wall time: 452 ms
    CPU times: user 170 ms, sys: 51.6 ms, total: 222 ms
    Wall time: 472 ms
    8
    CPU times: user 161 ms, sys: 36.2 ms, total: 197 ms
    Wall time: 466 ms
    CPU times: user 114 ms, sys: 85.4 ms, total: 199 ms
    Wall time: 475 ms
    CPU times: user 144 ms, sys: 45.2 ms, total: 189 ms
    Wall time: 433 ms
    CPU times: user 117 ms, sys: 68.9 ms, total: 186 ms
    Wall time: 461 ms
    CPU times: user 158 ms, sys: 55.3 ms, total: 213 ms
    Wall time: 517 ms
    CPU times: user 125 ms, sys: 38.4 ms, total: 164 ms
    Wall time: 446 ms
    CPU times: user 163 ms, sys: 39.4 ms, total: 203 ms
    Wall time: 491 ms
    CPU times: user 137 ms, sys: 55.2 ms, total: 192 ms
    Wall time: 470 ms
    CPU times: user 133 ms, sys: 74.7 ms, total: 207 ms
    Wall time: 714 ms
    CPU times: user 142 ms, sys: 34 ms, total: 176 ms
    Wall time: 464 ms
    CPU times: user 124 ms, sys: 57.1 ms, total: 181 ms
    Wall time: 731 ms
    CPU times: user 42 ms, sys: 41.1 ms, total: 83.1 ms
    Wall time: 393 ms
    CPU times: user 85.7 ms, sys: 42.1 ms, total: 128 ms
    Wall time: 404 ms
    CPU times: user 129 ms, sys: 46.9 ms, total: 176 ms
    Wall time: 485 ms
    CPU times: user 147 ms, sys: 62.3 ms, total: 210 ms
    Wall time: 479 ms
    CPU times: user 195 ms, sys: 49.8 ms, total: 245 ms
    Wall time: 491 ms
    CPU times: user 166 ms, sys: 75.3 ms, total: 241 ms
    Wall time: 496 ms
    CPU times: user 151 ms, sys: 72 ms, total: 223 ms
    Wall time: 465 ms
    CPU times: user 115 ms, sys: 70.3 ms, total: 186 ms
    Wall time: 432 ms
    CPU times: user 129 ms, sys: 85.2 ms, total: 214 ms
    Wall time: 451 ms
    9
    CPU times: user 124 ms, sys: 84.9 ms, total: 209 ms
    Wall time: 430 ms
    CPU times: user 93.1 ms, sys: 16.2 ms, total: 109 ms
    Wall time: 439 ms
    CPU times: user 153 ms, sys: 61.1 ms, total: 214 ms
    Wall time: 549 ms
    CPU times: user 148 ms, sys: 64.6 ms, total: 212 ms
    Wall time: 514 ms
    CPU times: user 109 ms, sys: 95.5 ms, total: 205 ms
    Wall time: 477 ms
    CPU times: user 129 ms, sys: 48.8 ms, total: 178 ms
    Wall time: 429 ms
    CPU times: user 148 ms, sys: 51.7 ms, total: 199 ms
    Wall time: 464 ms
    CPU times: user 139 ms, sys: 79 ms, total: 218 ms
    Wall time: 442 ms
    CPU times: user 151 ms, sys: 54.5 ms, total: 206 ms
    Wall time: 476 ms
    CPU times: user 139 ms, sys: 69.2 ms, total: 208 ms
    Wall time: 445 ms
    CPU times: user 171 ms, sys: 36.5 ms, total: 207 ms
    Wall time: 443 ms
    CPU times: user 123 ms, sys: 90 ms, total: 213 ms
    Wall time: 445 ms
    CPU times: user 156 ms, sys: 55.7 ms, total: 212 ms
    Wall time: 449 ms
    CPU times: user 154 ms, sys: 52.5 ms, total: 207 ms
    Wall time: 449 ms
    CPU times: user 122 ms, sys: 80.3 ms, total: 202 ms
    Wall time: 432 ms
    CPU times: user 152 ms, sys: 58.7 ms, total: 210 ms
    Wall time: 461 ms
    CPU times: user 153 ms, sys: 59.6 ms, total: 213 ms
    Wall time: 444 ms
    CPU times: user 163 ms, sys: 56.7 ms, total: 220 ms
    Wall time: 487 ms
    CPU times: user 152 ms, sys: 59.6 ms, total: 211 ms
    Wall time: 447 ms
    CPU times: user 137 ms, sys: 57.4 ms, total: 194 ms
    Wall time: 434 ms
    10
    CPU times: user 165 ms, sys: 87.8 ms, total: 253 ms
    Wall time: 1.07 s
    CPU times: user 156 ms, sys: 81.1 ms, total: 237 ms
    Wall time: 990 ms
    CPU times: user 167 ms, sys: 73.7 ms, total: 241 ms
    Wall time: 923 ms
    CPU times: user 164 ms, sys: 88.7 ms, total: 253 ms
    Wall time: 970 ms
    CPU times: user 158 ms, sys: 77.5 ms, total: 236 ms
    Wall time: 849 ms
    CPU times: user 137 ms, sys: 111 ms, total: 248 ms
    Wall time: 959 ms
    CPU times: user 171 ms, sys: 57.4 ms, total: 228 ms
    Wall time: 862 ms
    CPU times: user 152 ms, sys: 76.9 ms, total: 229 ms
    Wall time: 917 ms
    CPU times: user 183 ms, sys: 52.8 ms, total: 236 ms
    Wall time: 868 ms
    CPU times: user 167 ms, sys: 77 ms, total: 244 ms
    Wall time: 863 ms
    CPU times: user 163 ms, sys: 58.6 ms, total: 221 ms
    Wall time: 840 ms
    CPU times: user 144 ms, sys: 83.7 ms, total: 228 ms
    Wall time: 807 ms
    CPU times: user 111 ms, sys: 75.3 ms, total: 186 ms
    Wall time: 816 ms
    CPU times: user 178 ms, sys: 54.5 ms, total: 233 ms
    Wall time: 807 ms
    CPU times: user 133 ms, sys: 92.3 ms, total: 226 ms
    Wall time: 817 ms
    CPU times: user 153 ms, sys: 95 ms, total: 248 ms
    Wall time: 1.02 s
    CPU times: user 147 ms, sys: 91.6 ms, total: 238 ms
    Wall time: 811 ms
    CPU times: user 159 ms, sys: 71.8 ms, total: 231 ms
    Wall time: 850 ms
    CPU times: user 161 ms, sys: 76.8 ms, total: 238 ms
    Wall time: 860 ms
    CPU times: user 170 ms, sys: 49.3 ms, total: 220 ms
    Wall time: 428 ms
    11
    CPU times: user 135 ms, sys: 81.3 ms, total: 216 ms
    Wall time: 419 ms
    CPU times: user 147 ms, sys: 57.6 ms, total: 204 ms
    Wall time: 420 ms
    CPU times: user 130 ms, sys: 62 ms, total: 192 ms
    Wall time: 408 ms
    CPU times: user 146 ms, sys: 67.3 ms, total: 213 ms
    Wall time: 429 ms
    CPU times: user 158 ms, sys: 58.7 ms, total: 217 ms
    Wall time: 422 ms
    CPU times: user 167 ms, sys: 52.1 ms, total: 219 ms
    Wall time: 430 ms
    CPU times: user 146 ms, sys: 60.6 ms, total: 206 ms
    Wall time: 419 ms
    CPU times: user 141 ms, sys: 76.4 ms, total: 217 ms
    Wall time: 421 ms
    CPU times: user 163 ms, sys: 60.7 ms, total: 223 ms
    Wall time: 440 ms
    CPU times: user 121 ms, sys: 85.9 ms, total: 207 ms
    Wall time: 419 ms
    CPU times: user 153 ms, sys: 63.1 ms, total: 216 ms
    Wall time: 436 ms
    CPU times: user 129 ms, sys: 85.4 ms, total: 215 ms
    Wall time: 437 ms
    CPU times: user 158 ms, sys: 49.6 ms, total: 208 ms
    Wall time: 410 ms
    CPU times: user 154 ms, sys: 64.7 ms, total: 219 ms
    Wall time: 455 ms
    CPU times: user 152 ms, sys: 49.5 ms, total: 202 ms
    Wall time: 419 ms
    CPU times: user 127 ms, sys: 88.3 ms, total: 216 ms
    Wall time: 432 ms
    CPU times: user 125 ms, sys: 95 ms, total: 220 ms
    Wall time: 436 ms
    CPU times: user 154 ms, sys: 53.8 ms, total: 207 ms
    Wall time: 424 ms
    CPU times: user 119 ms, sys: 99.9 ms, total: 219 ms
    Wall time: 428 ms
    CPU times: user 147 ms, sys: 66.4 ms, total: 213 ms
    Wall time: 438 ms
    12
    CPU times: user 133 ms, sys: 77.1 ms, total: 210 ms
    Wall time: 437 ms
    CPU times: user 149 ms, sys: 74.1 ms, total: 224 ms
    Wall time: 434 ms
    CPU times: user 148 ms, sys: 71 ms, total: 219 ms
    Wall time: 439 ms
    CPU times: user 134 ms, sys: 85.1 ms, total: 219 ms
    Wall time: 432 ms
    CPU times: user 137 ms, sys: 76.5 ms, total: 214 ms
    Wall time: 423 ms
    CPU times: user 140 ms, sys: 58.6 ms, total: 198 ms
    Wall time: 425 ms
    CPU times: user 162 ms, sys: 57.4 ms, total: 219 ms
    Wall time: 429 ms
    CPU times: user 135 ms, sys: 65.2 ms, total: 201 ms
    Wall time: 423 ms
    CPU times: user 181 ms, sys: 47.7 ms, total: 228 ms
    Wall time: 636 ms
    CPU times: user 158 ms, sys: 57.6 ms, total: 215 ms
    Wall time: 431 ms
    CPU times: user 141 ms, sys: 78.8 ms, total: 220 ms
    Wall time: 422 ms
    CPU times: user 155 ms, sys: 62.7 ms, total: 218 ms
    Wall time: 442 ms
    CPU times: user 152 ms, sys: 64.6 ms, total: 217 ms
    Wall time: 431 ms
    CPU times: user 162 ms, sys: 62.6 ms, total: 225 ms
    Wall time: 441 ms
    CPU times: user 143 ms, sys: 71.1 ms, total: 215 ms
    Wall time: 427 ms
    CPU times: user 124 ms, sys: 62.2 ms, total: 186 ms
    Wall time: 405 ms
    CPU times: user 158 ms, sys: 60.7 ms, total: 218 ms
    Wall time: 432 ms
    CPU times: user 141 ms, sys: 75.9 ms, total: 217 ms
    Wall time: 439 ms
    CPU times: user 154 ms, sys: 66.7 ms, total: 220 ms
    Wall time: 433 ms
    CPU times: user 159 ms, sys: 62.6 ms, total: 222 ms
    Wall time: 433 ms
    13
    CPU times: user 174 ms, sys: 54.5 ms, total: 228 ms
    Wall time: 426 ms
    CPU times: user 161 ms, sys: 71.8 ms, total: 232 ms
    Wall time: 651 ms
    CPU times: user 140 ms, sys: 74 ms, total: 214 ms
    Wall time: 444 ms
    CPU times: user 141 ms, sys: 69.1 ms, total: 210 ms
    Wall time: 432 ms
    CPU times: user 150 ms, sys: 58.6 ms, total: 208 ms
    Wall time: 441 ms
    CPU times: user 144 ms, sys: 70.5 ms, total: 214 ms
    Wall time: 440 ms
    CPU times: user 144 ms, sys: 73.5 ms, total: 217 ms
    Wall time: 433 ms
    CPU times: user 135 ms, sys: 77.9 ms, total: 213 ms
    Wall time: 439 ms
    CPU times: user 151 ms, sys: 43.7 ms, total: 195 ms
    Wall time: 401 ms
    CPU times: user 147 ms, sys: 67.8 ms, total: 215 ms
    Wall time: 416 ms
    CPU times: user 148 ms, sys: 58.5 ms, total: 207 ms
    Wall time: 433 ms
    CPU times: user 109 ms, sys: 68.1 ms, total: 177 ms
    Wall time: 412 ms
    CPU times: user 135 ms, sys: 94.4 ms, total: 230 ms
    Wall time: 654 ms
    CPU times: user 146 ms, sys: 61.8 ms, total: 208 ms
    Wall time: 424 ms
    CPU times: user 149 ms, sys: 60.2 ms, total: 210 ms
    Wall time: 417 ms
    CPU times: user 137 ms, sys: 80.9 ms, total: 218 ms
    Wall time: 449 ms
    CPU times: user 161 ms, sys: 46.4 ms, total: 207 ms
    Wall time: 411 ms
    CPU times: user 135 ms, sys: 75.9 ms, total: 211 ms
    Wall time: 425 ms
    CPU times: user 119 ms, sys: 77.2 ms, total: 197 ms
    Wall time: 421 ms
    CPU times: user 145 ms, sys: 62.4 ms, total: 207 ms
    Wall time: 433 ms
    14
    CPU times: user 150 ms, sys: 61.1 ms, total: 211 ms
    Wall time: 421 ms
    CPU times: user 142 ms, sys: 79.1 ms, total: 221 ms
    Wall time: 422 ms
    CPU times: user 134 ms, sys: 75.3 ms, total: 209 ms
    Wall time: 437 ms
    CPU times: user 120 ms, sys: 86.3 ms, total: 207 ms
    Wall time: 419 ms
    CPU times: user 156 ms, sys: 57.3 ms, total: 214 ms
    Wall time: 427 ms
    CPU times: user 138 ms, sys: 91.3 ms, total: 229 ms
    Wall time: 636 ms
    CPU times: user 125 ms, sys: 89.9 ms, total: 215 ms
    Wall time: 421 ms
    CPU times: user 131 ms, sys: 83.7 ms, total: 214 ms
    Wall time: 426 ms
    CPU times: user 157 ms, sys: 50.7 ms, total: 208 ms
    Wall time: 417 ms
    CPU times: user 145 ms, sys: 70.9 ms, total: 215 ms
    Wall time: 436 ms
    CPU times: user 111 ms, sys: 101 ms, total: 211 ms
    Wall time: 423 ms
    CPU times: user 151 ms, sys: 67.2 ms, total: 218 ms
    Wall time: 431 ms
    CPU times: user 155 ms, sys: 56.5 ms, total: 212 ms
    Wall time: 430 ms
    CPU times: user 162 ms, sys: 55.6 ms, total: 218 ms
    Wall time: 439 ms
    CPU times: user 137 ms, sys: 61.5 ms, total: 198 ms
    Wall time: 412 ms
    CPU times: user 150 ms, sys: 52.8 ms, total: 203 ms
    Wall time: 419 ms
    CPU times: user 141 ms, sys: 78.4 ms, total: 219 ms
    Wall time: 440 ms
    CPU times: user 126 ms, sys: 55.8 ms, total: 182 ms
    Wall time: 399 ms
    CPU times: user 70 ms, sys: 43.4 ms, total: 113 ms
    Wall time: 339 ms
    CPU times: user 144 ms, sys: 54.1 ms, total: 198 ms
    Wall time: 410 ms
    15
    CPU times: user 138 ms, sys: 75.2 ms, total: 213 ms
    Wall time: 417 ms
    CPU times: user 168 ms, sys: 39.7 ms, total: 208 ms
    Wall time: 421 ms
    CPU times: user 141 ms, sys: 65.6 ms, total: 206 ms
    Wall time: 417 ms
    CPU times: user 123 ms, sys: 65.5 ms, total: 189 ms
    Wall time: 399 ms
    CPU times: user 131 ms, sys: 77.7 ms, total: 209 ms
    Wall time: 418 ms
    CPU times: user 135 ms, sys: 81.2 ms, total: 216 ms
    Wall time: 425 ms
    CPU times: user 133 ms, sys: 78.7 ms, total: 212 ms
    Wall time: 430 ms
    CPU times: user 158 ms, sys: 60.1 ms, total: 218 ms
    Wall time: 426 ms
    CPU times: user 148 ms, sys: 58.1 ms, total: 206 ms
    Wall time: 434 ms
    CPU times: user 142 ms, sys: 63.4 ms, total: 205 ms
    Wall time: 415 ms
    CPU times: user 172 ms, sys: 42.9 ms, total: 215 ms
    Wall time: 432 ms
    CPU times: user 153 ms, sys: 66.1 ms, total: 219 ms
    Wall time: 428 ms
    CPU times: user 141 ms, sys: 61 ms, total: 202 ms
    Wall time: 406 ms
    CPU times: user 148 ms, sys: 44.8 ms, total: 193 ms
    Wall time: 430 ms
    CPU times: user 166 ms, sys: 49 ms, total: 215 ms
    Wall time: 426 ms
    CPU times: user 143 ms, sys: 71.1 ms, total: 214 ms
    Wall time: 443 ms
    CPU times: user 163 ms, sys: 54 ms, total: 217 ms
    Wall time: 428 ms
    CPU times: user 153 ms, sys: 51 ms, total: 204 ms
    Wall time: 438 ms
    CPU times: user 108 ms, sys: 90.3 ms, total: 198 ms
    Wall time: 420 ms
    CPU times: user 136 ms, sys: 78.4 ms, total: 214 ms
    Wall time: 448 ms
    16
    CPU times: user 150 ms, sys: 58.3 ms, total: 208 ms
    Wall time: 431 ms
    CPU times: user 153 ms, sys: 60 ms, total: 213 ms
    Wall time: 432 ms
    CPU times: user 153 ms, sys: 60.6 ms, total: 214 ms
    Wall time: 431 ms
    CPU times: user 138 ms, sys: 84.9 ms, total: 223 ms
    Wall time: 434 ms
    CPU times: user 149 ms, sys: 69.6 ms, total: 219 ms
    Wall time: 429 ms
    CPU times: user 140 ms, sys: 68.9 ms, total: 209 ms
    Wall time: 432 ms
    CPU times: user 157 ms, sys: 57.5 ms, total: 214 ms
    Wall time: 421 ms
    CPU times: user 152 ms, sys: 57.4 ms, total: 210 ms
    Wall time: 429 ms
    CPU times: user 146 ms, sys: 37.9 ms, total: 184 ms
    Wall time: 384 ms
    CPU times: user 111 ms, sys: 50.3 ms, total: 162 ms
    Wall time: 398 ms
    CPU times: user 165 ms, sys: 50.5 ms, total: 215 ms
    Wall time: 432 ms
    CPU times: user 148 ms, sys: 61.9 ms, total: 210 ms
    Wall time: 438 ms
    CPU times: user 157 ms, sys: 57.9 ms, total: 215 ms
    Wall time: 438 ms
    CPU times: user 136 ms, sys: 72.1 ms, total: 208 ms
    Wall time: 421 ms
    CPU times: user 151 ms, sys: 61.1 ms, total: 212 ms
    Wall time: 423 ms
    CPU times: user 158 ms, sys: 63 ms, total: 221 ms
    Wall time: 444 ms
    CPU times: user 128 ms, sys: 73.7 ms, total: 201 ms
    Wall time: 419 ms
    CPU times: user 147 ms, sys: 66.5 ms, total: 214 ms
    Wall time: 446 ms
    CPU times: user 128 ms, sys: 87.7 ms, total: 216 ms
    Wall time: 436 ms
    CPU times: user 145 ms, sys: 71.2 ms, total: 216 ms
    Wall time: 416 ms
    17
    CPU times: user 147 ms, sys: 61.6 ms, total: 209 ms
    Wall time: 428 ms
    CPU times: user 155 ms, sys: 59.2 ms, total: 214 ms
    Wall time: 417 ms
    CPU times: user 153 ms, sys: 60.7 ms, total: 214 ms
    Wall time: 426 ms
    CPU times: user 156 ms, sys: 57.7 ms, total: 214 ms
    Wall time: 417 ms
    CPU times: user 146 ms, sys: 68.1 ms, total: 214 ms
    Wall time: 439 ms
    CPU times: user 150 ms, sys: 75.9 ms, total: 226 ms
    Wall time: 662 ms
    CPU times: user 160 ms, sys: 48.6 ms, total: 208 ms
    Wall time: 428 ms
    CPU times: user 156 ms, sys: 44 ms, total: 200 ms
    Wall time: 419 ms
    CPU times: user 147 ms, sys: 68.5 ms, total: 215 ms
    Wall time: 438 ms
    CPU times: user 157 ms, sys: 53.3 ms, total: 211 ms
    Wall time: 429 ms
    CPU times: user 153 ms, sys: 56.3 ms, total: 209 ms
    Wall time: 432 ms
    CPU times: user 170 ms, sys: 51 ms, total: 221 ms
    Wall time: 430 ms
    CPU times: user 164 ms, sys: 44 ms, total: 208 ms
    Wall time: 422 ms
    CPU times: user 160 ms, sys: 52.2 ms, total: 212 ms
    Wall time: 429 ms
    CPU times: user 130 ms, sys: 30.2 ms, total: 161 ms
    Wall time: 399 ms
    CPU times: user 139 ms, sys: 51.3 ms, total: 191 ms
    Wall time: 399 ms
    CPU times: user 141 ms, sys: 72.2 ms, total: 213 ms
    Wall time: 427 ms
    CPU times: user 128 ms, sys: 91.6 ms, total: 220 ms
    Wall time: 430 ms
    CPU times: user 185 ms, sys: 40.8 ms, total: 226 ms
    Wall time: 469 ms
    CPU times: user 146 ms, sys: 70.1 ms, total: 216 ms
    Wall time: 452 ms
    18
    CPU times: user 151 ms, sys: 56.7 ms, total: 207 ms
    Wall time: 424 ms
    CPU times: user 147 ms, sys: 65.7 ms, total: 213 ms
    Wall time: 434 ms
    CPU times: user 155 ms, sys: 60.9 ms, total: 216 ms
    Wall time: 427 ms
    CPU times: user 128 ms, sys: 61.8 ms, total: 190 ms
    Wall time: 420 ms
    CPU times: user 131 ms, sys: 79.9 ms, total: 210 ms
    Wall time: 408 ms
    CPU times: user 149 ms, sys: 68.6 ms, total: 218 ms
    Wall time: 434 ms
    CPU times: user 162 ms, sys: 62 ms, total: 224 ms
    Wall time: 430 ms
    CPU times: user 147 ms, sys: 65.6 ms, total: 213 ms
    Wall time: 424 ms
    CPU times: user 140 ms, sys: 76 ms, total: 216 ms
    Wall time: 434 ms
    CPU times: user 172 ms, sys: 32.9 ms, total: 205 ms
    Wall time: 411 ms
    CPU times: user 139 ms, sys: 66.3 ms, total: 206 ms
    Wall time: 434 ms
    CPU times: user 145 ms, sys: 61.1 ms, total: 206 ms
    Wall time: 420 ms
    CPU times: user 158 ms, sys: 59.7 ms, total: 217 ms
    Wall time: 437 ms
    CPU times: user 152 ms, sys: 59.5 ms, total: 212 ms
    Wall time: 420 ms
    CPU times: user 160 ms, sys: 48.1 ms, total: 208 ms
    Wall time: 419 ms
    CPU times: user 149 ms, sys: 58.5 ms, total: 207 ms
    Wall time: 462 ms
    CPU times: user 142 ms, sys: 57.7 ms, total: 200 ms
    Wall time: 423 ms
    CPU times: user 157 ms, sys: 53 ms, total: 210 ms
    Wall time: 451 ms
    CPU times: user 147 ms, sys: 49.4 ms, total: 197 ms
    Wall time: 416 ms
    CPU times: user 154 ms, sys: 66.6 ms, total: 221 ms
    Wall time: 448 ms
    19
    CPU times: user 129 ms, sys: 81.9 ms, total: 211 ms
    Wall time: 440 ms
    CPU times: user 153 ms, sys: 51.8 ms, total: 205 ms
    Wall time: 420 ms
    CPU times: user 180 ms, sys: 37.9 ms, total: 218 ms
    Wall time: 436 ms
    CPU times: user 165 ms, sys: 57.6 ms, total: 223 ms
    Wall time: 427 ms
    CPU times: user 130 ms, sys: 85.6 ms, total: 216 ms
    Wall time: 430 ms
    CPU times: user 146 ms, sys: 63.1 ms, total: 209 ms
    Wall time: 415 ms
    CPU times: user 167 ms, sys: 56.1 ms, total: 224 ms
    Wall time: 641 ms
    CPU times: user 159 ms, sys: 51.5 ms, total: 210 ms
    Wall time: 425 ms
    CPU times: user 155 ms, sys: 64.9 ms, total: 220 ms
    Wall time: 425 ms
    CPU times: user 123 ms, sys: 91.2 ms, total: 215 ms
    Wall time: 438 ms
    CPU times: user 156 ms, sys: 48.3 ms, total: 205 ms
    Wall time: 418 ms
    CPU times: user 143 ms, sys: 63.7 ms, total: 206 ms
    Wall time: 438 ms
    CPU times: user 129 ms, sys: 79.4 ms, total: 208 ms
    Wall time: 420 ms
    CPU times: user 138 ms, sys: 65.8 ms, total: 204 ms
    Wall time: 428 ms
    CPU times: user 142 ms, sys: 69.5 ms, total: 211 ms
    Wall time: 431 ms
    CPU times: user 144 ms, sys: 60.5 ms, total: 204 ms
    Wall time: 426 ms
    CPU times: user 141 ms, sys: 76.7 ms, total: 218 ms
    Wall time: 440 ms
    CPU times: user 147 ms, sys: 59.1 ms, total: 206 ms
    Wall time: 427 ms
    CPU times: user 160 ms, sys: 55.2 ms, total: 215 ms
    Wall time: 437 ms
    CPU times: user 149 ms, sys: 62.9 ms, total: 212 ms
    Wall time: 441 ms
    CPU times: user 58.2 s, sys: 25.9 s, total: 1min 24s
    Wall time: 3min 46s


.. code:: ipython3

    print(data.shape)


.. parsed-literal::

    (365, 20, 20)

