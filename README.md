# Process MOLLI and shMOLLI data

Reads a directory of shMOLLI DICOM images and processes the data to produce a look-locker corrected T1 map. Negative values are cropped to 0.

Two possible methods for processing the data are available.

1. Fast (default). Uses some numerical methods to solve exponential equations of the correct form. May be slightly less accurate, but significantly faster.

2. Slow. Uses scipy curve fitting algorithm to fit the exponential curve. More accurate, but much slower.

The difference between the two methods is very little as demonstrated in the figure below.

![fast_slow comparison](fast_slow.tif "Comparison of fast and slow fitting methods")

Any pixels/voxels where the max value is less than 100 is skipped. NB: For this version, data is processed top-left to bottom-right in the image. As images are often empty around the edges, this means the the processing is 'fast' to start with as each pixel is basically skipped, then slows down as the true data is processed, then speeds up again at the end.

## Usage

As module
```python
> pip3 install sh_molli
> process_sh_molli_series.py -i <inputfolder> -o <outputfilename> -p <plot_flag> -m <method>
```

In code
```python
> python3
> import sh_molli.sh_molli as sh
> im = sh.process_folder(dir,method='fast')
```

-i - input folder must be a path containing DICOM images only Can process data based on 'Inversion Time' being stored in dcm.TriggerTime, dcm.InversionTime and dcm.ImageComments

-o - output file name. Uses PIL for image writing, so supports all formats that PIL understands. Recommended using example.tiff to ensure that large values are not cropped

-p - plot flat (1, 0 or not present). If 1, the image will be displayed using matplotlib once the data is processed. Colorbar is cropped to 0-2000 range, sensible values for human tissue.

-m - method. ('fast' or 'slow'). See above.