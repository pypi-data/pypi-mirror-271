# -*- coding: utf-8 -*-
import itertools
import os
import sys
import traceback
import numpy as np
import pandas
import pandas as pd
from pyrsktools import RSK
import gsw
import matplotlib.pyplot as plt
import statsmodels.api
from matplotlib.ticker import ScalarFormatter
from tabulate import tabulate

class CTDError(Exception):
    """Exception raised for CTD related errors.

    Attributes:
        filename -- input dataset which caused the error
        message -- explanation of the error
    """
    def __init__(self, filename, message=" Unknown, check to make sure your mastersheet is in your current directory."):
        self.filename = filename
        self.message = message
        super().__init__(self.message)

class CTDFjorder:
    """
    CTDFjorder
    ==========

    CTDFjorder class for processing and analyzing CTD data.

    This class provides methods for reading RSK files, processing CTD data,
    calculating derived quantities, and generating plots.

    :var master_sheet_path: Path to the master sheet Excel file.

    Usage
    ------

    To run the default processing pipeline::

        CTDFjorder.run_default()

    Author
    -------

    Nikolas Yanek-Chrones

    Date
    -----

    May 1, 2024
    """
    master_sheet_path = None

    @staticmethod
    def run_default(plot=False):
        filesys = CTDFjorder._Filesystem()
        filesys.reset_file_environment()
        CTDFjorder.master_sheet_path = os.path.join(CTDFjorder._Filesystem.get_cwd(), "FjordPhyto MASTER SHEET.xlsx")
        rsk_files_list = CTDFjorder._Filesystem.get_rsk_files_in_working_directory(filesys.get_cwd())
        for file in rsk_files_list:
            try:
                my_data = CTDFjorder.CTD(file)
                my_data.add_filename_to_table()
                my_data.save_to_csv("output.csv")
                my_data.add_location_to_table()
                my_data.remove_non_positive_samples()
                my_data.run_complex_cleaner("practicalsalinity", 'salinitydiff')
                my_data.add_absolute_salinity()
                my_data.add_density()
                my_data.add_overturns()
                my_data.add_mld(0)
                my_data.add_mld(10)
                my_data.save_to_csv("outputclean.csv")
                if plot:
                    my_data.plot_depth_density_salinity_mld_scatter()
                    my_data.plot_depth_temperature_scatter()
                    my_data.plot_depth_salinity_density_mld_line()
            except Exception as e:
                print(f"Error processing file: '{file}' {e}")
                continue

    @staticmethod
    def merge_all_in_folder():
        filesys = CTDFjorder._Filesystem()
        CTDFjorder.master_sheet_path = os.path.join(CTDFjorder._Filesystem.get_cwd(), "FjordPhyto MASTER SHEET.xlsx")
        rsk_files_list = CTDFjorder._Filesystem.get_rsk_files_in_working_directory(filesys.get_cwd())
        for file in rsk_files_list:
            try:
                my_data = CTDFjorder.CTD(file)
                my_data.add_filename_to_table()
                my_data.add_location_to_table()
                my_data.save_to_csv("output.csv")
            except Exception as e:
                print(e)
                continue

    class _Filesystem:
        """
        _Filesystem
        -----------
        
        Utility class for file system operations.
        """

        @staticmethod
        def get_rsk_files_in_working_directory(working_directory):
            rsk_files_list = []
            rsk_filenames_no_path = []
            for filename in os.listdir(working_directory):
                if filename.endswith('.rsk'):
                    for filepath in rsk_files_list:
                        filename_no_path = ('_'.join(filepath.split("/")[-1].split("_")[0:3]).split('.rsk')[0])
                        if filename_no_path in rsk_filenames_no_path:
                            continue
                        rsk_filenames_no_path.append(filename_no_path)
                    file_path = os.path.join(working_directory, filename)
                    rsk_files_list.append(file_path)
            return rsk_files_list

        @staticmethod
        def get_cwd():
            working_directory_path = None
            # determine if application is a script file or frozen exe
            if getattr(sys, 'frozen', False):
                working_directory_path = os.path.dirname(sys.executable)
            elif __file__:
                working_directory_path = os.getcwd()
            else:
                working_directory_path = os.getcwd()
            return working_directory_path

        @staticmethod
        def get_filename(filepath):
            return '_'.join(filepath.split("/")[-1].split("_")[0:3]).split('.rsk')[0]

        @staticmethod
        def reset_file_environment():
            CTDFjorder.master_sheet_path = os.path.join(CTDFjorder._Filesystem.get_cwd(), "FjordPhyto MASTER SHEET.xlsx")
            output_file_csv = "output.csv"
            output_file_csv_clean = "output_clean.csv"
            output_plots_dir = "plots"
            cwd = CTDFjorder.CTD.get_cwd()
            CTDFjorder.master_sheet_path = os.path.join(cwd, CTDFjorder.master_sheet_path)
            output_file_csv = os.path.join(cwd, output_file_csv)
            output_file_csv_clean = os.path.join(cwd, output_file_csv_clean)
            if cwd is None:
                raise CTDError("", "Couldn't get working directory.")
            if os.path.isfile(output_file_csv):
                os.remove(output_file_csv)
            if os.path.isfile(output_file_csv_clean):
                os.remove(output_file_csv_clean)
            if os.path.isdir("./plots.gif"):
                os.remove("./plots/gif")
            if not os.path.isdir("./plots"):
                os.mkdir("./plots")
            if not os.path.isdir("./plots/gif"):
                os.mkdir("./plots/gif")

    class CTD():
        """
        CTD
        ---
        
        Class representing a CTD object for processing and analyzing CTD data.
        
        :var _ctd_array: DataFrame containing CTD data.
        :var _rsk: RSK object for reading RSK files.
        :var _filename: Filename of the RSK file.
        :var _utils: Utility object for CTD data processing.
        :var _calculator: Calculator object for CTD data calculations.
        :var _plotter: Placeholder for plotter object.
        :var _cwd: Current working directory.
        """
        _ctd_array = pandas.DataFrame()
        _rsk = None
        _filename = None
        _utils = None
        _calculator = None
        _plotter = None
        _cwd = None
        _NO_SAMPLES_ERROR = "No samples in file."
        _NO_LOCATION_ERROR = "No location could be found."
        _DENSITY_CALCULATION_ERROR = "Could not calculate density on this dataset."
        _SALINITYABS_CALCULATION_ERROR = "Could not calculate density on this dataset."
        _DATA_CLEANING_ERROR = "No data remains after data cleaning, reverting to previous CTD"
        _REMOVE_NEGATIVES_ERROR = "No data remains after removing non-positive samples."
        _MLD_ERROR = "No data remains after calculating MLD."

        def __init__(self, rskfilepath):
            """
            Initialize a new CTD object.

            :param rskfilepath: The file path to the RSK file.
            """
            self._rsk = RSK(rskfilepath)
            self._filename = ('_'.join(rskfilepath.split("/")[-1].split("_")[0:3]).split(".rsk")[0])
            print("New CTDFjorder Object Created from : " + self._filename)
            self._ctd_array = np.array(self._rsk.npsamples())
            self._ctd_array = pd.DataFrame(self._ctd_array)
            self._utils = self._Utility(self._filename, )
            self._calculator = self._Calculate
            self._cwd = self.get_cwd()

        @staticmethod
        def get_cwd():
            working_directory_path = None
            # determine if application is a script file or frozen exe
            if getattr(sys, 'frozen', False):
                working_directory_path = os.path.dirname(sys.executable)
            elif __file__:
                working_directory_path = os.getcwd()
            else:
                working_directory_path = os.getcwd()
            return working_directory_path

        def view_table(self):
            """
            Print the CTD data table.
            """
            print(tabulate(self._ctd_array, headers='keys', tablefmt='psql'))

        def add_filename_to_table(self):
            """
            Add the filename to the CTD data table.
            """
            self._ctd_array.assign(filename=self._filename)

        def add_location_to_table(self):
            """
            Add latitude and longitude information to the CTD data table.

            Retrieves the sample location data from the RSK file and adds it to the CTD data table.
            If no location data is found, it attempts to estimate the location using the master sheet.
            """
            self._ctd_array = self._utils.remove_sample_timezone_indicator(self._ctd_array)
            location_data = self._utils.get_sample_location(self._rsk, self._filename)
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._NO_SAMPLES_ERROR)
            try:
                self._ctd_array = self._ctd_array.assign(latitude=location_data[0],
                                                         longitude=location_data[1])
            except Exception:
                self._ctd_array.loc['latitude'] = None
                self._ctd_array.loc['longitude'] = None
                self._ctd_array.loc['filename'] = None
                raise CTDError(self._filename, self._NO_LOCATION_ERROR)

        def remove_non_positive_samples(self):
            """
            Remove samples with non-positive depth, pressure, salinity, absolute salinity, or density.

            Iterates through the columns of the CTD data table and removes rows with non-positive values
            for depth, pressure, salinity, absolute salinity, or density.
            """
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._NO_SAMPLES_ERROR)
            for column in self._ctd_array.columns:
                match column:
                    case 'depth_00':
                        self._ctd_array = self._utils.remove_rows_with_negative_depth(self._ctd_array)
                    case 'pressure_00':
                        self._ctd_array = self._utils.remove_rows_with_negative_pressure(self._ctd_array)
                    case 'salinity_00':
                        self._ctd_array = self._utils.remove_rows_with_negative_salinity(self._ctd_array)
                    case 'salinityabs':
                        self._ctd_array = self._utils.remove_rows_with_negative_salinityabs(self._ctd_array)
                    case 'density':
                        self._ctd_array = self._utils.remove_rows_with_negative_density(self._ctd_array)
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._REMOVE_NEGATIVES_ERROR)

        def run_complex_cleaner(self, feature, method='salinitydiff'):
            """
            Run complex data cleaning methods on the specified feature.

            :param feature: The feature to clean (e.g., 'practicalsalinity').
            :param method: The cleaning method to apply (default: 'salinitydiff').

            Applies complex data cleaning methods to the specified feature based on the selected method.
            Currently supports cleaning practical salinity using the 'salinitydiff' method.
            """
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._NO_SAMPLES_ERROR)
            supported_features = {
                "practicalsalinity": "salinity_00"
            }
            supported_methods = {
                "salinitydiff": self._calculator.calculate_and_drop_salinity_spikes(self._ctd_array)
            }
            if feature in supported_features.keys():
                if method in supported_methods.keys():
                    self._ctd_array.loc[self._ctd_array.index, 'salinity_00'] = supported_methods[method]
                else:
                    print(f"run_complex_cleaner: Invalid method \"{method}\" not in {supported_methods.keys()}")
            else:
                print(f"run_complex_cleaner: Invalid feature \"{feature}\" not in {supported_features.keys()}.")
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._DATA_CLEANING_ERROR)

        def add_absolute_salinity(self):
            """
            Calculate and add absolute salinity to the CTD data table.

            Calculates the absolute salinity using the TEOS-10 equations and adds it as a new column
            to the CTD data table. Removes rows with negative absolute salinity values.
            """
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._NO_SAMPLES_ERROR)
            self._ctd_array.loc[self._ctd_array.index, 'salinityabs'] = self._calculator.calculate_absolute_salinity(
                self._ctd_array)
            self._ctd_array = self._utils.remove_rows_with_negative_salinityabs(self._ctd_array)
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._SALINITYABS_CALCULATION_ERROR)

        def add_density(self):
            """
            Calculate and add density to the CTD data table.

            Calculates the density using the TEOS-10 equations and adds it as a new column to the CTD
            data table. If absolute salinity is not present, it is calculated first.
            """
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._NO_SAMPLES_ERROR)
            if 'salinityabs' in self._ctd_array.columns:
                self._ctd_array.loc[self._ctd_array.index, 'density'] = self._calculator.calculate_absolute_density(
                    self._ctd_array)
            else:
                self._ctd_array.loc[self._ctd_array.index, 'salinityabs'] = self.add_absolute_salinity()
                self._ctd_array = self._calculator.calculate_absolute_density(self._ctd_array)
                self._ctd_array.loc[self._ctd_array.index, 'density'] = self._calculator.calculate_absolute_density(
                    self._ctd_array)
                self._ctd_array.drop('salinityabs')
                if self._utils.no_values_in_object(self._ctd_array):
                    raise CTDError(self._filename, self._DENSITY_CALCULATION_ERROR)

        def add_overturns(self):
            """
            Identify and add density overturns to the CTD data table.

            Calculates density changes between consecutive measurements and identifies overturns where
            denser water lies above less dense water. Adds an 'overturn' column to the CTD data table.
            """
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._NO_SAMPLES_ERROR)
            self._ctd_array = self._calculator.calculate_overturns(self._ctd_array.copy())

        def addMeanSurfaceDensity(self):
            """
            Calculate and add mean surface density to the CTD data table.

            Calculates the mean surface density from the density values and adds it as a new column
            to the CTD data table.
            """
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._NO_SAMPLES_ERROR)
            mean_surface_density = self._calculator.calculate_mean_surface_density(self._ctd_array.copy())
            self._ctd_array = self._ctd_array.assign(mean_surface_density=mean_surface_density)

        def add_mld(self, reference, method="default"):
            """
            Calculate and add mixed layer depth (MLD) to the CTD data table.

            :param reference: The reference depth for MLD calculation.
            :param method: The MLD calculation method (default: "default").

            Calculates the mixed layer depth using the specified method and reference depth.
            Adds the MLD and the actual reference depth used as new columns to the CTD data table.
            """
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._NO_SAMPLES_ERROR)
            copy_ctd_array = self._ctd_array.copy()
            supported_methods = [
                "default"
            ]
            unpack = None

            if method == "default":
                unpack = self._calculator.calculate_mld(copy_ctd_array['density'], copy_ctd_array['depth_00'],
                                                        reference)
            else:
                print(f"add_mld: Invalid method \"{method}\" not in {supported_methods}")
                unpack = [None, None]
            if unpack is None:
                unpack = [None, None]
                raise CTDError("MLD could not be calculated.")
            MLD = unpack[0]
            depth_used_as_reference = unpack[1]
            self._ctd_array.loc[self._ctd_array.index, f'MLD {reference}'] = MLD
            self._ctd_array.loc[
                self._ctd_array.index, f'MLD {reference} Actual Reference Depth'] = depth_used_as_reference
            self._ctd_array = copy_ctd_array.merge(self._ctd_array)
            if self._utils.no_values_in_object(self._ctd_array):
                raise CTDError(self._filename, self._MLD_ERROR)

        def save_to_csv(self, output_file):
            """
            Save the CTD data table to a CSV file.

            :param output_file: The output CSV file path.

            Renames the columns of the CTD data table based on a predefined mapping and saves the
            data to the specified CSV file. If the file already exists, the data is appended to it.
            """
            rsk_labels = {
                "temperature_00": "Temperature (°C)",
                "pressure_00": "Pressure (dbar)",
                "chlorophyll_00": "Chlorophyll a (µg/l)",
                "seapressure_00": "Sea Pressure (dbar)",
                "depth_00": "Depth (m)",
                "salinity_00": "Salinity (PSU)",
                "speedofsound_00": "Speed of Sound (m/s)",
                "specificconductivity_00": "Specific Conductivity (µS/cm)",
                "conductivity_00": "Conductivity (mS/cm)",
                "density": "Density (kg/m^3) Derived",
                "salinityabs": "Absolute Salinity (g/kg) Derived",
                "MLD_Zero": "MLD Zero (m) Derived",
                "MLD_Ten": "MLD Ten (m) Derived",
                "stratification": "Stratification (J/m^2) Derived",
                "mean_surface_density": "Mean Surface Density (kg/m^3) Derived",
                "overturn": "Overturn (Δρ < -0.05)"
            }
            # Renaming columns
            data = self._ctd_array.copy()
            if 'filename' in data.columns:
                data = data[[col for col in data.columns if col != 'filename'] + ['filename']]
            if 'density_change' in data.columns:
                data = data.drop('density_change', axis=1)
                data.reset_index(inplace=True, drop=True)
            for key, new_column_name in rsk_labels.items():
                if key in data.columns:
                    data = data.rename(columns={key: new_column_name})
            try:
                csv_df = pd.read_csv(str(output_file))
            except FileNotFoundError:
                print(f"Error: The file {output_file} does not exist. A new file will be created.")
                csv_df = pd.DataFrame()  # If file does not exist, create an empty DataFrame

            # Merge the existing DataFrame with the new DataFrame
            merged_df = pd.concat([csv_df, data], ignore_index=True)

            # Overwrite the original CSV file with the merged DataFrame
            merged_df.to_csv(output_file, index=False)

            return merged_df

        # =============================================================================
        # Section: Plotting Functions
        # =============================================================================
        def plot_depth_salinity_density_mld_line(self):
            """
            Plot depth vs. salinity and density with MLD lines using LOESS smoothing.

            Generates a plot of depth vs. salinity and density, applying LOESS smoothing to the data.
            Adds horizontal lines indicating the mixed layer depth (MLD) at different reference depths.
            Saves the plot as an image file.
            """
            df = self._ctd_array.copy()
            filename = self._filename
            plt.rcParams.update({'font.size': 16})
            df_filtered = df
            if df_filtered.isnull().values.any():
                df_filtered.dropna(inplace=True)  # Drop rows with NaNs
            df_filtered = df_filtered.reset_index(drop=True)
            if len(df_filtered) < 1:
                return
            fig, ax1 = plt.subplots(figsize=(18, 18))
            ax1.invert_yaxis()
            # Dynamically set y-axis limits based on depth data
            max_depth = df_filtered['depth_00'].max()
            ax1.set_ylim([max_depth, 0])  # Assuming depth increases downwards
            lowess = statsmodels.api.nonparametric.lowess
            salinity_lowess = lowess(df_filtered['salinity_00'], df_filtered['depth_00'], frac=0.1)
            salinity_depths, salinity_smooth = zip(*salinity_lowess)
            color_salinity = 'tab:blue'
            ax1.plot(salinity_smooth, salinity_depths, color=color_salinity, label='Practical Salinity')
            ax1.set_xlabel('Practical Salinity (PSU)', color=color_salinity)
            ax1.set_ylabel('Depth (m)')
            ax1.tick_params(axis='x', labelcolor=color_salinity)
            density_lowess = lowess(df_filtered['density'], df_filtered['depth_00'], frac=0.1)
            density_depths, density_smooth = zip(*density_lowess)
            ax2 = ax1.twiny()
            color_density = 'tab:red'
            ax2.plot(density_smooth, density_depths, color=color_density, label='Density (kg/m^3)')
            ax2.set_xlabel('Density (kg/m^3)', color=color_density)
            ax2.tick_params(axis='x', labelcolor=color_density)
            ax2.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
            mld_cols = []
            for col in df.columns:
                if 'MLD' in col and 'Actual' not in col:
                    mld_cols.append(df[col])
            refdepth_cols = []
            for col in df.columns:
                if 'Actual' in col:
                    refdepth_cols.append(df[col])
            for idx, mld_col in enumerate(mld_cols):
                ax1.axhline(y=mld_col.iloc[0], color='green', linestyle='--',
                            label=f'MLD {refdepth_cols[idx].iloc[0]} Ref')
                ax1.text(0.95, mld_col.iloc[0], f'MLD with respect to {refdepth_cols[idx].iloc[0]}m', va='center',
                         ha='right', backgroundcolor='white', color='green', transform=ax1.get_yaxis_transform())
            if df_filtered['overturn'].any():
                plt.title(
                    f"{filename}\n Depth vs. Salinity and Density with LOESS Transform \n THIS IS AN UNSTABLE WATER COLUMN \n(Higher density fluid lies above lower density fluid)")
            else:
                plt.title(
                    f"{filename}\n Depth vs. Salinity and Density with LOESS Transform \n THIS IS AN UNSTABLE WATER COLUMN \n(Higher density fluid lies above lower density fluid)")
            ax1.grid(True)
            lines, labels = ax1.get_legend_handles_labels()
            ax2_legend = ax2.get_legend_handles_labels()
            ax1.legend(lines + ax2_legend[0], labels + ax2_legend[1], loc='lower center', bbox_to_anchor=(0.5, -0.15),
                       ncol=3)
            plot_path = os.path.join(self._cwd, f"plots/{filename}_salinity_density_depth_plot_dual_x_axes_line.png")
            plot_folder = os.path.join(self._cwd, "plots")
            if not (os.path.isdir(plot_folder)):
                os.mkdir(plot_folder)
            plt.savefig(plot_path)
            plt.close(fig)

        def plot_depth_density_salinity_mld_scatter(self):
            """
            Plot depth vs. salinity and density with MLD lines using scatter points.

            Generates a scatter plot of depth vs. salinity and density.
            Adds horizontal lines indicating the mixed layer depth (MLD) at different reference depths.
            Saves the plot as an image file.
            """
            df = self._ctd_array.copy()
            filename = self._filename
            plt.rcParams.update({'font.size': 16})
            df_filtered = df
            if df_filtered.empty:
                plt.close()
                return
            df_filtered = df_filtered.reset_index(drop=True)
            fig, ax1 = plt.subplots(figsize=(18, 18))
            ax1.invert_yaxis()
            # Dynamically set y-axis limits based on depth data
            max_depth = df_filtered['depth_00'].max()
            ax1.set_ylim([max_depth, 0])  # Assuming depth increases downwards
            color_salinity = 'tab:blue'
            ax1.scatter(df_filtered['salinity_00'], df_filtered['depth_00'], color=color_salinity,
                        label='Practical Salinity')
            ax1.set_xlabel('Practical Salinity (PSU)', color=color_salinity)
            ax1.set_ylabel('Depth (m)')
            ax1.tick_params(axis='x', labelcolor=color_salinity)
            ax2 = ax1.twiny()
            color_density = 'tab:red'
            ax2.scatter(df_filtered['density'], df_filtered['depth_00'], color=color_density, label='Density (kg/m^3)')
            ax2.set_xlabel('Density (kg/m^3)', color=color_density)
            ax2.tick_params(axis='x', labelcolor=color_density)
            ax2.xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
            mld_cols = []
            for col in df.columns:
                if 'MLD' in col and 'Actual' not in col:
                    mld_cols.append(df[col])
            refdepth_cols = []
            for col in df.columns:
                if 'Actual' in col:
                    refdepth_cols.append(df[col])
            for idx, mld_col in enumerate(mld_cols):
                ax1.axhline(y=mld_col.iloc[0], color='green', linestyle='--',
                            label=f'MLD {refdepth_cols[idx].iloc[0]} Ref')
                ax1.text(0.95, mld_col.iloc[0], f'MLD with respect to {refdepth_cols[idx].iloc[0]}m', va='center',
                         ha='right', backgroundcolor='white', color='green', transform=ax1.get_yaxis_transform())
            if df_filtered['overturn'].any():
                plt.title(
                    f"{filename}\n Depth vs. Salinity and Density \n THIS IS AN UNSTABLE WATER COLUMN \n(Higher density fluid lies above lower density fluid)")
            else:
                plt.title(
                    f"{filename}\n Depth vs. Salinity and Density \n THIS IS AN UNSTABLE WATER COLUMN \n(Higher density fluid lies above lower density fluid)")
            ax1.grid(True)
            lines, labels = ax1.get_legend_handles_labels()
            ax2_legend = ax2.get_legend_handles_labels()
            ax1.legend(lines + ax2_legend[0], labels + ax2_legend[1], loc='upper center', bbox_to_anchor=(0.5, -0.15),
                       ncol=3)
            plot_path = os.path.join(self._cwd, f"plots/{filename}_salinity_density_depth_plot_dual_x_axes.png")
            plot_folder = os.path.join(self._cwd, "plots")
            if not (os.path.isdir(plot_folder)):
                os.mkdir(plot_folder)
            plt.savefig(plot_path)
            plt.close(fig)

        def plot_depth_temperature_scatter(self):
            """
            Plot depth vs. temperature with MLD lines using scatter points.

            Generates a scatter plot of depth vs. temperature.
            Adds horizontal lines indicating the mixed layer depth (MLD) at different reference depths.
            Saves the plot as an image file.
            """
            df = self._ctd_array.copy()
            filename = self._filename
            plt.rcParams.update({'font.size': 16})
            df_filtered = df
            if df_filtered.empty:
                plt.close()
                return
            df_filtered = df_filtered.reset_index(drop=True)
            fig, ax1 = plt.subplots(figsize=(18, 18))
            ax1.invert_yaxis()
            # Dynamically set y-axis limits based on depth data
            max_depth = df_filtered['depth_00'].max()
            ax1.set_ylim([max_depth, 0])  # Assuming depth increases downwards

            color_temp = 'tab:blue'
            ax1.scatter(df_filtered['temperature_00'], df_filtered['depth_00'], color=color_temp,
                        label="Temperature (°C)")
            ax1.set_xlabel("Temperature (°C)", color=color_temp)
            ax1.set_ylabel('Depth (m)')
            ax1.tick_params(axis='x', labelcolor=color_temp)
            mld_cols = []
            for col in df.columns:
                if "MLD" in col and "Actual" not in col:
                    mld_cols.append(df[col])
            refdepth_cols = []
            for col in df.columns:
                if "Reference Depth" in col:
                    refdepth_cols.append(df[col])
            for idx, mld_col in enumerate(mld_cols):
                ax1.axhline(y=mld_col.iloc[0], color='green', linestyle='--',
                            label=f'MLD {refdepth_cols[idx].iloc[0]} Ref')
                ax1.text(0.95, mld_col.iloc[0], f'MLD with respect to {refdepth_cols[idx].iloc[0]}m', va='center',
                         ha='right', backgroundcolor='white', color='green', transform=ax1.get_yaxis_transform())
            if df_filtered['overturn'].any():
                plt.title(
                    f"{filename}\n Depth vs. Temperature \n THIS IS AN UNSTABLE WATER COLUMN \n(Higher density fluid lies above lower density fluid)")
            else:
                plt.title(
                    f"{filename}\n Depth vs. Temperature \n THIS IS AN UNSTABLE WATER COLUMN \n(Higher density fluid lies above lower density fluid)")
            ax1.grid(True)
            lines, labels = ax1.get_legend_handles_labels()
            ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
            plot_path = os.path.join(self._cwd, f"plots/{filename}_temperature_depth_plot.png")
            plot_folder = os.path.join(self._cwd, "plots")
            if not (os.path.isdir(plot_folder)):
                os.mkdir(plot_folder)
            plt.savefig(plot_path)
            plt.close(fig)

        class _Utility:
            """
            _Utility
            --------

            Utility class for CTD data processing.

            :var filename: Filename of the RSK file.
            :var mastersheet: Path to the master sheet Excel file.
            """

            def __init__(self, filename):
                """
                Initialize a new _Utility object.

                :param filename: The filename of the RSK file.
                """
                self.filename = filename
                self.mastersheet = os.path.join(CTDFjorder._Filesystem.get_cwd(), CTDFjorder.master_sheet_path)

            def no_values_in_object(self, object_to_check):
                """
                Check if an object has no values.

                :param object_to_check: The object to check for values.
                :return: True if the object has no values, False otherwise.

                Checks if the given object is None, empty, or has a length greater than 0.
                Returns True if the object has no values, False otherwise.
                """
                if isinstance(object_to_check, type(None)):
                    return True
                if object_to_check.empty:
                    return True
                if len(object_to_check) > 0:
                    return False

            def process_master_sheet(self, master_sheet_path, filename):
                """
                Process the master sheet to find the closest location and time for a given filename.

                :param master_sheet_path: The path to the master sheet Excel file.
                :param filename: The filename of the RSK file.
                :return: A tuple containing the estimated latitude, longitude, and updated filename.

                Extracts the date and time components from the filename and compares them with the data
                in the master sheet. Calculates the absolute differences between the dates and times to
                find the closest match. Returns the estimated latitude, longitude, and updated filename
                based on the closest match.
                """

                def get_date_from_string(filename):
                    try:
                        year = filename.split('_')[1][:4]
                        month = filename.split('_')[1][4:6]
                        day = filename.split('_')[1][6:]
                        hour = filename.split('_')[2][0:2]
                        minute = filename.split('_')[2][2:4]
                        time = f"{hour}:{minute}"
                        return float(year), float(month), float(day), time
                    except:
                        return None, None, None, None

                # Function to calculate the absolute difference between two dates
                def date_difference(row, target_year, target_month, target_day):
                    return abs(row['year'] - target_year) + abs(row['month'] - target_month) + abs(
                        row['day'] - target_day)

                # Function to calculate the absolute difference between two times
                def time_difference(target_time, df_time):
                    df_time_str = str(df_time)
                    target_hour, target_minute = [int(target_time.split(':')[0]), int(target_time.split(':')[1])]
                    try:
                        df_hour, df_minute = [int(df_time_str.split(':')[0]), int(df_time_str.split(':')[1])]
                    except:
                        return None
                    return abs((target_hour * 60 + target_minute) - (df_hour * 60 + df_minute))

                # Load the master sheet
                master_df = pd.read_excel(master_sheet_path)
                # Get date and time components from the filename
                year, month, day, time = get_date_from_string(filename)
                if year is None:
                    return
                # Calculate absolute differences for each row in 'master_df'
                master_df['date_difference'] = master_df.apply(date_difference, args=(year, month, day), axis=1)
                master_df['time_difference'] = master_df['time_local'].apply(lambda x: time_difference(time, x))
                # Find the rows with the smallest total difference for date
                smallest_date_difference = master_df['date_difference'].min()
                closest_date_rows = master_df[master_df['date_difference'] == smallest_date_difference]
                # Check if time_difference returns None
                if closest_date_rows['time_difference'].isnull().any():
                    closest_time_time = None
                    closest_row_overall = closest_date_rows.iloc[0]
                else:
                    # If there are multiple rows with the smallest date difference, select the row with the smallest time difference
                    if len(closest_date_rows) > 1:
                        closest_time_row = closest_date_rows.loc[closest_date_rows['time_difference'].idxmin()]
                        closest_row_overall = closest_time_row
                        closest_time_time = closest_row_overall['time_local']
                    else:
                        closest_row_overall = closest_date_rows.iloc[0]
                        closest_time_time = closest_row_overall['time_local']
                latitude = closest_row_overall['latitude']
                longitude = closest_row_overall['longitude']
                unique_id = closest_row_overall.iloc[0]
                RBRfilename = filename + "_gpscm"
                # Access the closest date components
                closest_date_year = closest_row_overall['year']
                closest_date_month = closest_row_overall['month']
                closest_date_day = closest_row_overall['day']
                # Print the closest date and time
                print("|-ESTIMATION ALERT-|")
                print("Had to guess location on file: " + filename)
                print("Unique ID: " + unique_id)
                print("Closest Date (Year, Month, Day):", closest_date_year, closest_date_month, closest_date_day)
                print("Lat: " + str(latitude))
                print("Long: " + str(longitude))
                if closest_time_time:
                    print("Closest Time:", closest_time_time)
                print("====================")
                return latitude, longitude, RBRfilename

            def get_sample_location(self, rsk, filename):
                """
                Get the sample location from the RSK file or estimate it using the master sheet.

                :param rsk: The RSK object.
                :param filename: The filename of the RSK file.
                :return: A tuple containing the latitude, longitude, and updated filename.

                Retrieves the sample location data from the RSK file. If no location data is found,
                it attempts to estimate the location using the master sheet. Returns the latitude,
                longitude, and updated filename.
                """
                # Adding geo data, assumes no drift and uses the first lat long in the file if there is one
                geo_data_length = len(list(itertools.islice(rsk.geodata(), None)))
                if geo_data_length < 1:
                    latitude_intermediate, longitude_intermediate, filename = self.process_master_sheet(
                        self.mastersheet, filename)
                    return latitude_intermediate, longitude_intermediate, filename
                else:
                    for geo in itertools.islice(rsk.geodata(), None):
                        # Is there geo data?
                        if geo.latitude is not None:
                            # If there is, is it from the southern ocean?
                            if not (geo.latitude > -60):
                                try:
                                    latitude_intermediate = geo.latitude[0]
                                    longitude_intermediate = geo.longitude[0]
                                    filename += "_gps"
                                    return latitude_intermediate, longitude_intermediate, filename
                                except:
                                    latitude_intermediate = geo.latitude
                                    longitude_intermediate = geo.longitude
                                    filename += "_gps"
                                    return latitude_intermediate, longitude_intermediate, filename
                            else:
                                latitude_intermediate, longitude_intermediate, filename = self.process_master_sheet(
                                    self.mastersheet, filename)
                                return latitude_intermediate, longitude_intermediate, filename
                        else:
                            return None, None, filename + 'gpserror'

            def remove_sample_timezone_indicator(self, df):
                """
                Remove the timezone indicator from the 'timestamp' column of a DataFrame.

                :param df: The DataFrame to process.
                :return: The updated DataFrame with the timezone indicator removed.

                Removes the timezone indicator (e.g., '+00:00') from the 'timestamp' column of the
                given DataFrame. Returns the updated DataFrame.
                """
                if self.no_values_in_object(df):
                    return None
                if 'timestamp' in df.columns:
                    df['timestamp'] = df['timestamp'].astype(str).str.split('+').str[0]
                    return df
                else:
                    return df

            def remove_rows_with_negative_depth(self, df):
                """
                Remove rows with negative depth values from a DataFrame.

                :param df: The DataFrame to process.
                :return: The updated DataFrame with rows containing negative depth values removed.

                Removes rows from the given DataFrame where the 'depth_00' column has negative values.
                Returns the updated DataFrame.
                """
                if self.no_values_in_object(df):
                    return None
                if 'depth_00' in df.columns:
                    df = df[df['depth_00'] >= 0].reset_index(drop=True)
                else:
                    return None
                if self.no_values_in_object(df):
                    return None
                return df.copy()

            def remove_rows_with_negative_salinity(self, df):
                """
                Remove rows with negative salinity values from a DataFrame.

                :param df: The DataFrame to process.
                :return: The updated DataFrame with rows containing negative salinity values removed.

                Removes rows from the given DataFrame where the 'salinity_00' column has negative values.
                Returns the updated DataFrame.
                """
                if self.no_values_in_object(df):
                    return None
                if 'salinity_00' in df.columns:
                    df = df[df['salinity_00'] >= 0].reset_index(drop=True)
                else:
                    return None
                if self.no_values_in_object(df):
                    return None
                return df.copy()

            def remove_rows_with_negative_pressure(self, df):
                """
                Remove rows with negative pressure values from a DataFrame.

                :param df: The DataFrame to process.
                :return: The updated DataFrame with rows containing negative pressure values removed.

                Removes rows from the given DataFrame where the 'pressure_00' column has negative values.
                Returns the updated DataFrame.
                """
                if self.no_values_in_object(df):
                    return None
                if 'pressure_00' in df.columns:
                    df = df[df['pressure_00'] >= 0].reset_index(drop=True)
                else:
                    return None
                if self.no_values_in_object(df):
                    return None
                return df.copy()

            def remove_rows_with_negative_salinityabs(self, df):
                """
                Remove rows with negative absolute salinity values from a DataFrame.

                :param df: The DataFrame to process.
                :return: The updated DataFrame with rows containing negative absolute salinity values removed.

                Removes rows from the given DataFrame where the 'salinityabs' column has negative values.
                Returns the updated DataFrame.
                """
                if self.no_values_in_object(df):
                    return None
                if 'salinityabs' in df.columns:
                    df = df[df['salinityabs'] >= 0].reset_index(drop=True)
                else:
                    return None
                if self.no_values_in_object(df):
                    return None
                return df.copy()

            def remove_rows_with_negative_density(self, df):
                """
                Remove rows with negative density values from a DataFrame.

                :param df: The DataFrame to process.
                :return: The updated DataFrame with rows containing negative density values removed.

                Removes rows from the given DataFrame where the 'density' column has negative values.
                Returns the updated DataFrame.
                """
                if self.no_values_in_object(df):
                    return None
                if 'density' in df.columns:
                    df = df[df['density'] >= 0].reset_index(drop=True)
                else:
                    return None
                if self.no_values_in_object(df):
                    return None
                return df.copy()

        # =============================================================================
        # Section: Calculation Functions
        # =============================================================================

        class _Calculate:
            """
            _Calculate
            ----------

            Class for CTD data calculations.
            """

            @staticmethod
            def gsw_infunnel(SA, CT, p):
                """
                .. staticmethod:: gsw_infunnel(SA, CT, p)
                    :param SA: Absolute Salinity [g/kg]
                    :param CT: Conservative Temperature [deg C]
                    :param p: Sea pressure [dbar] (absolute pressure - 10.1325 dbar)
                    :returns: A boolean series where True indicates the values are inside the "oceanographic funnel".

                Checks if the given Absolute Salinity (SA), Conservative Temperature (CT), and pressure (p) are within the "oceanographic funnel" for the TEOS-10 75-term equation.
                """
                # Ensure all inputs are Series and aligned
                if not (isinstance(SA, pd.Series) and isinstance(CT, pd.Series) and (
                        isinstance(p, pd.Series) or np.isscalar(p))):
                    raise CTDError("","SA, CT, and p must be pandas Series or p a scalar")

                if isinstance(p, pd.Series) and (SA.index.equals(CT.index) and SA.index.equals(p.index)) is False:
                    raise CTDError("","Indices of SA, CT, and p must be aligned")

                if np.isscalar(p):
                    p = pd.Series(p, index=SA.index)

                # Define the funnel conditions
                CT_freezing_p = gsw.CT_freezing(SA, p, 0)
                CT_freezing_500 = gsw.CT_freezing(SA, 500, 0)

                in_funnel = pd.Series(True, index=SA.index)  # Default all to True
                condition = (
                        (p > 8000) |
                        (SA < 0) | (SA > 42) |
                        ((p < 500) & (CT < CT_freezing_p)) |
                        ((p >= 500) & (p < 6500) & (SA < p * 5e-3 - 2.5)) |
                        ((p >= 500) & (p < 6500) & (CT > (31.66666666666667 - p * 3.333333333333334e-3))) |
                        ((p >= 500) & (CT < CT_freezing_500)) |
                        ((p >= 6500) & (SA < 30)) |
                        ((p >= 6500) & (CT > 10.0)) |
                        SA.isna() | CT.isna() | p.isna()
                )
                in_funnel[condition] = False

                return in_funnel

            @staticmethod
            def calculate_and_drop_salinity_spikes(df):
                """
                .. staticmethod:: calculate_and_drop_salinity_spikes(df, filename)
                    :param df: DataFrame containing depth and salinity data
                    :returns: DataFrame after removing salinity spikes

                Calculates and removes salinity spikes from the CTD data based on predefined thresholds for acceptable changes in salinity with depth.
                """
                acceptable_delta_salinity_per_depth = [
                    (0.0005, 0.001),
                    (0.005, 0.01),
                    (0.05, 0.1),
                    (0.5, 1)
                ]
                if df.empty:
                    return None
                # Convert 'depth_00' and 'salinity_00' to numeric, coercing errors
                df['depth_00'] = pd.to_numeric(df['depth_00'], errors='coerce')
                df['salinity_00'] = pd.to_numeric(df['salinity_00'], errors='coerce')

                # Drop any rows where either 'depth_00' or 'salinity_00' is NaN
                df = df.dropna(subset=['depth_00', 'salinity_00'])

                # Check if there is enough depth range to calculate
                min_depth = df['depth_00'].min()
                max_depth = df['depth_00'].max()
                if min_depth == max_depth:
                    print("Insufficient depth range to calculate.")
                    return df

                def recursively_drop(df, depth_range, acceptable_delta, i):
                    try:
                        num_points = int((max_depth - min_depth) / depth_range)  # Calculate number of points
                    except:
                        print("Error in calculating number of points.")
                        return df
                    ranges = np.linspace(min_depth, max_depth, num=num_points)

                    # Group by these ranges
                    groups = df.groupby(pd.cut(df['depth_00'], ranges), observed=True)

                    # Calculate the min and max salinity for each range and filter ranges where the difference is <= 1
                    filtered_groups = groups.filter(
                        lambda x: abs(x['salinity_00'].max() - x['salinity_00'].min()) <= acceptable_delta)
                    # Get the indices of the filtered groups
                    filtered_indices = filtered_groups.index
                    return filtered_groups

                for i, deltas in enumerate(acceptable_delta_salinity_per_depth):
                    df = recursively_drop(df, deltas[0], deltas[1], i)
                return df

            @staticmethod
            def calculate_overturns(ctd_array):
                """
                .. staticmethod:: calculate_overturns(ctd_array)
                    :param ctd_array: DataFrame containing depth, density, and timestamp data
                    :returns: DataFrame with identified density overturns

                Calculates density overturns in the CTD data where denser water lies above lighter water, which may indicate mixing or other dynamic processes.
                """
                # Sort DataFrame by depth in ascending order
                ctd_array = ctd_array.sort_values(by='depth_00', ascending=True)
                # Calculate density change and identify overturns
                ctd_array['density_change'] = ctd_array[
                    'density'].diff()  # Difference in density between consecutive measurements
                ctd_array['overturn'] = ctd_array[
                                            'density_change'] < -0.05  # Negative change indicates denser water above less dense water
                ctd_array = ctd_array.sort_values(by='timestamp', ascending=True)
                return ctd_array

            @staticmethod
            def calculate_absolute_density(ctd_array):
                """
                .. staticmethod:: calculate_absolute_density(ctd_array)
                    :param ctd_array: DataFrame containing salinity, temperature, and pressure data
                    :returns: Series with calculated absolute density

                Calculates absolute density from the CTD data using the TEOS-10 equations, ensuring all data points are within the valid oceanographic funnel.
                """
                SA = ctd_array['salinity_00']
                t = ctd_array['temperature_00']
                p = ctd_array['pressure_00']
                CT = gsw.CT_from_t(SA, t, p)
                if CTDFjorder.CTD._Calculate.gsw_infunnel(SA, CT, p).all():
                    return gsw.density.rho_t_exact(SA, t, p)
                else:
                    raise CTDError("","Sample not in funnel, could not calculate density.")

            @staticmethod
            def calculate_absolute_salinity(ctd_array):
                """
                .. staticmethod:: calculate_absolute_salinity(ctd_array)
                    :param ctd_array: DataFrame containing practical salinity, pressure, longitude, and latitude data
                    :returns: Series with calculated absolute salinity

                Calculates absolute salinity from practical salinity, pressure, and geographical coordinates using the TEOS-10 salinity conversion formulas.
                """
                SP = ctd_array['salinity_00']
                p = ctd_array['pressure_00']
                lon = ctd_array['longitude']
                lat = ctd_array['latitude']
                return gsw.conversions.SA_from_SP(SP, p, lon, lat)

            @staticmethod
            def calculate_mld(densities, depths, reference_depth):
                """
                .. staticmethod:: calculate_mld(densities, depths, reference_depth)
                    :param densities: Series of densities
                    :param depths: Series of depths corresponding to densities
                    :param reference_depth: The depth at which to anchor the reference density
                    :returns: Tuple containing the mixed layer depth and reference depth

                Calculates the mixed layer depth (MLD) using the density threshold method. MLD is the depth at which the density exceeds the reference density by a predefined amount (e.g., 0.05 kg/m³).
                """
                # Convert to numeric and ensure no NaNs remain
                densities = densities.apply(pd.to_numeric, errors='coerce')
                depths = depths.apply(pd.to_numeric, errors='coerce')
                densities = densities.dropna(how='any').reset_index(drop=True)
                depths = depths.dropna(how='any').reset_index(drop=True)
                reference_depth = int(reference_depth)
                if len(depths) == 0 or len(densities) == 0:
                    return None
                sorted_data = sorted(zip(depths, densities), key=lambda x: x[0])
                sorted_depths, sorted_densities = zip(*sorted_data)
                # Determine reference density
                reference_density = None
                for i, depth in enumerate(sorted_depths):
                    if depth >= reference_depth:
                        if depth == reference_depth:
                            reference_density = sorted_densities[i]
                            reference_depth = sorted_depths[i]
                        else:
                            # Linear interpolation
                            try:
                                reference_density = sorted_densities[i - 1] + (
                                        (sorted_densities[i] - sorted_densities[i - 1]) * (
                                        (reference_depth - sorted_depths[i - 1]) /
                                        (sorted_depths[i] - sorted_depths[i - 1])))
                            except:
                                raise CTDError("",
                                    f"Insufficient depth range to calculate MLD. Maximum sample depth is {depths.max()}, minimum is {depths.min()}")
                        break
                if reference_density is None:
                    return None
                # Find the depth where density exceeds the reference density by more than 0.05 kg/m³
                for depth, density in zip(sorted_depths, sorted_densities):
                    if density > reference_density + 0.05 and depth >= reference_depth:
                        return depth, reference_depth
                return None  # If no depth meets the criterion

            @staticmethod
            def calculate_mld_loess(densities, depths, reference_depth):
                """
                .. staticmethod:: calculate_mld_LOESS(densities, depths, reference_depth)
                    :param densities: Series of densities
                    :param depths: Series of depths corresponding to densities
                    :param reference_depth: The depth at which to anchor the reference density
                    :returns: Tuple containing the mixed layer depth and reference depth

                Calculates the mixed layer depth (MLD) using LOESS smoothing to first smooth the density profile and then determine the depth where the smoothed density exceeds the reference density by a predefined amount.
                """
                # Ensure input is pandas Series and drop NA values
                if isinstance(densities, pd.Series) and isinstance(depths, pd.Series):
                    densities = densities.dropna().reset_index(drop=True)
                    depths = depths.dropna().reset_index(drop=True)

                # Convert to numeric and ensure no NaNs remain
                densities = densities.apply(pd.to_numeric, errors='coerce')
                depths = depths.apply(pd.to_numeric, errors='coerce')
                densities = densities.dropna().reset_index(drop=True)
                depths = depths.dropna().reset_index(drop=True)
                if densities.empty or depths.empty:
                    return None, None

                # Convert pandas Series to numpy arrays for NumPy operations
                densities = densities.to_numpy()
                depths = depths.to_numpy()

                # Remove duplicates by averaging densities at the same depth
                unique_depths, indices = np.unique(depths, return_inverse=True)
                average_densities = np.zeros_like(unique_depths)
                np.add.at(average_densities, indices, densities)
                counts = np.zeros_like(unique_depths)
                np.add.at(counts, indices, 1)
                average_densities /= counts

                # Apply LOESS smoothing
                lowess = statsmodels.api.nonparametric.lowess
                smoothed = lowess(average_densities, unique_depths, frac=0.1)
                smoothed_depths, smoothed_densities = zip(*smoothed)
                reference_density = np.interp(reference_depth, smoothed_depths, smoothed_densities)

                # Find the depth where density exceeds the reference density by more than 0.05 kg/m³
                exceeding_indices = np.where(np.array(smoothed_densities) > reference_density + 0.05)[0]
                if exceeding_indices.size > 0:
                    mld_depth = smoothed_depths[exceeding_indices[0]]
                    return mld_depth, reference_depth

                return None, None  # If no depth meets the criterion

            @staticmethod
            def calculate_mean_surface_density(df):
                """
                .. staticmethod:: calculate_mean_surface_density(df)
                  :param df: DataFrame containing density data
                  :returns: Mean surface density

                Calculates the mean surface density from the CTD data, includes all depth ranges in profile.
                """
                return df['density'].mean()

def main():
    if len(sys.argv) < 2:
        print("Usage: ctdfjorder <command> [arguments]")
        print("Commands:")
        print("  process <file>          Process a single RSK file")
        print("  merge                   Merge all RSK files in the current folder")
        print("  default                 Run the default processing pipeline")
        print("CWD:")
        print(CTDFjorder.CTD.get_cwd())
        sys.exit(1)

    command = sys.argv[1]

    if command == "process":
        if len(sys.argv) < 3:
            print("Usage: ctdfjorder process <file>")
            sys.exit(1)

        file_path = sys.argv[2]
        try:
            ctd = CTDFjorder.CTD(file_path)
            ctd.add_filename_to_table()
            ctd.save_to_csv("output.csv")
            ctd.add_location_to_table()
            ctd.remove_non_positive_samples()
            ctd.run_complex_cleaner("practicalsalinity", 'salinitydiff')
            ctd.add_absolute_salinity()
            ctd.add_density()
            ctd.add_overturns()
            ctd.add_mld(0)
            ctd.add_mld(10)
            ctd.save_to_csv("outputclean.csv")
            print("Processing completed successfully.")
        except Exception as e:
            print(f"Error processing file: '{file_path}' {e}")

    elif command == "merge":
        CTDFjorder.merge_all_in_folder()
        print("Merging completed successfully.")

    elif command == "default":
        CTDFjorder.run_default()
        print("Default processing completed successfully.")

    elif command == "defaultplotall":
        CTDFjorder.run_default(True)
        print("Default processing completed successfully.")

    else:
        print(f"Unknown command: {command}")
        print("Usage: ctdfjorder <command> [arguments]")
        print("Commands:")
        print("  process <file>          Process a single RSK file")
        print("  merge                   Merge all RSK files in the current folder")
        print("  default                 Run the default processing pipeline")
        print("  defaultplotall          Run the default processing pipeline and create plots")
        print("CWD:")
        print(CTDFjorder.CTD.get_cwd())
        sys.exit(1)

if __name__ == "__main__":
    main()

