# hhnk_research_tools/__init__.py
from typing import TYPE_CHECKING

from hhnk_research_tools.gis.raster import Raster, RasterMetadata  # noqa: F401

if TYPE_CHECKING:
    # TODO zou moeten werken met typehints van imports. Maar vraag is maar of het werkt.
    import hhnk_research_tools as hrt

import hhnk_research_tools.threedi as threedi
import hhnk_research_tools.variables as variables
import hhnk_research_tools.waterschadeschatter.resources
from hhnk_research_tools.dataframe_functions import (
    df_add_geometry_to_gdf,
    df_convert_to_gdf,
    gdf_write_to_csv,
    gdf_write_to_geopackage,
)
from hhnk_research_tools.folder_file_classes.file_class import File
from hhnk_research_tools.folder_file_classes.folder_file_classes import (
    File,
    FileGDB,
    FileGDBLayer,
    Folder,
)
from hhnk_research_tools.folder_file_classes.sqlite_class import (
    Sqlite,
)
from hhnk_research_tools.folder_file_classes.threedi_schematisation import (
    RevisionsDir,
    ThreediResult,
    ThreediSchematisation,
)
from hhnk_research_tools.general_functions import (
    check_create_new_file,
    convert_gdb_to_gpkg,
    current_time,
    dict_to_class,
    ensure_file_path,
    get_functions,
    get_pkg_resource_path,
    get_uuid,
    get_variables,
    load_source,
    time_delta,
)
from hhnk_research_tools.gis.raster_calculator import RasterBlocks, RasterCalculatorV2
from hhnk_research_tools.raster_functions import (
    RasterCalculator,
    build_vrt,
    create_meta_from_gdf,
    create_new_raster_file,
    dx_dy_between_rasters,
    gdf_to_raster,
    hist_stats,
    load_gdal_raster,
    reproject,
    save_raster_array_to_tiff,
)
from hhnk_research_tools.sql_functions import (
    create_sqlite_connection,
    execute_sql_changes,
    execute_sql_selection,
    sql_construct_select_query,
    sql_create_update_case_statement,
    sql_table_exists,
    sqlite_replace_or_add_table,
    sqlite_table_to_df,
    sqlite_table_to_gdf,
)
from hhnk_research_tools.threedi.call_api import call_threedi_api
from hhnk_research_tools.threedi.read_api_file import read_api_file
from hhnk_research_tools.waterschadeschatter.wss_main import Waterschadeschatter

# TODO how does this versioning work?
# Threedigrid version number is automatic updated with zest.releaser. Geopandas uses versioneer.py.
# the version number in setup.py is updated using the find_version()
__version__ = "2024.1"

__doc__ = """
General toolbox for loading, converting and saving serval datatypes.
"""
