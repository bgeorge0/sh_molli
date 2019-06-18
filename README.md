# Process MOLLI and shMOLLI data

Reads a directory of shMOLLI DICOM images and processes the data to produce a look-locker corrected T1 map. Negative values are cropped to 0.

## Usage

As module
```python
> pip3 install sh_molli
> process_sh_molli_series.py -i <inputfolder> -o <outputfilename> -p <plot_flag>
```

In code
```python
> python3
> import sh_molli.sh_molli as sh
> im = sh.process_folder(dir)
```

-i - input folder must be a path containing DICOM images only Can process data based on 'Inversion Time' being stored in dcm.TriggerTime, dcm.InversionTime and dcm.ImageComments

-o - output file name. Uses PIL for image writing, so supports all formats that PIL understands. Recommended using example.tiff to ensure that large values are not cropped

-p - plot flat (1, 0 or not present). If 1, the image will be displayed using matplotlib once the data is processed. Colorbar is cropped to 0-2000 range, sensible values for human tissue.