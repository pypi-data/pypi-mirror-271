# Guide to folders and files

mm3 creates many folders and files in your experimental directory during the course of processing. This page enumerates and explains those items. (Explicitly, this explains the way your experimental and analyzed data is organized by mm3, not how the folders and files are organized in the mm3 repository).

The paths of the folders and subfolders should be defined in your parameters.yaml file, though most of the scripts will make the folders for you if you have not already. Be very sure that you put in the right names, as the easiest bugs to get when processing images are path errors!

## Experimental Directory

`/full/path/to/experimental/directory/`

Defined in the parameters.yaml file as experimental_directory. Type the whole path in quotes. This is main folder where all subfolders should go that contain raw images, analysis, and movies. Good practice is to begin this folder name with yyyymmdd.

### Image Directory

This folder should contain all your TIFF images, but you should keep .nd2 files in the experimental directory.

TIFF files have a specific naming scheme:

`experiment_name_t0000xy00.tif` or `experiment_name_t0000xy00c0.tif`

The file postfix `t0000xy00c0.tif`, with information about the time point `t`, the FOV number `xy` and the color channel `c`, if there is more than one imaging method per time point, are particularly important. mm3 scripts expect this format when searching and retrieving metadata from image files.

### Analysis Directory

`/experimental_directory/analysis/`

This is where most metadata and processed images go that are accumulated during processing. This includes:
* TIFF_metadata.pkl and .txt : Python dictionary of metadata associated with each TIFF file. Created by Compile.
* channel_masks.pkl and .txt : Python dictionary that records the location of the channels in each FOV. Is a nested dictionaries of FOVs and then channel peaks. The final values are 4 pixel coordinates, ((y1, y2), (x1, x2)). Created by Compile.
* time_table.pkl and .txt : Python dictionary that maps the nominal time point per FOV to the actual elapsed time in seconds each picture was taken.
* crosscorrs.pkl and .txt : Python dictionary that contains image correlation value for channels over time. Used to guess if a channel is full or empty. Same structure as channel_masks. Created by Compile.
* specs.pkl and .txt : Python dictionary which is the specifications of channels as full (1), empty (0), or ignore (-1). Same structure as channel_masks. Created by ChannelPicker.

The .txt files are simply a convenience provided for checking the metadata. If you want to manually edit the metadata you must open the .pkl files in a Python session, change them, and resave them.

The analysis directory also contains subfolders which contain analyzed data. This includes both the image stacks and the final curated cell data. These folders are created by the various scripts and do not need to be initialized beforehand.

#### Channel stacks

`/experimental_directory/analysis/channels/`

Contains the sliced and stacked channel information as created by Compile. Each stack is for a single channel for a single color plane for all time points. They are named with the following scheme:

`experiment_name_xy000_p0000_c1.tif`

Where `experiment_name` is from the parameters file. `xy` is the 3 digit FOV number, `p` is the four digit peak ID (channel ID) and `c` is the single digit color plane. FOV number and color plane are 1 indexed, and the peak ID comes from the X pixel location of the channel midline in the original TIFF images.

#### Averaged empty channels

`/experimental_directory/analysis/empties/`

Contains the averaged empty channel templates, as created by ChannelPicker, to be used during subtraction. There should be one empty channel stack per FOV. Uses the naming convention:

`experimental_name_xy000_empty_c1.tif`

#### Subtracted

`/experimental_directory/analysis/subtracted/`

Contains the subtracted phase contrast images as created by mm3_Subtract.py. Uses the naming convention:

`experimental_name_xy000_p0000_sub_c1.tif`

#### Segmented

`/experimental_directory/analysis/segmented/`

Contains the segmented images as created by Subtract. Uses the naming convention:

`experimental_name_xy000_p0000_seg.tif`

#### Lineages

`/experimental_directory/analysis/lineages/`

This optional folder is created if you want to create lineage images after segmentation and lineage finding. These images show how the cells grow and are connected to each other over time. Useful for debugging segmentation.

`experimental_name_xy000_p0000_lin.png`

#### Cell data

`/experimental_directory/analysis/cell_data/`

This folder contains the final, curated cell data after segmentation and lineage creation.

#### HDF5

`/experimental_directory/analysis/hdf5/`

If in your parameters file you elected to output the image stacks as HDF5 files rather than TIFF stacks, this file will contain all your image data as well as additional metadata. There will be one HDF5 file for each FOV, which contains raw, empty, subtracted, and segmented images for all channels in that FOV.
