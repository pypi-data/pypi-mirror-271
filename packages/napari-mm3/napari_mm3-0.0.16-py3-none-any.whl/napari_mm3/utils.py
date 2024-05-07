from __future__ import print_function, division
from functools import wraps
import numpy as np
import pandas as pd
import six
import json
from scipy import ndimage as ndi
from skimage import filters, morphology
from skimage.filters import median
from pathlib import Path
import warnings
import scipy.io as sio
import tifffile as tiff

TIFF_FILE_FORMAT_PEAK = "%s_xy%03d_p%04d_%s.tif"
TIFF_FILE_FORMAT_NO_PEAK = "%s_xy%03d_%s.tif"


def load_tiff_stack_simple(dir: Path, prefix, fov, postfix, peak=None):
    """Load a tiff stack from a directory.
    Parameters
    ----------
    dir : Path
        Directory containing the tiff stack.
    prefix : str
        Prefix of the tiff stack.
    fov : int
        FOV number.
    postfix : str
        Postfix of the tiff stack.
    peak : int, optional
        Peak number. If None, the tiff stack is assumed to be a single channel.
    Returns
    -------
    np.ndarray
        The tiff stack.
    """
    filename = TIFF_FILE_FORMAT_NO_PEAK % (prefix, fov, postfix)
    if peak:
        filename = TIFF_FILE_FORMAT_PEAK % (prefix, fov, peak, postfix)

    with tiff.TiffFile(dir / filename) as tif:
        return tif.asarray()


# functions and classes for reading / writing .json files

# numpy dtypes are not json serializable - need to convert
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def write_cells_to_json(Cells, path_out):
    json_out = {}
    for cell_id, cell in Cells.items():
        json_out[cell_id] = vars(cell)
        try:
            json_out[cell_id].pop("time_table")
        except:
            pass
    with open(path_out, "w") as fout:
        json.dump(json_out, fout, sort_keys=True, indent=2, cls=NpEncoder)


def write_cells_to_matlab(cells, path_out):
    # TODO: make this run when we want.
    for cell_id in cells:
        cell = cells[cell_id]
        new_cell = {k: v for k, v in vars(cell).items() if v is not None}
        new_cell = cell_from_dict(new_cell)
        cells[cell_id] = new_cell
    with open(path_out, "wb") as f:
        sio.savemat(f, cells)


def cell_from_dict(in_dict):
    """Helper function for json deserialization.
    Turns a dictionary from a serialized cell object to a 'cell' object.
    """
    # initializing pxl2um to None disables the Cell constructor.
    # Then we manually override each field with json-derived cell parameters
    cell = Cell(
        pxl2um=None, time_table=None, cell_id=None, region=None, t=None, parent_id=None
    )
    for key, val in in_dict.items():
        vars(cell)[key] = val
    return cell


def read_cells_from_json(path_in):
    """
    Read in a json file of cell data and return a dictionary of Cell objects.

    Parameters
    ----------
    path_in : str
        Path to json file.

    Returns
    -------
    Cells_new : dict
        Dictionary of Cell objects.
    """
    with open(path_in, "r") as fin:
        json_loaded = json.load(fin)
    cells_new = {}
    for cell_id, cell in json_loaded.items():
        cells_new[cell_id] = cell_from_dict(cell)
    return Cells(cells_new)


### Cell class and related functions

# this is the object that holds all information for a cell
class Cell:
    """
    The Cell class is one cell that has been born. It is not neccesarily a cell that
    has divided.

    When cells are made during lineage creation, the information is stored per cell in
    an object called Cell. The Cell object is the fundamental unit of data produced by
    mm3. Every Cell object has a unique identifier (`id`) as well as all the other
    pertinent information. The default data format save by the track widget is a dictionary
    of these cell objecs, where the keys are each cell id and the values are the object
    itself. Below is a description of the information contained in a Cell object and how
    to export it to other formats.

    For an overview on classes in Python see [here](https://learnpythonthehardway.org/book/ex40.html).

    ## Cell object attributes

    The following is a list of the attributes of a Cell.

    #### Standard attributes
    * `Cell.id` : The cell id is a string in the form `f0p0t0r0` which represents the FOV,
        channel peak number, time point the cell came from as well as which segmented region
        it is in that image.
    * `Cell.fov` : FOV the cell came from.
    * `Cell.peak` : Channel peak number the cell came from.
    * `Cell.birth_label` : The segmented region number the cell was born at. The regions are
        numbered from the closed end of the channel, so mother cells should have a birth label of 1.
    * `Cell.parent` : This cell's mother cell's id.
    * `Cell.daughters` : A list of the ids of this cell's two daughter cells.
    * `Cell.birth_time` : Nominal time point at time of birth.
    * `Cell.division_time` : Nominal division time of cell. Note that this is equal to
        the birth time of the daughters.
    * `Cell.times` : A list of time points for which this cell grew. Includes the first
        time point but does not include the last time point. It is the same length as
        the following attributes, but it may not be sequential because of dropped segmentations.
    * `Cell.labels` : The segmented region labels over time.
    * `Cell.bboxes` : The bounding boxes of each region in the segmented channel image over time.
    * `Cell.areas` : The areas of the segmented regions over time in pixels^2.
    * `Cell.orientations`: The angle between the cell's major axis and the positive x axis
        (within [pi/2, -pi/2]) over time.
    * `Cell.centroids`: The y and x positions (in that order) in pixels of the centroid of the cell over time.
    * `Cell.lengths` : The long axis length in pixels of the regions over time.
    * `Cell.widths` : The long axis width in pixels of the regions over time.
    * `Cell.times_w_div` : Same as Cell.times but includes the division time.
    * `Cell.lengths_w_div` : The long axis length in microns of the regions over time,
        including the division length.
    * `Cell.sb` : Birth length of cell in microns.
    * `Cell.sd` : Division length of cell in microns. The division length is the combined birth
        length of the daugthers.
    * `Cell.delta` : Cell.sd - Cell.sb. Simply for convenience.
    * `Cell.tau` : Nominal generation time of the cell.
    * `Cell.elong_rate` : Elongation rate of the cell using a linear fit of the log lengths.
    * `Cell.septum_position` : The birth length of the first daughter (closer to closed end)
        divided by the division length.

    #### Fluorescence attributes:
    * `Cell.fl_tots`: Total integrated fluorescence per time point. The plane which was
        analyzed is appended to the attribute name, so that e.g. Cell.fl_tots_c1
        represents the integrated fluorescence from the cell in plane c1.
    * `Cell.fl_area_avgs`: Mean fluorescence per pixel by timepoint. The plane which was analyzed
        is appended to the attribute name, e.g. as Cell.fl_area_avgs_c1.
    * `Cell.fl_vol_avgs`: Mean fluorescence per cell volume. The plane which was analyzed
        is appended to the attribute name, e.g. as Cell.fl_vol_avgs_c1.

    #### Foci tracking attributes:
    * `Cell.disp_l`: Displacement on long axis in pixels of each focus from the center
        of the cell, by time point. (1D np.array)
    * `Cell.disp_w`: Displacement on short axis in pixels of each focus from the center
        of the cell, by time point. (1D np.array)
    * `Cell.foci_h`: Focus "height." Sum of the intensity of the gaussian fitting
        area, by time point. (1D np.array)
    """

    # initialize (birth) the cell
    def __init__(self, pxl2um, time_table, cell_id, region, t, parent_id=None):
        """The cell must be given a unique cell_id and passed the region
        information from the segmentation

        Parameters
        __________

        cell_id : str
            cell_id is a string in the form fXpXtXrX
            f is 3 digit FOV number
            p is 4 digit peak number
            t is 4 digit time point at time of birth
            r is region label for that segmentation
            Use the function create_cell_id to return a proper string.

        region : region properties object
            Information about the labeled region from
            skimage.measure.regionprops()

        parent_id : str
            id of the parent if there is one.
        """
        # Hack for json deserialization -- there's probably a better way to do this.
        if pxl2um is None:
            return

        # create all the attributes
        # id
        self.id = cell_id

        self.pxl2um = pxl2um
        self.time_table = time_table

        # identification convenience
        self.fov = int(cell_id.split("f")[1].split("p")[0])
        self.peak = int(cell_id.split("p")[1].split("t")[0])
        self.birth_label = int(cell_id.split("r")[1])

        # parent id may be none
        self.parent = parent_id

        # daughters is updated when cell divides
        # if this is none then the cell did not divide
        self.daughters = None

        # birth and division time
        self.birth_time = t
        self.division_time = None  # filled out if cell divides

        # the following information is on a per timepoint basis
        self.times = [t]
        self.abs_times = [time_table[self.fov][t]]  # elapsed time in seconds
        self.labels = [region.label]
        self.bboxes = [region.bbox]
        self.areas = [region.area]

        # calculating cell length and width by using Feret Diamter. These values are in pixels
        length_tmp, width_tmp = feretdiameter(region)
        if length_tmp is None:
            print("feretdiameter() failed for " + self.id + " at t=" + str(t) + ".")
        self.lengths = [length_tmp]
        self.widths = [width_tmp]

        # calculate cell volume as cylinder plus hemispherical ends (sphere). Unit is px^3
        self.volumes = [
            (length_tmp - width_tmp) * np.pi * (width_tmp / 2) ** 2
            + (4 / 3) * np.pi * (width_tmp / 2) ** 3
        ]

        # angle of the fit elipsoid and centroid location
        if region.orientation > 0:
            self.orientations = [-(np.pi / 2 - region.orientation)]
        else:
            self.orientations = [np.pi / 2 + region.orientation]

        self.centroids = [region.centroid]

        # these are special datatype, as they include information from the daugthers for division
        # computed upon division
        self.times_w_div = None
        self.lengths_w_div = None
        self.widths_w_div = None

        # this information is the "production" information that
        # we want to extract at the end. Some of this is for convenience.
        # This is only filled out if a cell divides.
        self.sb = None  # in um
        self.sd = None  # this should be combined lengths of daughters, in um
        self.delta = None
        self.tau = None
        self.elong_rate = None
        self.septum_position = None
        self.width = None

    def grow(self, time_table, region, t):
        """Append data from a region to this cell.
        use cell.times[-1] to get most current value"""

        self.times.append(t)
        # TODO: Switch time_table to be passed in directly.
        self.abs_times.append(time_table[self.fov][t])
        self.labels.append(region.label)
        self.bboxes.append(region.bbox)
        self.areas.append(region.area)

        # calculating cell length and width by using Feret Diamter
        length_tmp, width_tmp = feretdiameter(region)
        if length_tmp is None:
            print("feretdiameter() failed for " + self.id + " at t=" + str(t) + ".")
        self.lengths.append(length_tmp)
        self.widths.append(width_tmp)
        self.volumes.append(
            (length_tmp - width_tmp) * np.pi * (width_tmp / 2) ** 2
            + (4 / 3) * np.pi * (width_tmp / 2) ** 3
        )

        if region.orientation > 0:
            ori = -(np.pi / 2 - region.orientation)
        else:
            ori = np.pi / 2 + region.orientation

        self.orientations.append(ori)
        self.centroids.append(region.centroid)

    def divide(self, daughter1, daughter2, t):
        """Divide the cell and update stats.
        daugther1 and daugther2 are instances of the Cell class.
        daughter1 is the daugther closer to the closed end."""

        # put the daugther ids into the cell
        self.daughters = [daughter1.id, daughter2.id]

        # give this guy a division time
        self.division_time = daughter1.birth_time

        # update times
        self.times_w_div = self.times + [self.division_time]
        self.abs_times.append(self.time_table[self.fov][self.division_time])

        # flesh out the stats for this cell
        # size at birth
        self.sb = self.lengths[0] * self.pxl2um

        # force the division length to be the combined lengths of the daughters
        self.sd = (daughter1.lengths[0] + daughter2.lengths[0]) * self.pxl2um

        # delta is here for convenience
        self.delta = self.sd - self.sb

        # generation time. Use more accurate times and convert to minutes
        self.tau = np.float64((self.abs_times[-1] - self.abs_times[0]) / 60.0)

        # include the data points from the daughters
        self.lengths_w_div = [l * self.pxl2um for l in self.lengths] + [self.sd]
        self.widths_w_div = [w * self.pxl2um for w in self.widths] + [
            ((daughter1.widths[0] + daughter2.widths[0]) / 2) * self.pxl2um
        ]

        # volumes for all timepoints, in um^3
        self.volumes_w_div = []
        for i in range(len(self.lengths_w_div)):
            self.volumes_w_div.append(
                (self.lengths_w_div[i] - self.widths_w_div[i])
                * np.pi
                * (self.widths_w_div[i] / 2) ** 2
                + (4 / 3) * np.pi * (self.widths_w_div[i] / 2) ** 3
            )

        # calculate elongation rate.

        try:
            times = np.float64((np.array(self.abs_times) - self.abs_times[0]) / 60.0)
            log_lengths = np.float64(np.log(self.lengths_w_div))
            p = np.polyfit(times, log_lengths, 1)  # this wants float64
            self.elong_rate = p[0] * 60.0  # convert to hours

        except:
            self.elong_rate = np.float64("NaN")
            print("Elongation rate calculate failed for {}.".format(self.id))

        # calculate the septum position as a number between 0 and 1
        # which indicates the size of daughter closer to the closed end
        # compared to the total size
        self.septum_position = daughter1.lengths[0] / (
            daughter1.lengths[0] + daughter2.lengths[0]
        )

        # calculate single width over cell's life
        self.width = np.mean(self.widths_w_div)

        # convert data to smaller floats. No need for float64
        # see https://docs.scipy.org/doc/numpy-1.13.0/user/basics.types.html
        convert_to = "float16"  # numpy datatype to convert to

        self.sb = self.sb.astype(convert_to)
        self.sd = self.sd.astype(convert_to)
        self.delta = self.delta.astype(convert_to)
        self.elong_rate = self.elong_rate.astype(convert_to)
        self.tau = self.tau.astype(convert_to)
        self.septum_position = self.septum_position.astype(convert_to)
        self.width = self.width.astype(convert_to)

        self.lengths = [length.astype(convert_to) for length in self.lengths]
        self.lengths_w_div = [
            length.astype(convert_to) for length in self.lengths_w_div
        ]
        self.widths = [width.astype(convert_to) for width in self.widths]
        self.widths_w_div = [width.astype(convert_to) for width in self.widths_w_div]
        self.volumes = [vol.astype(convert_to) for vol in self.volumes]
        self.volumes_w_div = [vol.astype(convert_to) for vol in self.volumes_w_div]
        # note the float16 is hardcoded here
        self.orientations = [
            np.float16(orientation) for orientation in self.orientations
        ]
        self.centroids = [
            (y.astype(convert_to), x.astype(convert_to)) for y, x in self.centroids
        ]

    def place_in_cell(self, x, y, t):
        """Translates from screen-space to in-cell coordinates."""
        # check if our cell exists at the current timestamp.
        if not (t in self.times):
            return None, None, None

        cell_time = self.times.index(t)
        bbox = self.bboxes[cell_time]
        # check that the point is inside the cell's bounding box.
        if not ((bbox[0] < y) & (y < bbox[2]) & (bbox[1] < x) & (x < bbox[3])):
            return None, None, None

        centroid = self.centroids[cell_time]
        orientation = self.orientations[cell_time]
        dx = x - centroid[1]
        dy = y - centroid[0]
        if orientation < 0:
            orientation = np.pi + orientation
        disp_y = dy * np.sin(orientation) - dx * np.cos(orientation)
        disp_x = dy * np.cos(orientation) + dx * np.sin(orientation)

        return disp_y, disp_x, cell_time

    def print_info(self):
        """prints information about the cell"""
        print("id = %s" % self.id)
        print("times = {}".format(", ".join("{}".format(t) for t in self.times)))
        print(
            "lengths = {}".format(", ".join("{:.2f}".format(l) for l in self.lengths))
        )


# obtains cell length and width of the cell using the feret diameter
def feretdiameter(region):
    """
    feretdiameter calculates the length and width of the binary region shape. The cell orientation
    from the ellipsoid is used to find the major and minor axis of the cell.
    See https://en.wikipedia.org/wiki/Feret_diameter.

    Parameters
    ----------
    region : skimage.measure._regionprops._RegionProperties
        regionprops object of the binary region of the cell

    Returns
    -------
    length : float
        length of the cell
    width : float
        width of the cell
    """

    # y: along vertical axis of the image; x: along horizontal axis of the image;
    # calculate the relative centroid in the bounding box (non-rotated)
    # print(region.centroid)
    y0, x0 = region.centroid
    y0 = y0 - np.int16(region.bbox[0]) + 1
    x0 = x0 - np.int16(region.bbox[1]) + 1

    # orientation is now measured in RC coordinates - quick fix to convert
    # back to xy
    if region.orientation > 0:
        ori1 = -np.pi / 2 + region.orientation
    else:
        ori1 = np.pi / 2 + region.orientation
    cosorient = np.cos(ori1)
    sinorient = np.sin(ori1)

    amp_param = (
        1.2  # amplifying number to make sure the axis is longer than actual cell length
    )

    # coordinates relative to bounding box
    # r_coords = region.coords - [np.int16(region.bbox[0]), np.int16(region.bbox[1])]

    # limit to perimeter coords. pixels are relative to bounding box
    region_binimg = np.pad(
        region.image, 1, "constant"
    )  # pad region binary image by 1 to avoid boundary non-zero pixels
    distance_image = ndi.distance_transform_edt(region_binimg)
    r_coords = np.where(distance_image == 1)
    r_coords = list(zip(r_coords[0], r_coords[1]))

    # coordinates are already sorted by y. partion into top and bottom to search faster later
    # if orientation > 0, L1 is closer to top of image (lower Y coord)
    if (ori1) > 0:
        L1_coords = r_coords[: int(np.round(len(r_coords) / 4))]
        L2_coords = r_coords[int(np.round(len(r_coords) / 4)) :]
    else:
        L1_coords = r_coords[int(np.round(len(r_coords) / 4)) :]
        L2_coords = r_coords[: int(np.round(len(r_coords) / 4))]

    #####################
    # calculte cell length
    L1_pt = np.zeros((2, 1))
    L2_pt = np.zeros((2, 1))

    # define the two end points of the the long axis line
    # one pole.
    L1_pt[1] = x0 + cosorient * 0.5 * region.major_axis_length * amp_param
    L1_pt[0] = y0 - sinorient * 0.5 * region.major_axis_length * amp_param

    # the other pole.
    L2_pt[1] = x0 - cosorient * 0.5 * region.major_axis_length * amp_param
    L2_pt[0] = y0 + sinorient * 0.5 * region.major_axis_length * amp_param

    # calculate the minimal distance between the points at both ends of 3 lines
    # aka calcule the closest coordiante in the region to each of the above points.
    # pt_L1 = r_coords[np.argmin([np.sqrt(np.power(Pt[0]-L1_pt[0],2) + np.power(Pt[1]-L1_pt[1],2)) for Pt in r_coords])]
    # pt_L2 = r_coords[np.argmin([np.sqrt(np.power(Pt[0]-L2_pt[0],2) + np.power(Pt[1]-L2_pt[1],2)) for Pt in r_coords])]

    try:
        pt_L1 = L1_coords[
            np.argmin(
                [
                    np.sqrt(
                        np.power(Pt[0] - L1_pt[0], 2) + np.power(Pt[1] - L1_pt[1], 2)
                    )
                    for Pt in L1_coords
                ]
            )
        ]
        pt_L2 = L2_coords[
            np.argmin(
                [
                    np.sqrt(
                        np.power(Pt[0] - L2_pt[0], 2) + np.power(Pt[1] - L2_pt[1], 2)
                    )
                    for Pt in L2_coords
                ]
            )
        ]
        length = np.sqrt(
            np.power(pt_L1[0] - pt_L2[0], 2) + np.power(pt_L1[1] - pt_L2[1], 2)
        )
    except:
        length = None

    #####################
    # calculate cell width
    # draw 2 parallel lines along the short axis line spaced by 0.8*quarter of length = 0.4, to avoid  in midcell

    # limit to points in each half
    W_coords = []
    if (ori1) > 0:
        W_coords.append(
            r_coords[: int(np.round(len(r_coords) / 2))]
        )  # note the /2 here instead of /4
        W_coords.append(r_coords[int(np.round(len(r_coords) / 2)):])
    else:
        W_coords.append(r_coords[int(np.round(len(r_coords) / 2)):])
        W_coords.append(r_coords[: int(np.round(len(r_coords) / 2))])

    # starting points
    x1 = x0 + cosorient * 0.5 * length * 0.4
    y1 = y0 - sinorient * 0.5 * length * 0.4
    x2 = x0 - cosorient * 0.5 * length * 0.4
    y2 = y0 + sinorient * 0.5 * length * 0.4
    W1_pts = np.zeros((2, 2))
    W2_pts = np.zeros((2, 2))

    # now find the ends of the lines
    # one side
    W1_pts[0, 1] = x1 - sinorient * 0.5 * region.minor_axis_length * amp_param
    W1_pts[0, 0] = y1 - cosorient * 0.5 * region.minor_axis_length * amp_param
    W1_pts[1, 1] = x2 - sinorient * 0.5 * region.minor_axis_length * amp_param
    W1_pts[1, 0] = y2 - cosorient * 0.5 * region.minor_axis_length * amp_param

    # the other side
    W2_pts[0, 1] = x1 + sinorient * 0.5 * region.minor_axis_length * amp_param
    W2_pts[0, 0] = y1 + cosorient * 0.5 * region.minor_axis_length * amp_param
    W2_pts[1, 1] = x2 + sinorient * 0.5 * region.minor_axis_length * amp_param
    W2_pts[1, 0] = y2 + cosorient * 0.5 * region.minor_axis_length * amp_param

    # calculate the minimal distance between the points at both ends of 3 lines
    pt_W1 = np.zeros((2, 2))
    pt_W2 = np.zeros((2, 2))
    d_W = np.zeros((2, 1))
    i = 0
    for W1_pt, W2_pt in zip(W1_pts, W2_pts):

        # # find the points closest to the guide points
        # pt_W1[i,0], pt_W1[i,1] = r_coords[np.argmin([np.sqrt(np.power(Pt[0]-W1_pt[0],2) + np.power(Pt[1]-W1_pt[1],2)) for Pt in r_coords])]
        # pt_W2[i,0], pt_W2[i,1] = r_coords[np.argmin([np.sqrt(np.power(Pt[0]-W2_pt[0],2) + np.power(Pt[1]-W2_pt[1],2)) for Pt in r_coords])]

        # find the points closest to the guide points
        pt_W1[i, 0], pt_W1[i, 1] = W_coords[i][
            np.argmin(
                [
                    np.sqrt(
                        np.power(Pt[0] - W1_pt[0], 2) + np.power(Pt[1] - W1_pt[1], 2)
                    )
                    for Pt in W_coords[i]
                ]
            )
        ]
        pt_W2[i, 0], pt_W2[i, 1] = W_coords[i][
            np.argmin(
                [
                    np.sqrt(
                        np.power(Pt[0] - W2_pt[0], 2) + np.power(Pt[1] - W2_pt[1], 2)
                    )
                    for Pt in W_coords[i]
                ]
            )
        ]

        # calculate the actual width
        d_W[i] = np.sqrt(
            np.power(pt_W1[i, 0] - pt_W2[i, 0], 2)
            + np.power(pt_W1[i, 1] - pt_W2[i, 1], 2)
        )
        i += 1

    # take the average of the two at quarter positions
    width = np.mean([d_W[0], d_W[1]])
    return length, width


# take info and make string for cell id
def create_focus_id(region, t, peak, fov, experiment_name=None):
    """Make a unique focus id string for a new focus"""
    if experiment_name is None:
        focus_id = "f{:0=2}p{:0=4}t{:0=4}r{:0=2}".format(fov, peak, t, region.label)
    else:
        focus_id = "{}f{:0=2}p{:0=4}t{:0=4}r{:0=2}".format(
            experiment_name, fov, peak, t, region.label
        )
    return focus_id


# function for a growing cell, used to calculate growth rate
def cell_growth_func(t, sb, elong_rate):
    """
    Assumes you have taken log of the data.
    It also allows the size at birth to be a free parameter, rather than fixed
    at the actual size at birth (but still uses that as a guess)
    Assumes natural log, not base 2 (though I think that makes less sense)

    old form: sb*2**(alpha*t)
    """
    return sb + elong_rate * t


# functions for pruning a dictionary of cells

class Cells(dict):
    def __init__(self, dict_):
        super().__init__(dict_)


def cellsmethod(func):
    """Decorator to dynamically add a given function as a method to 'Cells'"""

    @wraps(func)  # Copies the docstring, etc, from 'func' to 'wrapper'
    def wrapper(self, *args, **kwargs):
        return Cells(func(self, *args, **kwargs))

    # Add 'wrapper' to Cells
    setattr(Cells, func.__name__, wrapper)
    return func  # returning func means func can still be used normally


# find cells with both a mother and two daughters
@cellsmethod
def find_complete_cells(cells):
    """Go through a dictionary of cells and return another dictionary
    that contains just those with a parent and daughters"""

    Complete_cells = {}

    for cell_id in cells:
        if cells[cell_id].daughters and cells[cell_id].parent:
            Complete_cells[cell_id] = cells[cell_id]

    return Complete_cells


# finds cells whose birth label is 1
@cellsmethod
def find_mother_cells(cells):
    """Return only cells whose starting region label is 1."""

    Mother_cells = {}

    for cell_id in cells:
        if cells[cell_id].birth_label == 1:
            Mother_cells[cell_id] = cells[cell_id]

    return Mother_cells


@cellsmethod
def filter_cells(cells, attr, val, idx=None, debug=False) -> Cells:
    """Return only cells whose designated attribute equals "val"."""

    Filtered_cells = {}

    for cell_id, cell in cells.items():

        at_val = getattr(cell, attr)
        if debug:
            print(at_val)
            print("Times: ", cell.times)
        if idx is not None:
            at_val = at_val[idx]
        if at_val == val:
            Filtered_cells[cell_id] = cell

    return Filtered_cells


@cellsmethod
def filter_cells_containing_val_in_attr(cells, attr, val) -> Cells:
    """Return only cells that have val in list attribute, attr."""

    Filtered_cells = {}

    for cell_id, cell in cells.items():

        at_list = getattr(cell, attr)
        if val in at_list:
            Filtered_cells[cell_id] = cell

    return Filtered_cells


@cellsmethod
def find_cells_of_birth_label(cells, label_num=1) -> Cells:
    """Return only cells whose starting region label is given.
    If no birth_label is given, returns the mother cells.
    label_num can also be a list to include cells of many birth labels
    """

    fcells = {}  # f is for filtered

    if type(label_num) is int:
        label_num = [label_num]

    for cell_id in cells:
        if cells[cell_id].birth_label in label_num:
            fcells[cell_id] = cells[cell_id]

    return fcells


@cellsmethod
def organize_cells_by_channel(cells, specs) -> dict:
    """
    Returns a nested dictionary where the keys are first
    the fov_id and then the peak_id (similar to specs),
    and the final value is a dictiary of cell objects that go in that
    specific channel, in the same format as normal {cell_id : Cell, ...}
    """

    # make a nested dictionary that holds lists of cells for one fov/peak
    cells_by_peak = {}
    for fov_id in specs.keys():
        cells_by_peak[fov_id] = {}
        for peak_id, spec in specs[fov_id].items():
            # only make a space for channels that are analyized
            if spec == 1:
                cells_by_peak[fov_id][peak_id] = {}

    # organize the cells
    for cell_id, cell in cells.items():
        cells_by_peak[cell.fov][cell.peak][cell_id] = cell

    # remove peaks and that do not contain cells
    remove_fovs = []
    for fov_id, peaks in cells_by_peak.items():
        remove_peaks = []
        for peak_id in peaks.keys():
            if not peaks[peak_id]:
                remove_peaks.append(peak_id)

        for peak_id in remove_peaks:
            peaks.pop(peak_id)

        if not cells_by_peak[fov_id]:
            remove_fovs.append(fov_id)

    for fov_id in remove_fovs:
        cells_by_peak.pop(fov_id)

    return cells_by_peak


@cellsmethod
def gen_label_to_cell_mapping(cells, specs) -> dict:
    """
    Generates a map from (fov, peak, time, label) -> cell_id
    """
    fov_cells = organize_cells_by_channel(cells, specs)
    cell_map = {}
    for fov_id, peaks in fov_cells.items():
        cell_map[fov_id] = {}
        for peak_id, peak in peaks.items():
            new_peak = {}
            for cell_id, cell in peak.items():
                for time_idx, time in enumerate(cell.times):
                    if time not in new_peak:
                        new_peak[time] = {}
                    new_peak[time][cell.labels[time_idx]] = cell.id
            cell_map[fov_id][peak_id] = new_peak
    return cell_map


@cellsmethod
def infer_cell_id(cells: Cells, xloc, yloc, t):
    """
    Given screen-space coordinates and timestamp of a point, this finds the
    cell that point belongs to.
    Returns:
      cell_id: id of the cell the point is inside of.
      disp_y, disp_x: The cell-space displacement of the point.
      cell_time: the cell-time of the point
    """
    cell: Cell
    for cell_id, cell in cells.items():
        disp_y, disp_x, cell_time = cell.place_in_cell(xloc, yloc, t)
        if disp_y is None:
            continue
        return cell_id, disp_y, disp_x, cell_time
    return None, None, None, None


@cellsmethod
def find_screenspace_foci(cells: Cells):
    """
    From a list of cells, gets the absolute screen-space position of all foci.
    Returns:
      x_pts: List of foci x-positions
      y_pts: List of foci y-positions.
      times (int): List of times associated with above foci.
    """
    x_pts = []
    y_pts = []
    times = []
    cell: Cell
    for cell_id, cell in cells.items():
        # get conversion from cell to 'real' time
        for i, time in enumerate(cell.times):
            orientation = cell.orientations[i]
            centroid = cell.centroids[i]
            x_locs = cell.disp_w[i]
            y_locs = cell.disp_l[i]

            data_x_locs = []
            data_y_locs = []
            for x, y in zip(x_locs, y_locs):
                # convert from cell to pixel space.
                if orientation < 0:
                    orientation = np.pi + orientation

                dy = y * np.sin(orientation) + x * np.cos(orientation)
                dx = -y * np.cos(orientation) + x * np.sin(orientation)

                xloc = dx + centroid[1]
                yloc = dy + centroid[0]
                data_x_locs.append(xloc)
                data_y_locs.append(yloc)

            x_pts.extend(data_x_locs)
            y_pts.extend(data_y_locs)
            times.extend(len(data_x_locs) * [time])

    return np.array(x_pts), np.array(y_pts), np.array(times)


@cellsmethod
def find_all_cell_intensities(
    cells,
    intensity_directory,
    seg_directory,
    specs,
    channel_name="sub_c2",
    apply_background_correction=True,
):
    """
    Finds fluorescenct information for cells. All the cells in cells
    should be from one fov/peak.
    """

    # iterate over each fov in specs
    for fov_id, fov_peaks in specs.items():

        # iterate over each peak in fov
        for peak_id, peak_value in fov_peaks.items():

            # if peak_id's value is not 1, go to next peak
            if peak_value != 1:
                continue

            print(
                "Quantifying channel {} fluorescence in cells in fov {}, peak {}.".format(
                    channel_name, fov_id, peak_id
                )
            )
            # Load fluorescent images and segmented images for this channel
            fl_stack = load_tiff_stack_simple(
                intensity_directory, fov=fov_id, peak=peak_id, postfix=channel_name
            )
            corrected_stack = np.zeros(fl_stack.shape)

            for frame in range(fl_stack.shape[0]):
                # median filter will be applied to every image
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    median_filtered = median(
                        fl_stack[frame, ...], selem=morphology.disk(1)
                    )

                # subtract the gaussian-filtered image from true image to correct
                #   uneven background fluorescence
                if apply_background_correction:
                    blurred = filters.gaussian(
                        median_filtered, sigma=10, preserve_range=True
                    )
                    corrected_stack[frame, :, :] = median_filtered - blurred
                else:
                    corrected_stack[frame, :, :] = median_filtered

            seg_stack = load_tiff_stack_simple(
                seg_directory, fov=fov_id, peak=peak_id, postfix=channel_name
            )

            # evaluate whether each cell is in this fov/peak combination
            for _, cell in cells.items():

                cell_fov = cell.fov
                if cell_fov != fov_id:
                    continue

                cell_peak = cell.peak
                if cell_peak != peak_id:
                    continue

                cell_times = cell.times
                cell_labels = cell.labels
                cell.area_mean_fluorescence[channel_name] = []
                cell.volume_mean_fluorescence[channel_name] = []
                cell.total_fluorescence[channel_name] = []

                # loop through cell's times
                for i, t in enumerate(cell_times):
                    frame = t - 1
                    cell_label = cell_labels[i]

                    total_fluor = np.sum(
                        corrected_stack[frame, seg_stack[frame, :, :] == cell_label]
                    )

                    cell.area_mean_fluorescence[channel_name].append(
                        total_fluor / cell.areas[i]
                    )
                    cell.volume_mean_fluorescence[channel_name].append(
                        total_fluor / cell.volumes[i]
                    )
                    cell.total_fluorescence[channel_name].append(total_fluor)

    # The cell objects in the original dictionary will be updated,
    # no need to return anything specifically.


@cellsmethod
def find_cells_of_fov_and_peak(cells, fov_id, peak_id) -> Cells:
    """Return only cells from a specific fov/peak
    Parameters
    ----------
    fov_id : int corresponding to FOV
    peak_id : int correstonging to peak
    """

    fcells = {}  # f is for filtered

    for cell_id in cells:
        if cells[cell_id].fov == fov_id and cells[cell_id].peak == peak_id:
            fcells[cell_id] = cells[cell_id]

    return fcells


# TODO: List of ALL cell properties
@cellsmethod
def cells2df(
    cells,
    columns=[
        "fov",
        "peak",
        "birth_label",
        "birth_time",
        "division_time",
        "sb",
        "sd",
        "width",
        "delta",
        "tau",
        "elong_rate",
        "septum_position",
    ],
) -> pd.DataFrame:
    """
    Take cell data (a dicionary of Cell objects) and return a dataframe.

    rescale : boolean
        If rescale is set to True, then the 6 major parameters are rescaled by their mean.
    """
    # Make dataframe for plotting variables
    cells_dict = {cell_id: vars(cell) for cell_id, cell in cells.items()}
    df = pd.DataFrame(
        cells_dict
    ).transpose()  # must be transposed so data is in columns
    df = df.sort_values(by=["fov", "peak", "birth_time", "birth_label"])
    df = df[columns].apply(pd.to_numeric)
    return df


def find_last_daughter(cell, Cells):
    """Finds the last daughter in a lineage starting with a earlier cell.
    Helper function for find_continuous_lineages"""

    # go into the daugther cell if the daughter exists
    if cell.daughters[0] in Cells:
        cell = Cells[cell.daughters[0]]
        cell = find_last_daughter(cell, Cells)
    else:
        # otherwise just give back this cell
        return cell

    # finally, return the deepest cell
    return cell


def find_cells_born_after(cells, born_after=None):
    """
    Returns Cells dictionary of cells with a birth_time after the value specified
    """

    if born_after is None:
        return cells

    return {
        cell_id: cell
        for cell_id, cell in six.iteritems(cells)
        if cell.birth_time >= born_after
    }


def lineages_to_dict(lineages):
    """Converts the lineage structure of cells organized by peak back
    to a dictionary of cells. Useful for filtering but then using the
    dictionary based plotting functions"""

    Cells = {}

    for fov, peaks in six.iteritems(lineages):
        for peak, cells in six.iteritems(peaks):
            Cells.update(cells)

    return Cells


def find_continuous_lineages(cells, specs, t1=0, t2=1000):
    """
    Uses a recursive function to only return cells that have continuous
    lineages between two time points. Takes a "lineage" form of Cells and
    returns a dictionary of the same format. Good for plotting
    with saw_tooth_plot()
    t1 : int
        First cell in lineage must be born before this time point
    t2 : int
        Last cell in lineage must be born after this time point
    """

    Lineages = organize_cells_by_channel(cells, specs)

    # This is a mirror of the lineages dictionary, just for the continuous cells
    Continuous_Lineages = {}

    for fov, peaks in six.iteritems(Lineages):
        # print("fov = {:d}".format(fov))
        # Create a dictionary to hold this FOV
        Continuous_Lineages[fov] = {}

        for peak, cells in six.iteritems(peaks):
            # print("{:<4s}peak = {:d}".format("",peak))
            # sort the cells by time in a list for this peak
            cells_sorted = [(cell_id, cell) for cell_id, cell in six.iteritems(cells)]
            cells_sorted = sorted(cells_sorted, key=lambda x: x[1].birth_time)

            # Sometimes there are not any cells for the channel even if it was to be analyzed
            if not cells_sorted:
                continue

            # look through list to find the cell born immediately before t1
            # and divides after t1, but not after t2
            for i, cell_data in enumerate(cells_sorted):
                cell_id, cell = cell_data
                if cell.birth_time < t1 and t1 <= cell.division_time < t2:
                    first_cell_index = i
                    break

            # filter cell_sorted or skip if you got to the end of the list
            if i == len(cells_sorted) - 1:
                continue
            else:
                cells_sorted = cells_sorted[i:]

            # get the first cell and it's last contiguous daughter
            first_cell = cells_sorted[0][1]
            last_daughter = find_last_daughter(first_cell, cells)

            # check to the daughter makes the second cut off
            if last_daughter.birth_time > t2:
                # print(fov, peak, 'Made it')

                # now retrieve only those cells within the two times
                # use the function to easily return in dictionary format
                cells_cont = find_cells_born_after(cells, born_after=t1)
                # Cells_cont = find_cells_born_before(Cells_cont, born_before=t2)

                # append the first cell which was filtered out in the above step
                cells_cont[first_cell.id] = first_cell

                # and add it to the big dictionary
                Continuous_Lineages[fov][peak] = cells_cont

        # remove keys that do not have any lineages
        if not Continuous_Lineages[fov]:
            Continuous_Lineages.pop(fov)

    cells = lineages_to_dict(Continuous_Lineages)  # revert back to return

    return cells
