import os
from pathlib import Path

import numpy as np

import hhnk_research_tools as hrt
from hhnk_research_tools.folder_file_classes.file_class import File
from hhnk_research_tools.folder_file_classes.folder_file_classes import Folder
from hhnk_research_tools.folder_file_classes.sqlite_class import Sqlite
from hhnk_research_tools.gis.raster import Raster
from hhnk_research_tools.threedi.threediresult_loader import ThreediResultLoader

# Third-party imports


class ThreediSchematisation(Folder):
    """Threedi model/schematisation.
    expected files are the;
    .sqlite
    /rasters
        - content depends on model type, they are read from the global settings in the sqlite.
    """

    def __init__(self, base, name, create=True):
        super().__init__(os.path.join(base, name), create=create)

        # File
        # self.add_file("database", self.model_path())

    @property
    def rasters(self):
        return self.ThreediRasters(base=self.base, caller=self)

    @property
    def database(self):
        filepath = self.model_path()
        if filepath in [None, ""]:
            filepath = ""

        sqlite_cls = Sqlite(filepath)
        # if os.path.exists(sqlite_cls.path):
        #     return sqlite_cls
        # else:
        #     return None
        return sqlite_cls

    @property
    def structure(self):
        return f"""  
            {self.space}model
            {self.space}└── rasters
            """

    @property
    def database_path(self):
        return str(self.database)

    @property
    def sqlite_paths(self):
        """Return all sqlites in folder"""
        return self.find_ext("sqlite")

    @property
    def sqlite_names(self):
        """Return all sqlites in folder"""
        return [sp.stem for sp in self.sqlite_paths]

    def model_path(self, idx=0, name=None):
        """Find a model using an index"""
        if name:
            try:
                idx = self.sqlite_names.index(name)
            except Exception:
                raise ValueError("name of sqlite given, but cannot be found")
        if len(self.sqlite_paths) >= 1:
            return self.sqlite_paths[idx]
        else:
            return ""

    class ThreediRasters(Folder):
        def __init__(self, base, caller):
            super().__init__(os.path.join(base, "rasters"), create=True)
            self.caller = caller

            self.dem = self.get_raster_path(table_name="v2_global_settings", col_name="dem_file")
            self.storage = self.get_raster_path(
                table_name="v2_simple_infiltration",
                col_name="max_infiltration_capacity_file",
            )
            self.friction = self.get_raster_path(table_name="v2_global_settings", col_name="frict_coef_file")
            self.infiltration = self.get_raster_path(
                table_name="v2_simple_infiltration", col_name="infiltration_rate_file"
            )
            self.initial_wlvl_2d = self.get_raster_path(
                table_name="v2_global_settings", col_name="initial_waterlevel_file"
            )

            # Waterschadeschatter required 50cm resolution.
            self.dem_50cm = self.full_path("dem_50cm.tif")

            self.landuse = self.find_file_by_name("landuse_*.tif")

            self.add_file("soil", "soil.tif")
            # Groundwaterlevel (used to create storage)
            self.add_file("gwlvl_glg", "gwlvl_glg.tif")
            self.add_file("gwlvl_ggg", "gwlvl_ggg.tif")
            self.add_file("gwlvl_ghg", "gwlvl_ghg.tif")

        def find_file_by_name(self, name) -> File:
            tifs = [i for i in self.path.glob(name)]
            if len(tifs) == 0:
                tifs = [""]
            return File(tifs[0])

        def get_raster_path(self, table_name, col_name):
            """Read the sqlite to check which rasters are used in the model.
            This only works for models from Klondike release onwards, where we only have
            one global settings row.
            """

            if self.caller.database.exists():
                df = hrt.sqlite_table_to_df(database_path=self.caller.database.path, table_name=table_name)
                # if len(df) > 1:
                # print(f"{table_name} has more than 1 row. Choosing the first row for the rasters.")
                if len(df) == 0:
                    raster_name = None
                else:
                    raster_name = df.iloc[0][col_name]

                if raster_name is None:
                    raster_path = ""
                else:
                    raster_path = self.caller.full_path(raster_name)
            else:
                raster_path = ""
            return Raster(raster_path)

        def __repr__(self):
            return f"""  
    dem - {self.dem.name}
    storage - {self.storage.name}
    friction - {self.friction.name}
    infiltration - {self.infiltration.name}
    landuse - {self.landuse.name}
    initial_wlvl_2d - {self.initial_wlvl_2d.name}
    dem_50cm - {self.dem_50cm.name}
"""


class ThreediResult(Folder):
    """Result of threedi simulation. Base files are .nc and .h5.
    Use .grid to access GridH5ResultAdmin and .admin to access GridH5Admin
    """

    def __init__(self, base, create=False):
        super().__init__(base, create=create)

        # Files
        self.add_file("grid_path", "results_3di.nc")
        self.add_file("admin_path", "gridadmin.h5")

    @property
    def grid(self):
        # moved imports here because gridbuilder has h5py issues
        from threedigrid.admin.gridresultadmin import GridH5ResultAdmin

        return GridH5ResultAdmin(self.admin_path.base, self.grid_path.base)

    @property
    def admin(self):
        from threedigrid.admin.gridadmin import GridH5Admin

        return GridH5Admin(self.admin_path.base)

    @property
    def load(self):
        return ThreediResultLoader(self.grid)


class RevisionsDir(Folder):
    """directory with subfolders.
    When the dir is accessed with indexing ["foldername"], the returnclass is retured.
    This defaults to the ThreediResult directory with .nc and .h5. But for climate results
    the folder structure is a bit different.
    """

    def __init__(self, base, name, returnclass=ThreediResult, create=False):
        super().__init__(os.path.join(base, name), create=create)
        self.isrevisions = True
        self.returnclass = returnclass  # eg ClimateResult
        self.sub_folders = {}  # revisions that are already initialized.

    def __getitem__(self, revision):
        """revision can be a integer or a path"""
        create = True
        if revision in ["", None]:
            create = False

        if type(revision) == int:  # revision number as input
            revision_dir = self.revisions[revision]
        elif os.path.isabs(str(revision)):  # full path as input
            revision_dir = revision
        elif not os.sep in str(revision):
            revision_dir = self.full_path(revision)
        else:
            raise ValueError(f"{str(revision)} is not valid input for `revision`")

        revision_dir = Folder(revision_dir)
        if not revision_dir.name in self.sub_folders.keys():
            self.sub_folders[revision_dir.name] = self.returnclass(revision_dir, create=create)

        return self.sub_folders[revision_dir.name]

    def revision_structure(self, name):
        spacing = "\n\t\t\t\t\t\t\t"
        structure = f""" {spacing}{name} """
        for i, rev in enumerate(self.revisions):
            if i == len(self.revisions) - 1:
                structure = structure + f"{spacing}└── {rev}"
            else:
                structure = structure + f"{spacing}├── {rev}"

        return structure

    @property
    def revisions(self):
        return self.content

    @property
    def revisions_mtime(self):
        """sorted list of revisions by:
        mtime -> latest edit date first
        """
        revisions_sorted = np.take(self.revisions, np.argsort([item.lstat().st_mtime for item in self.revisions]))[
            ::-1
        ]
        return revisions_sorted

    @property
    def revisions_rev(self):
        """sort list of revisions by:
        rev -> revisions. highest revisionnr first
        """
        lst_items = []
        for item in self.revisions:
            try:
                lst_items += [int(str(item.name).split("#")[1].split(" ")[0])]
            except:
                lst_items += [0]  # add 0 so its always at end of list.
        revisions_sorted = np.take(self.revisions, np.argsort(lst_items))[::-1]
        return revisions_sorted
