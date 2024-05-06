 "use strict";

 //
 // 
 // ------------------------------------------------------
 // Dataframe Cleanser javascript utilities 
 // ------------------------------------------------------
 // 
 //

 const DEBUG_UTILS = false
 const DEBUG_DETAILS_UTILS = false
 const DEBUG_CELL_UTILS = false

 window.debug_load_flag = false;

 var dfc_loaded_flagged = false;


 window.log_prefix = '[' + "dfcleanser" + ']';

 window.NEW_LINE = "\n";


 //
 // ---------------------------------------------------
 // ---------------------------------------------------
 // Dataframe Cleanser cell metadata
 // ---------------------------------------------------
 // ---------------------------------------------------
 //


 //
 // ---------------------------------------------------
 // Dataframe Cleanser cell libs data
 // ---------------------------------------------------
 //
 window.DFC_CONSOLE_LIB = "from dfcleanser.system.system_control import ";
 window.SYSTEM_LIB = "from dfcleanser.system.system_control import ";
 window.COMMON_LIB = "from dfcleanser.common.common_utils import ";


 window.QT_CONSOLE_LIB = "from dfcleanser.Qt.system.SystemControl import ";
 window.QT_SYSTEM_LIB = "from dfcleanser.Qt.system.System import ";
 window.QT_SYSTEM_CONTOL_LIB = "from dfcleanser.Qt.system.SystemControl import ";
 window.QT_IMPORT_LIB = "from dfcleanser.Qt.data_import.DataImport import ";
 window.QT_EXPORT_LIB = "from dfcleanser.Qt.data_export.DataExport import ";
 window.QT_TRANSFORM_LIB = "from dfcleanser.Qt.data_transform.DataTransform import ";
 window.QT_INSPECTION_LIB = "from dfcleanser.Qt.data_inspection.DataInspection import ";
 window.QT_CLEANSING_LIB = "from dfcleanser.Qt.data_cleansing.DataCleansing import ";

 window.SW_UTILS_GEOCODE_LIB = "from dfcleanser.Qt.utils.Geocode.Geocode import ";
 window.SW_UTILS_GEOCODE_BULK_LIB = "from dfcleanser.Qt.utils.Geocode.BulkGeocode import ";
 window.SW_UTILS_GEOCODE_BULK_CONTROL_LIB = "from dfcleanser.Qt.utils.Geocode.BulkGeocodeControl import ";
 window.DF_BROWSER_LIB = "from dfcleanser.Qt.data_inspection.DataInspectionInspectRows import ";
 window.SW_UTILS_CENSUS_LIB = "from dfcleanser.Qt.utils.Census.Census import ";
 window.SW_UTILS_ZIPCODE_LIB = "from dfcleanser.Qt.utils.ZipCode.ZipCode import ";

 window.INSPECTION_GRAPHS_LIB = "from dfcleanser.Qt.data_inspection.DataInspectionColumnsWidgets import ";

 window.CFG_LIB = "from dfcleanser.common.cfg import ";
 window.HELP_LIB = "from dfcleanser.common.help_utils import ";

 window.OS_LIB = "from os import ";

 //
 // ---------------------------------------------------
 // Dataframe Cleanser jupyter cell ids
 // ---------------------------------------------------
 //
 window.DC_CONSOLE_ID = 0;
 window.DC_SYSTEM_ID = 1;
 window.DC_DATA_IMPORT_ID = 2;
 window.DC_DATA_INSPECTION_ID = 3;
 window.DC_DATA_CLEANSING_ID = 4;
 window.DC_DATA_TRANSFORM_ID = 5;
 window.DC_DATA_EXPORT_ID = 6;

 window.DC_GEOCODE_UTILITY_ID = 7;
 window.DC_DF_BROWSER_ID = 8;
 window.DC_CENSUS_ID = 9;
 window.DC_ZIPCODE_UTILITY_ID = 10;

 window.DC_GEOCODE_BULK_ID = 11;


 window.DC_WORKING_TITLE_ID = 12;
 window.DC_WORKING_CELL_ID = 13;

 window.DC_INSPECTION_GRAPHS_ID = 14;

 window.POPUP_CELL_ID = 28;

 const DC_BLANK_LINE_ID = 1000;

 const WORKING_CELL = "# Working Cell ";

 window.empty_cell_id = null;


 /* 
    --------------------------------------------------------------
    Jupyter Cell Metadata dfc_cellid values
    --------------------------------------------------------------
 */

 var dfc_cell_ids = [
     "DCConsole", "DCSystem", "DCDataImport", "DCDataInspection", "DCDataCleansing",
     "DCDataTransform", "DCDataExport", "DCGeocodeUtility", "DCDfBrowser", "DCCensusUtility",
     "DCZipcodeUtility", "DCGeocodeBulk", "DCWorkingTitle", "DCWorking", "DCInspectionGraphs",
     "dfcPopUpCell"
 ];

 /* 
      --------------------------------------------------------------
      Logical mapping to dfc_cellids above
      --------------------------------------------------------------
   */

 var dfc_chapter_element_ids = [
     "DC_CONSOLE_CHAPTER_ID", "DC_SYSTEM_CHAPTER_ID", "DC_DATA_IMPORT_CHAPTER_ID", "DC_DATA_INSPECTION_CHAPTER_ID", "DC_DATA_CLEANSING_CHAPTER_ID",
     "DC_DATA_TRANSFORM_CHAPTER_ID", "DC_DATA_EXPORT_CHAPTER_ID", "DC_GEOCODE_UTILITY_CHAPTER_ID", "DC_DFSUBSET_UTILITY_CHAPTER_ID", "DC_CENSUS_CHAPTER_ID",
     "DC_ZIPCODE_UTILITY_CHAPTER_ID", "DC_GEOCODE_BULK_CHAPTER_ID", "DC_WORKING_TITLE_CHAPTER_ID", "DC_WORKING_CELL_CHAPTER_ID", "DC_INSPECT_GRAPHS_CHAPTER_ID",
     "POPUP_CELL_ID",
 ];


 window.WORKING_CODE_CELL = '# working cell- please do not remove';
 window.WORKING_TITLE_CELL = '<div align="left" id="Restricted"/><div><img src="https://rickkrasinski.github.io/dfcleanser/graphics/Restricted.jpg" width="80" align="left"/></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;Restricted</h2></div></div>';
 window.LOCAL_WORKING_TITLE_CELL = '<div align="left" id="Restricted"/><div><img src="./PandasDataframeCleanser_files/graphics/Restricted.jpg" width="80" align="left"/></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;Restricted</h2></div></div>';
 window.WORKING_BLANK_LINE = '<br></br>';


 window.SYSTEM_TITLE_CELL = '<div align="left" id="Restricted"/><div><img src="https://rickkrasinski.github.io/dfcleanser/graphics/SystemChapter.png" width="80" align="left"/></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;System</h2></div></div>';
 window.DATA_IMPORT_TITLE_CELL = '<div align="left" id="Restricted"/><div><img src="https://rickkrasinski.github.io/dfcleanser/graphics/DataImportChapter.png" width="80" align="left"/></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;Data Import</h2></div></div>';
 window.DATA_INSPECTION_TITLE_CELL = '<div align="left" id="Restricted"/><div><img src="https://rickkrasinski.github.io/dfcleanser/graphics/DataInspectionChapter.png" width="80" align="left"/></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;Data Inspection</h2></div></div>';
 window.DATA_CLEANSING_TITLE_CELL = '<div align="left" id="Restricted"/><div><img src="https://rickkrasinski.github.io/dfcleanser/graphics/DataCleansingChapter.png width="80" align="left"/></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;Data Cleansing</h2></div></div>';
 window.DATA_TRANSFORM_TITLE_CELL = '<div align="left" id="Restricted"/><div><img src="https://rickkrasinski.github.io/dfcleanser/graphics/DataTransformChapter.png" width="80" align="left"/></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;Data Transform</h2></div></div>';
 window.DATA_EXPORT_TITLE_CELL = '<div align="left" id="Restricted"/><div><img src="https://rickkrasinski.github.io/dfcleanser/graphics/DataExportChapter.png" width="80" align="left"/></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;Data Export</h2></div></div>';

 window.ZIPCODE_TITLE_CELL = '<div align="left" id="Restricted"/><div><a  onclick="control_qt_chapter(0)";/> <img src="https://rickkrasinski.github.io/dfcleanser/graphics/ZipCodeChapter.png" width="80" align="left"/></a></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;ZipCode</h2></div></div>';
 window.GEOCODE_TITLE_CELL = '<div align="left" id="Restricted"/><div><a  onclick="alert(blow me)"/><img src="https://rickkrasinski.github.io/dfcleanser/graphics/GeocodeChapter.png" width="80" align="left"/></a></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;Geocoding</h2></div></div>';
 window.CENSUS_TITLE_CELL = '<div align="left" id="Restricted"/><div><img src="https://rickkrasinski.github.io/dfcleanser/graphics/CensusChapter.png" width="80" align="left"/></div><div><image width="10"></div><div><image width="10"><h2>&nbsp;&nbsp;&nbsp;Census</h2></div></div>';




 /* 
   ---------------------------------------------------------
   *
   *  dfc qt chapter control functions
   * 
   --------------------------------------------------------- 
 */



 /*
  *
  *  clear output of a dfcleanser chapter
  * 
  *  @function clear_dfcleanser_chapter_output
  * 
  *  @param : chapterid
  * 
  */
 function clear_dfcleanser_chapter_output(chapterid) {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     " + "clear_dfcleanser_chapter_output", chapterid);

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     " + "clear_dfcleanser_chapter_output", is_dfcleanser_chapter_loaded(chapterid));

     if (is_dfcleanser_chapter_loaded(chapterid)) {

         switch (chapterid) {

             case DC_GEOCODE_BULK_ID:
                 window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_bulk_geocoders", "-1"));
                 window.scroll_to(DC_GEOCODE_BULK_ID);
                 break;
             case DC_DF_BROWSER_ID:
                 window.run_code_in_cell(window.DC_DF_BROWSER_ID, window.getJSPCode(window.DF_BROWSER_LIB, "clearDfBrowser", ""));
                 break;
             case DC_CENSUS_ID:
                 window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "clearCensus", ""));
                 break;
             case DC_WORKING_CELL_ID:
                 window.run_code_in_cell(window.WORKING_CODE_CELL, window.getJSPCode(window.CFG_LIB, "sync_notebook", "0"));
                 break;
         }
     } else {

         switch (chapterid) {

             case DC_DATA_IMPORT_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_IMPORT_LIB, "clearDataImport", ""));
                 break;
             case DC_DATA_CLEANSING_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_CLEANSING_LIB, "clearDataCleansing", ""));
                 break;
             case DC_SYSTEM_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_SYSTEM_LIB, "clearSystem", ""));
                 break;
             case DC_DATA_EXPORT_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_EXPORT_LIB, "clearDataExport", ""));
                 break;
             case DC_DATA_TRANSFORM_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_TRANSFORM_LIB, "clearDataTransform", ""));
                 break;
             case DC_DATA_INSPECTION_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_INSPECTION_LIB, "clearDataInspection", ""));
                 break;
             case DC_GEOCODE_UTILITY_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_LIB, "clearGeocode", ""));
                 break;
             case DC_ZIPCODE_UTILITY_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_ZIPCODE_LIB, "clearZipCode", ""));
                 break;
         }


     }

     window.scroll_to(DC_WORKING_CELL_ID);
 }


 /*
  *
  *  reset a dfcleanser chapter
  * 
  *  @function load_dfcleanser_chapter
  * 
  *  @param : chapterid
  * 
  */
 function load_dfcleanser_chapter(chapterid) {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     " + "load_dfcleanser_chapter", chapterid, is_dfcleanser_chapter_loaded(chapterid));

     if (is_dfcleanser_chapter_loaded(chapterid)) {

         switch (chapterid) {

             case DC_CONSOLE_ID:
                 window.run_code_in_cell(window.DC_CONSOLE_ID, window.getJSPCode(window.QT_SYSTEM_CONTOL_LIB, "display_system_environment", "-1"));
                 break;
             case DC_DF_BROWSER_ID:
                 window.run_code_in_cell(window.DC_DF_BROWSER_ID, window.getJSPCode(window.DF_BROWSER_LIB, "showDfBrowser", ""));
                 break;
             case DC_WORKING_CELL_ID:
                 window.run_code_in_cell(window.WORKING_CODE_CELL, window.getJSPCode(window.CFG_LIB, "sync_notebook", "0"));
                 break;

         }
     } else {
         if (DEBUG_UTILS)
             console.log(log_prefix + "\n" + "     " + "load_dfcleanser_chapter(2)", chapterid, is_dfcleanser_chapter_loaded(chapterid));

         switch (chapterid) {

             case DC_SYSTEM_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_SYSTEM_LIB, "showSystem", ""));
                 break;
             case DC_DATA_IMPORT_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_IMPORT_LIB, "showDataImport", ""));
                 break;
             case DC_DATA_EXPORT_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_EXPORT_LIB, "showDataExport", ""));
                 break;
             case DC_DATA_CLEANSING_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_CLEANSING_LIB, "showDataCleansing", ""));
                 break;
             case DC_GEOCODE_UTILITY_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_LIB, "showGeocode", ""));
                 break;
             case DC_DATA_TRANSFORM_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_TRANSFORM_LIB, "showDataTransform", ""));
                 break;
             case DC_DATA_INSPECTION_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_INSPECTION_LIB, "showDataInspection", ""));
                 break;
             case DC_DF_BROWSER_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.DF_BROWSER_LIB, "showDfBrowser", ""));
                 break;
             case DC_ZIPCODE_UTILITY_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_ZIPCODE_LIB, "showZipCode", ""));
                 break;
             case DC_CENSUS_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "showCensus", ""));
                 break;



         }
     }
     window.scroll_to(DC_WORKING_CELL_ID);
 }

 /*
  *
  *  close_dfcleanser_chapter_instances
  * 
  *  @function close_dfcleanser_chapter
  * 
  *  @param : chapterid
  * 
  */
 function close_dfcleanser_chapter_instances(chapterid) {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     " + "close_dfcleanser_chapter_instances", chapterid);

     if (is_dfcleanser_chapter_loaded(chapterid)) {

         switch (chapterid) {

             case DC_DF_BROWSER_ID:
                 window.run_code_in_cell(window.DC_DF_BROWSER_ID, window.getJSPCode(window.DF_BROWSER_LIB, "closeDfBrowserInstances", ""));
                 break;
             case DC_CENSUS_ID:
                 window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "closeCensusInstances", ""));
                 break;
             case DC_WORKING_CELL_ID:
                 window.run_code_in_cell(window.WORKING_CODE_CELL, window.getJSPCode(window.CFG_LIB, "sync_notebook", "0"));
                 break;

             case DC_GEOCODE_BULK_ID:
                 window.delete_dfc_cell("DCGeocodeBulk");
                 break;

         }

     } else {

         switch (chapterid) {

             case DC_SYSTEM_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_SYSTEM_LIB, "closeSystemChapter", ""));
                 break;
             case DC_DATA_IMPORT_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_IMPORT_LIB, "closeDataImportChapter", ""));
                 break;
             case DC_DATA_EXPORT_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_IMPORT_LIB, "closeDataExportChapter", ""));
                 break;
             case DC_DATA_TRANSFORM_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_TRANSFORM_LIB, "closeDataTransformChapter", ""));
                 break;
             case DC_DATA_INSPECTION_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_INSPECTION_LIB, "closeDataExportChapter", ""));
                 break;
             case DC_DATA_CLEANSING_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_CLEANSING_LIB, "closeDataCleansingChapter", ""));
                 break;
             case DC_GEOCODE_UTILITY_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_LIB, "closeGeocodeChapter", ""));
                 break;
             case DC_ZIPCODE_UTILITY_ID:
                 window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_ZIPCODE_LIB, "closeZipCodeChapter", ""));
                 break;

         }
     }

     window.scroll_to(DC_WORKING_CELL_ID);
 }


 window.control_qt_chapter = function(chapter_id) {

     var chapter_text;

     if (DEBUG_UTILS)
         console.log("control_qt_chapter", chapter_id);

     switch (chapter_id) {

         case 0:
             chapter_text = "Data Inspection";
             break;
         case 1:
             chapter_text = "Data Cleansing";
             break;
         case 2:
             chapter_text = "Data Transform";
             break;
         case 3:
             chapter_text = "Data Export";
             break;
         case 4:
             chapter_text = "Data Import";
             break;
         case 5:
             chapter_text = "System";
             break;
         case 6:
             chapter_text = "Geocode Utility";
             break;
         case 7:
             chapter_text = "Zipcode Utility";
             break;
         case 8:
             chapter_text = "Uniques Utility";
             break;
         case 9:
             chapter_text = "Outliers Utility";
             break;
         case 10:
             chapter_text = "df Browser Utility";
             break;
         case 11:
             chapter_text = "Census Utility";
             break;
     }

     var opt1 = "\n 1) Reset " + chapter_text + " Instances";
     var opt2 = "\n 2) Open " + chapter_text + " Instance";
     var opt3 = "\n 3) Close All " + chapter_text + " Instances";

     var option = window.prompt("Enter control option : " + opt1 + opt2 + opt3, "1");

     var command = -1;

     if (option.indexOf("1") > -1) command = 1;
     if (option.indexOf("2") > -1) command = 2;
     if (option.indexOf("3") > -1) command = 3;

     var dfc_chapter_id = -1;

     switch (chapter_id) {

         case 0:
             dfc_chapter_id = DC_DATA_INSPECTION_ID;
             break;
         case 1:
             dfc_chapter_id = DC_DATA_CLEANSING_ID;
             break;
         case 2:
             dfc_chapter_id = DC_DATA_TRANSFORM_ID;
             break;
         case 3:
             dfc_chapter_id = DC_DATA_EXPORT_ID;
             break;
         case 4:
             dfc_chapter_id = DC_DATA_IMPORT_ID;
             break;
         case 5:
             dfc_chapter_id = DC_SYSTEM_ID;
             break;
         case 6:
             dfc_chapter_id = DC_GEOCODE_UTILITY_ID;
             break;
         case 7:
             dfc_chapter_id = DC_ZIPCODE_UTILITY_ID;
             break;
         case 8:
             dfc_chapter_id = "Uniques Utility";
             break;
         case 9:
             dfc_chapter_id = "Outliers Utility";
             break;
         case 10:
             dfc_chapter_id = DC_DF_BROWSER_ID;
             break;
         case 11:
             dfc_chapter_id = DC_CENSUS_ID;
             break;
     }

     if (command == 1) {
         clear_dfcleanser_chapter_output(dfc_chapter_id);
         if (dfc_chapter_id == DC_GEOCODE_UTILITY_ID)
             clear_dfcleanser_chapter_output(DC_GEOCODE_BULK_ID);
     } else {
         if (command == 2)
             load_dfcleanser_chapter(dfc_chapter_id);
         else {
             if (command == 3) {
                 close_dfcleanser_chapter_instances(dfc_chapter_id);
                 if (dfc_chapter_id == DC_GEOCODE_UTILITY_ID)
                     close_dfcleanser_chapter_instances(DC_GEOCODE_BULK_ID);
             }

         }
     }

 };



 //
 // ---------------------------------------------------
 // ---------------------------------------------------
 // Dataframe Cleanser cell metadata end
 // ---------------------------------------------------
 // ---------------------------------------------------
 //


 //
 // ---------------------------------------------------
 // ---------------------------------------------------
 //     dfcleanser cell identification functions 
 // ---------------------------------------------------
 // ---------------------------------------------------
 //

 /*
  *
  *  get dfc cell pointed to by dfc id 
  * 
  *  @function get_dfc_cellid_for_cell_id 
  * 
  *     @param : cellId - cell id to select
  * 
  */

 window.get_dfc_cellid_for_cell_id = function(cellid) {
     return (dfc_cell_ids[cellid]);
 };


 /*
  *
  *  get dfc chapter element id 
  * 
  *  @function get_dfc_chapter_id 
  * 
  *     @param : cellId - cell id to select
  * 
  */

 window.get_dfc_chapter_element_id = function(chapterid) {
     return (dfc_chapter_element_ids[chapterid]);
 };



 window.get_dfc_chapter_title_html = function(chapterid) {

     var title_html = window.SYSTEM_TITLE_CELL;

     switch (chapterid) {
         case window.DC_SYSTEM_ID:
             title_html = window.SYSTEM_TITLE_CELL;
             break;
         case window.DC_SYSTEM_ID:
             title_html = window.ZIPCODE_TITLE_CELL;
             break;
         case window.DC_DATA_IMPORT_ID:
             title_html = window.DATA_IMPORT_TITLE_CELL;
             break;
         case window.DC_DATA_INSPECTION_ID:
             title_html = window.DATA_INSPECTION_TITLE_CELL;
             break;
         case window.DC_DATA_CLEANSING_ID:
             title_html = window.DATA_CLEANSING_TITLE_CELL;
             break;
         case window.DC_DATA_TRANSFORM_ID:
             title_html = window.DATA_TRANSFORM_TITLE_CELL;
             break;
         case window.DC_DATA_EXPORT_ID:
             title_html = window.DATA_EXPORT_TITLE_CELL;
             break;
         case window.DC_ZIPCODE_UTILITY_ID:
             title_html = window.ZIPCODE_TITLE_CELL;
             break;
         case window.DC_GEOCODE_UTILITY_ID:
             title_html = window.GEOCODE_TITLE_CELL;
             break;
         case window.DC_CENSUS_ID:
             title_html = window.CENSUS_TITLE_CELL;
             break;
     }

     return (title_html);
 };


 /*
  *
  *  get cell pointed to by logical id 
  * 
  *  @function get_cell_for_id
  * 
  *    @param : cellId - cell id to select
  * 
  */
 window.get_cell_for_id = function(cellId) {

     // get the current cells 
     var cells = IPython.notebook.get_cells();
     var cell = null;

     if (cellId == POPUP_CELL_ID) {
         return (get_popupcodecell());
     }

     // search through the cells 
     for (var i = 0; i < (IPython.notebook.ncells()); i++) {
         cell = cells[i];
         var cellIndex = IPython.notebook.find_cell_index(cell);

         // check that cell index is valid
         if (IPython.notebook.is_valid_cell_index(cellIndex)) {
             // get the cell metadata 
             var cell_mdata = cell.metadata;

             if (cell_mdata != undefined) {
                 if ("dfcleanser_metadata" in cell_mdata) {

                     var dfc_cell_mdata = cell_mdata["dfcleanser_metadata"];
                     if ("dfc_cellid" in dfc_cell_mdata) {
                         var dfc_cell_id = dfc_cell_mdata["dfc_cellid"];

                         if (get_dfc_cellid_for_cell_id(cellId) == dfc_cell_id)
                             return (cell);
                     }
                 }
             }
         }
         cell = null;
     }
     return (cell);
 };


 /*
  *
  *  get cell before cell pointed to by logical id 
  * 
  *  @function get_cell_for_before_id
  * 
  *    @param : cellId - cell id to select
  * 
  */
 window.get_cell_for_before_id = function(cellId) {

     // get the current cells 
     var cells = IPython.notebook.get_cells();
     var cell = null;
     var prev_cell = null;

     // search through the cells 
     for (var i = 0; i < (IPython.notebook.ncells()); i++) {
         cell = cells[i];
         var cellIndex = IPython.notebook.find_cell_index(cell);

         // check that cell index is valid
         if (IPython.notebook.is_valid_cell_index(cellIndex)) {
             // get the cell metadata 
             var cell_mdata = cell.metadata;

             if ((cell_mdata != undefined) && ("dfcleanser_metadata" in cell_mdata)) {
                 var dfc_cell_mdata = cell_mdata["dfcleanser_metadata"];
                 if ("dfc_cellid" in dfc_cell_mdata) {
                     var dfc_cell_id = dfc_cell_mdata["dfc_cellid"];
                     if (dfc_cell_id == cellId) {
                         return (prev_cell);
                     } else prev_cell = cell;
                 } else prev_cell = cell;
             } else prev_cell = cell;
         } else cell = null;
     }

     return (cell);
 };

 /*
  *
  *  select cell pointed to by logical id 
  * 
  *  @function select_cell
  * 
  *    @param : id - cell id to select
  * 
  */
 window.select_cell = function(id) {
     var cell_to_select = window.get_cell_for_id(id);
     select_current_cell(cell_to_select);
 };


 /*
  *
  *  selectthe cell before cell pointed to by logical id 
  * 
  *  @function select_before_cell
  * 
  *    @param : id - cell id to select
  * 
  */
 window.select_before_cell = function(id) {

     if (DEBUG_DETAILS_UTILS)
         console.log("select_before_cell", id);

     var cell_to_select = window.get_cell_for_before_id(id);
     select_current_cell(cell_to_select);
 };


 /*
  *
  *  set the cell pointed to by logical id 
  *  as the currently selected ipyhton cell with focus
  * 
  *  @function select_current_cell
  * 
  *  @param : cell_to_select - cell to focus
  * 
  */
 window.select_current_cell = function(cell_to_select) {

     if (DEBUG_DETAILS_UTILS)
         console.log("select_current_cell", cell_to_select);

     var cellIndex = IPython.notebook.find_cell_index(cell_to_select);
     IPython.notebook.select(cellIndex, true);
     IPython.notebook.focus_cell();
     cell_to_select.select(true);
 };

 /*
  *
  *  select cell from its metadata
  * 
  *  @function select_cell_from_metadata
  * 
  *  @param : metadata - cell metadata to search for
  * 
  */
 window.select_cell_from_metadata = function(metadata, offset = 0) {

     if (DEBUG_CELL_UTILS)
         console.log(log_prefix + "\n" + "     select_cell_from_metadata : metadata : offset ", metadata, offset);

     var cells = IPython.notebook.get_cells();
     var cellIndex = null;

     for (var i = 0; i < (IPython.notebook.ncells()); i++) {
         var cell = cells[i];
         var cmdata = cell.metadata;
         var dfc_mdata = cmdata["dfcleanser_metadata"];

         if (DEBUG_CELL_UTILS)
             console.log(log_prefix + "\n" + "     select_cell_from_metadata : dfc_mdata ", i, dfc_mdata);

         if (dfc_mdata != undefined) {
             var dfc_cell_id = dfc_mdata["dfc_cellid"];

             if (DEBUG_CELL_UTILS)
                 console.log(log_prefix + "\n" + "     select_cell_from_metadata : dfc_cell_id ", dfc_cell_id, dfc_cell_id.length);
             console.log(log_prefix + "\n" + "     select_cell_from_metadata : metadata ", metadata, metadata.length);

             if (dfc_cell_id == metadata) {

                 if (DEBUG_CELL_UTILS)
                     console.log(log_prefix + "\n" + "     select_cell_from_metadata : metadata : dfc_cell_id ", metadata, dfc_cell_id);

                 for (var j = 0; j < offset; j++) {
                     cell = cells[i + j + 1]; //IPython.notebook.select_next().get_selected_cell();
                     select_current_cell(cell);
                 }
                 select_current_cell(cell);

                 if (DEBUG_CELL_UTILS)
                     console.log(log_prefix + "\n" + "     select_cell_from_metadata : cell ", cell);

                 return (cell);
             }
         }
     }
 };

 //
 // ---------------------------------------------------
 // ---------------------------------------------------
 //   dfcleanser cell identification functions end
 // ---------------------------------------------------
 // ---------------------------------------------------
 //




 //
 // ---------------------------------------------------
 // ---------------------------------------------------
 //         dfcleanser cell control functions 
 // ---------------------------------------------------
 // ---------------------------------------------------
 //


 /*
  *
  *  delete the dfcleanser cell by id.
  * 
  *  @function delete_output_cell
  * 
  *  @param : id - cell id
  * 
  */
 window.delete_output_cell = function(id) {

     if (get_dfc_mode() == 1)
         return;

     var cell_to_delete = null;
     var cell_to_return_to = null;
     cell_to_delete = window.get_cell_for_id(id);

     if (cell_to_delete != window.empty_cell_id) {
         select_cell(id);
         cell_to_return_to = IPython.notebook.select_next().get_selected_cell()
         IPython.notebook.delete_cell(IPython.notebook.find_cell_index(cell_to_delete));
     }
     IPython.notebook.select(cell_to_return_to);
 };

 /*
  *
  *  run code in the dfcleanser cell
  * 
  *  @function run_code_in_cell
  * 
  *   @param : id   - cell id
  *   @param : code - python code to run
  * 
  */
 window.run_code_in_cell = function(id, code) {

     if (DEBUG_UTILS) {
         console.log("run_code_in_cell id = ", id);
         console.log("run_code_in_cell code = ", code);
         console.log("run_code_in_cell DC_WORKING_CELL_ID = ", DC_WORKING_CELL_ID);
         console.log("run_code_in_cell get_dfc_mode() = ", get_dfc_mode());
     }

     var runCell = null;

     if (get_dfc_mode() == 1) {
         if (id == WORKING_CELL_ID)
             runCell = window.get_cell_for_id(id);
         else {
             if ((id == SW_UTILS_DATASTRUCT_TASK_BAR_ID) || (id == SW_UTILS_GEOCODE_TASK_BAR_ID) ||
                 (id == SW_UTILS_DFSUBSET_TASK_BAR_ID) || (id == SW_UTILS_CENSUS_TASK_BAR_ID) || (id == SCRIPT_TASK_BAR_ID))
                 runCell = window.get_cell_for_id(id);
             else
                 runCell = get_popupcodecell();
         }
     } else {
         runCell = window.get_cell_for_id(id);
     }

     if (DEBUG_DETAILS_UTILS)
         console.log("run_code_in_cell : runCell", runCell);


     var runCode = code;

     if (id == POPUP_CELL_ID)
         if (DEBUG_UTILS)
             console.log("run_code_in_cell", runCell, runCode);

     if (runCell != null) {
         if (id == window.DC_WORKING_CELL_ID) {
             runCode = WORKING_CELL + "- please do not remove" + NEW_LINE + code;
             if (DEBUG_UTILS)
                 console.log(log_prefix + "\n" + "     run_code_in_cell : WORKING CELL ", runCode);
             run_code(runCell, runCode);
         } else { run_code(runCell, runCode); }
     } else {
         if (DEBUG_UTILS)
             console.log(log_prefix + "\n" + "     Cell to run in not found", id, code);
     }
 };

 /*
  *
  *  run code in the dfcleanser cell
  * 
  *  @function insert_cell_and_run_code_in_output_cell
  * 
  *   @param : id         - cell id
  *   @param : outputid   - cell id for new cell
  *   @param : code       - python code to run
  * 
  */
 window.insert_cell_and_run_code_in_output_cell = function(id, outputid, code) {

     window.delete_output_cell(outputid);
     window.select_cell(id);
     IPython.notebook.insert_cell_below('code');
     var cell = IPython.notebook.select_next().get_selected_cell();
     window.run_code(cell, code);

     if (DEBUG_DETAILS_UTILS) {
         console.log(log_prefix + "\n" + "     insert_cell_and_run_code_in_output_cell", id, outputid, code);
     }
 };

 /*
  *
  *  clear cell output in the dfcleanser cell
  * 
  *  @function clear_cell_output
  * 
  *   @param : id         - cell id
  * 
  */
 window.clear_cell_output = function(id) {

     if (get_dfc_mode() == 1)
         var cell_to_clear = get_popupcodecell();
     else
         var cell_to_clear = window.get_cell_for_id(id);

     if (cell_to_clear != window.empty_cell_id) {
         IPython.notebook.clear_output(IPython.notebook.find_cell_index(cell_to_clear));
     } else {
         if (DEBUG_DETAILS_UTILS)
             console.log(log_prefix + "\n" + "     clear_cell_output : fail", id);
     }
 };


 /*
  *
  *  run code in noteboook cell
  * 
  *  @function run_code
  * 
  *   @param : cell          -   noteboook cell to run code in
  *   @param : code          -   code to run in cell
  * 
  */
 window.run_code = function(cell, code) {
     cell.set_text(code);
     cell.execute();
 };



 //
 // ---------------------------------------------------
 // ---------------------------------------------------
 //      dfcleanser cell control functions end
 // ---------------------------------------------------
 // ---------------------------------------------------
 //



 function process_pop_up_cmd(chid) {
     /**
      * pop up main task bar calls.
      *
      * Parameters:
      *  fid
      *      System Environment function id
      */

     if (DEBUG_UTILS)
         if (chid == 6)
             console.log(log_prefix + "\n" + "     process_pop_up_cmd : reset dfc");

     var code = null;

     switch (chid) {
         case 1:
             code = "from dfcleanser.Qt.data_import.Dataimport import showDataImport" + window.NEW_LINE;
             code = code + "showDataImport()";
             break;
         case 6:
             if (get_dfc_mode() == 0) {
                 load_dfcleanser_chapter(0);
                 return;
             } else {
                 code = "from dfcleanser.system.load import load_pop_up_startup" + NEW_LINE;
                 code = code + "load_pop_up_startup()";
             }
             break;
     }

     window.delete_output_cell(window.POPUP_CELL_ID);
     var cell = get_cell_for_id(window.POPUP_CELL_ID);
     run_code(cell, code);

     window.shut_off_autoscroll();

 }

 //
 // ---------------------------------------------------
 // end cell control functions 
 // ---------------------------------------------------
 //



 /* 
 // -------------------------------------------------------
 // -------------------------------------------------------
 //         dfcleanser load and unload functions
 // ------------------------------------------------------
 // -------------------------------------------------------
 */

 var dfc_mode = 0;

 window.get_dfc_mode = function() {
     return (dfc_mode);
 };



 /*
  *
  *  Load the dfcleanser utility from the toolbar icon.
  *  @function load_dfcleanser_from_toolbar
  * 
  */
 window.load_dfcleanser_from_toolbar = function() {
     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     load_dfcleanser_from_toolbar");

     var internet_available = $.get("https://rickkrasinski.github.io/dfcleanser/graphics/Restricted.jpg")
         .done(function() {
             return (true);
         }).fail(function() {
             return (false);
         });

     if (DEBUG_UTILS)
         console.log("internet_available", internet_available);

     add_dfcleanser_working_chapter();

     window.shut_off_autoscroll();

     var nbname = IPython.notebook.get_notebook_name();

     if (DEBUG_UTILS)
         console.log("load_dfcleanser_from_toolbar - run_code_in_cell")

     window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_CONSOLE_LIB, "load_dfcleanser_from_toolbar", JSON.stringify([nbname])));
 }

 /*
  *
  *  check if dfcleanser is currently loaded
  *  @function is_dfcleanser_loaded
  * 
  */
 window.is_dfcleanser_loaded = function() {

     var cells = IPython.notebook.get_cells();

     // search through the cells 
     for (var i = 0; i < (IPython.notebook.ncells()); i++) {

         var cell = cells[i];
         var cmdata = cell.metadata;
         var dfc_mdata = cmdata["dfcleanser_metadata"];

         if (dfc_mdata != undefined) { return (true); }
     }

     return (false);
 };

 /* 
 // -------------------------------------------------------
 // -------------------------------------------------------
 //        dfcleanser load and unload functions end
 // ------------------------------------------------------
 // -------------------------------------------------------
 */


 /* 
 // -------------------------------------------------------
 // -------------------------------------------------------
 //         dfcleanser jupyter cell functions 
 // -------------------------------------------------------
 // ------------------------------------------------------
*/


 const MARKDOWN = 0
 const CODE = 1

 /*
  *
  *  add a dfcleanser cell to the notebook
  * 
  *  @function add_dfc_cell
  * 
  *   @param : ctype    - cell type
  *   @param : ctext    - cell text
  *   @param : dfcid    - dfcleanser metadata id
  * 
  */
 window.add_dfc_cell = function(ctype, ctext, dfcid, afterid = -1) {
     if (DEBUG_DETAILS_UTILS)
         if (ctype == 0)
             console.log(log_prefix + "\n" + "     add_dfc_cell MARKDOWN ", dfcid, afterid);
         else
             console.log(log_prefix + "\n" + "     add_dfc_cell CODE CELL ", dfcid, afterid);

         // if first cell to load find correct 
         // cell to start loading after
     if (afterid != -1) {
         select_cell(afterid);
     }

     if (ctype == CODE) {
         IPython.notebook.insert_cell_below('code');
     } else {
         IPython.notebook.insert_cell_below('markdown');
     }

     var cell_to_add = IPython.notebook.select_next().get_selected_cell();
     cell_to_add.set_text(ctext);

     if (DEBUG_UTILS)
         console.log("add_dfc_cell", cell_to_add, ctext);

     // add the cellid metadata
     var dfcellDict = { "dfc_cellid": dfcid };
     var dfcleanserDict = { "dfcleanser_metadata": dfcellDict };
     var newcellDict = { "trusted": true, "scrolled": false, "dfcleanser_metadata": dfcellDict };
     cell_to_add.metadata = newcellDict; //dfcleanserDict;

     if (ctype == MARKDOWN) { cell_to_add.execute(); } else { cell_to_add.execute(); }

     if (DEBUG_DETAILS_UTILS)
         console.log("add_dfc_cell", cell_to_add)
 };

 /*
  *
  *  find the number of dfcleanser cells
  * 
  *  @function get_num_dfcleanser_cells
  * 
  */
 window.get_num_dfcleanser_cells = function() {

     var cells = IPython.notebook.get_cells();
     var total_dfc_cells = 0;

     for (var i = 0; i < (IPython.notebook.ncells()); i++) {
         var cell = cells[i];
         var cmdata = cell.metadata;
         var dfc_mdata = cmdata["dfcleanser_metadata"];

         if (dfc_mdata != undefined) { total_dfc_cells++; }
     }
     return (total_dfc_cells);
 };

 /*
  *
  *  get the metadata for a dfc cell
  * 
  *  @function get_dfc_metadata
  * 
  *   @param : cell    - cell to get metadata from
  * 
  */
 window.get_dfc_metadata = function(cell) {
     var cmdata = cell.metadata;
     var dfc_mdata = cmdata["dfcleanser_metadata"];
     if (dfc_mdata != undefined) return (dfc_mdata);
     else return (undefined);
 }

 /*
  *
  *  delete the dfc cell
  * 
  *  @function delete_dfc_cell
  * 
  *   @param : cell_to_delete    - cell to delete
  * 
  */

 window.delete_dfc_cell = function(cell_to_delete) {

     if (true) //window.debug_load_flag)
         console.log(log_prefix + "\n" + "     delete_dfc_cell", cell_to_delete);

     var cellid = select_cell_from_metadata(cell_to_delete);
     if (true) //window.debug_load_flag)
         console.log(log_prefix + "\n" + "     cellid", cellid);


     IPython.notebook.delete_cell(IPython.notebook.find_cell_index(cellid));
 }

 /*
  *
  *  delete the dfc chapter cells
  * 
  *  @function delete_dfc_chapter
  * 
  *   @param : chaptertitle    - chapter cells to delete
  * 
  */
 window.delete_dfc_chapter = function(chaptertitle) {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     delete_dfc_chapter", chaptertitle);

     var cell_to_delete = null;
     var next_cell = null;
     cell_to_delete = select_cell_from_metadata(chaptertitle)

     // delete the title cell
     if (cell_to_delete != window.empty_cell_id) {
         select_current_cell(cell_to_delete);
         next_cell = IPython.notebook.select_next().get_selected_cell();
         IPython.notebook.delete_cell(IPython.notebook.find_cell_index(cell_to_delete));
     }

     if (window.debug_load_flag)
         console.log(log_prefix + "\n" + "     delete_dfc_chapter : delete title", cell_to_delete);

     // delete the code cell 
     cell_to_delete = next_cell;
     select_current_cell(cell_to_delete);
     next_cell = IPython.notebook.select_next().get_selected_cell();
     var dfc_codetext = cell_to_delete.get_text();

     if (containsSubstring(dfc_codetext, "from dfcleanser."))
         IPython.notebook.delete_cell(IPython.notebook.find_cell_index(cell_to_delete));
     else
         next_cell = cell_to_delete;

     // delete the blank line cell 
     cell_to_delete = next_cell;
     select_current_cell(cell_to_delete);
     next_cell = IPython.notebook.select_next().get_selected_cell();

     var dfc_metadata = get_dfc_metadata(cell_to_delete);

     if (dfc_metadata != undefined) {
         var dfcid = dfc_metadata["dfc_cellid"];
         if (dfcid != undefined) {
             if (containsSubstring(dfcid, "DCBlankline"))
                 IPython.notebook.delete_cell(IPython.notebook.find_cell_index(cell_to_delete));
         }
     }

     IPython.notebook.select(next_cell);
 };

 /*
  *
  *  delete all dfc cells
  * 
  *  @function delete_dfcleanser_cells
  * 
  */
 window.delete_dfcleanser_cells = function() {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     delete_dfcleanser_cells");

     var cells = IPython.notebook.get_cells();
     var cell = window.empty_cell_id;

     // search through the cells 
     for (var i = 0; i < (IPython.notebook.ncells()); i++) {
         cell = cells[i];
         var cmdata = cell.metadata;
         var dfc_mdata = cmdata["dfcleanser_metadata"];

         if (dfc_mdata != undefined) {
             var cellIndex = IPython.notebook.find_cell_index(cell);
             IPython.notebook.select(cellIndex, true);
             IPython.notebook.focus_cell();
             cell.select(true);
             IPython.notebook.delete_cell(cellIndex);
         }
     }
 };

 /* 
 // -------------------------------------------------------
 // -------------------------------------------------------
 //      dfcleanser jupyter cell functions end
 // -------------------------------------------------------
 // ------------------------------------------------------
*/


 //
 // ---------------------------------------------------
 // ---------------------------------------------------
 //           common uility functions
 // ---------------------------------------------------
 // ---------------------------------------------------
 //

 //
 // check if element has attribute
 //
 window.has_Attribute = function(elem, cattr) {
     var cattr = elem.attr(cattr);
     if (typeof cattr !== typeof undefined && cattr !== false) return (true);
     else return (false);
 };

 //
 // scroll to a chapter in the notebook
 //
 window.scroll_to = function(chapterid) {

     var element_to_scroll_to = document.getElementById(get_dfc_chapter_element_id(chapterid));

     if (element_to_scroll_to != null) element_to_scroll_to.scrollIntoView();

 };

 window.handlecbcheck = function(cb) {
     if (DEBUG_DETAILS_UTILS)
         console.log("handlecbcheck", cb);
 };

 //
 // check if string contains a substring
 //
 function containsSubstring(instr, insubstr) {
     var flag = instr.indexOf(insubstr);
     if (flag == -1) return (false);
     else return (true);
 }


 //
 // -----------------------------------------------------
 // helper functions for running python methods from js
 // -----------------------------------------------------
 //
 window.getJCode = function(code) {
     return (code + NEW_LINE);
 };
 window.getJSCode = function(lib, call) {
     return (lib + call + NEW_LINE + call + "()");
 };
 window.getJSPCode = function(lib, call, parm) {
     return (lib + call + NEW_LINE + call + "(" + parm + ")");
 };



 // -----------------------------------------------------
 // helper html functions 
 // -----------------------------------------------------



 //
 //
 // ---------------------------------------------------
 // helper functions for getting form input data
 // ---------------------------------------------------
 // 
 //

 // 
 // Common get values for checkboxes
 // 
 window.getcheckboxValues = function(id) {
     var formd = document.getElementById(id);

     if (formd == null) {
         if (DEBUG_DETAILS_UTILS)
             console.log("no checkbox ", id, " not found");
         return (null);
     }

     var inputs = new Array();
     $('#' + id + ' :input').each(function() {
         var type = $(this).attr("type");
         if (type == "checkbox")
             var id = $(this).attr("id");
         if ($(this).is(':checked')) { inputs.push("True"); } else { inputs.push("False"); }
     });
     return (JSON.stringify(inputs));
 };

 // 
 // Common get values for radios
 // 
 window.getradioValues = function(id) {
     var formd = document.getElementById(id);

     if (formd == null) {
         if (DEBUG_DETAILS_UTILS)
             console.log("no radio ", id, " not found");
         return (null);
     }

     var inputs = new Array();
     var total_found = -1;
     var found_at = -1;

     $('#' + id + ' :input').each(function() {
         total_found = total_found + 1;
         var type = $(this).attr("type");
         if (type == "radio")
             var id = $(this).attr("id");
         if ($(this).is(':checked')) {
             found_at = total_found;
         }
     });
     inputs.push(found_at);
     return (JSON.stringify(found_at));
 };

 // 
 // Common get value for dropdown
 // 
 window.getdropdownValues = function(id) {
     var formd = document.getElementById(id);

     if (formd == null) {
         return (null);
     }

     var inputs = new Array();
     var total_found = -1;
     var found_at = -1;

     $('#' + id + ' option').each(function() {
         total_found = total_found + 1;
         var sel = $(this).prop("selected");
         if (sel == true) {
             found_at = total_found;
         }
     });
     inputs.push(found_at);
     return (JSON.stringify(found_at));
 };

 // 
 // Common get values for input forms
 // 
 window.get_input_form_parms = function(fid) {

     var inputs = new Array();
     var ids = new Array();

     $('#' + fid + ' :input').each(function() {
         var type = $(this).attr("type");

         if ((type != "file") && (type != "button")) {
             if (String($(this).val()).length > 0) {
                 inputs.push(String($(this).val()));
                 ids.push(String($(this).attr("id")));
             }
         }
     });

     var parms = new Array();
     parms.push(ids);
     parms.push(inputs);

     return (JSON.stringify(parms));
 };

 // 
 // Common get labels for input forms
 // 
 window.get_input_form_labels = function(id) {

     var inputs = new Array();
     $('#' + id + ' :input').each(function() {
         var $element = $(this)
         var $label = $("label[for='" + $element.attr('id') + "']")
         inputs.push(String($label.text()));
     });

     return (JSON.stringify(inputs));
 };


 //
 // function to request a full list of parms for an inout form
 //
 window.getfullparms = function(inputid) {

     switch (inputid) {

         case "arcgisgeocoder":
         case "googlegeocoder":
         case "binggeocoder":
         case "baidugeocoder":
         case "mapquestgeocoder":
         case "nomingeocoder":
         case "arcgisquery":
         case "googlequery":
         case "bingquery":
         case "databcquery":
         case "mapquestquery":
         case "nominquery":
         case "arcgisreverse":
         case "bingreverse":
         case "nominreverse":
         case "googlereverse":
         case "arcgisbatchgeocoder":
         case "baidubulkgeocoder":
         case "googlebulkgeocoder":
         case "bingbulkgeocoder":
         case "mapquestbulkgeocoder":
         case "nominbulkgeocoder":
         case "arcgisbatchquery":
         case "bingbulkquery":
         case "mapquestbulkquery":
         case "nominatimbulkquery":
         case "googlebulkreverse":

             var inputs = new Array();
             inputs.push(String(inputid));
             window.run_code_in_cell(window.DC_GEOCODE_UTILITY_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_LIB, "display_geocode_utility", "12" + ", " + JSON.stringify(inputs)));
             window.scroll_to(DC_GEOCODE_UTILITY_ID);
             break;

         case "googlebulkquery":

             var inputs = new Array();
             inputs.push(String(inputid));

             var tableid = $('#gegdfltypesTable');

             if (DEBUG_DETAILS_UTILS)
                 console.log("tableid", tableid);
             if (tableid == null)
                 inputs.push(String(0));
             else
                 inputs.push(String(6));

             window.run_code_in_cell(window.DC_GEOCODE_UTILITY_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_LIB, "display_geocode_utility", "12" + ", " + JSON.stringify(inputs)));
             window.scroll_to(DC_GEOCODE_UTILITY_ID);
             break;

         default:
             var inputs = new Array();
             inputs.push(String(inputid));
             window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "get_fullparms", JSON.stringify(inputs)));
             break;
     }
 };


 window.set_select_disable = function(selectid, option) {
     if (option == "Enable") {
         $('#' + selectid).removeAttr('disabled');
     } else {
         $('#' + selectid).attr('disabled', 'disabled');
     }
 };

 //
 // ----------------------------------------------------------
 // file selection directory - dirs restricted to local only
 // Note : adhere to the browser security usage of fakepath
 // ---------------------------------------------------------
 // 
 window.onChangefileselect = function(inputid, fileid) {

     var input = document.getElementById(inputid);
     var file = document.getElementById(fileid);

     if (DEBUG_DETAILS_UTILS)
         console.log("onChangefileselect", input, file);

     if (inputid == "addcolumnfilename") input.value = file.value.replace("C:\\fakepath\\", "");
     else input.value = file.value.replace("C:\\fakepath\\", "datasets/");
 };




 //
 // ---------------------------------------------------------
 // ---------------------------------------------------------
 // common functions for jupyter to javascript coordination
 // ---------------------------------------------------------
 // ---------------------------------------------------------
 //

 //
 // get the current notebook name
 // 
 window.getNotebookName = function() {

     var nbname = IPython.notebook.get_notebook_name();

     if (window.get_cell_for_id(window.DC_WORKING_CELL_ID) == null) {
         window.add_dfc_cell(1, "# Temporary Working Cell", "DCWorking");
         window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.CFG_LIB, "set_notebookName", JSON.stringify(nbname)));
         window.delete_output_cell(window.DC_WORKING_CELL_ID);
     } else {
         window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.CFG_LIB, "set_notebookName", JSON.stringify(nbname)));
     }
 };

 //
 // get the current notebook path
 // 
 window.getNotebookPath = function() {

     var code = "dcpath = %pwd" + NEW_LINE;
     code = code + "from dfcleanser.common.cfg import set_notebookPath" + NEW_LINE;
     code = code + "set_notebookPath(dcpath)";
     if (window.get_cell_for_id(window.DC_WORKING_CELL_ID) == null) {
         window.add_dfc_cell(1, "# Temporary Working Cell", "DCWorking");
         window.run_code_in_cell(window.DC_WORKING_CELL_ID, code);
         window.delete_output_cell(window.DC_WORKING_CELL_ID);
     } else {
         window.run_code_in_cell(window.DC_WORKING_CELL_ID, code);
     }
 };

 window.saveCurrentNotebook = function() {
     IPython.notebook.save_checkpoint();
     console.log(log_prefix + "\n" + "     dfc checkpoint");
 };



 window.select_chapter_df = function(selectid) {
     /**
      * select a chapter
      *
      * Parameters:
      */

     var dfname = $("#" + selectid).val();

     var parms = new Array();
     parms.push(selectid);
     parms.push(dfname);

     window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "set_chapter_df", JSON.stringify(parms)));
 };


 //
 // ---------------------------------------------------
 //            common help functions
 // ---------------------------------------------------
 //


 //
 // display help by url
 //
 window.display_help_url = function(url) {
     console.log("url", url);
     window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "display_url", JSON.stringify(url)));
     //#return true;
 };

 //
 // display inline help 
 //
 window.display_inline_help = function(noteid, txtmsg) {
     var noteobj = noteid.text(txtmsg);
     noteobj.html(noteobj.html().replace(/\n/g, '<br/>'));
     noteid.css('color', '#67a1f3');
 };

 //
 // sync with Jupyter
 //
 window.sync_notebook = function() {

     var nbname = IPython.notebook.get_notebook_name();
     var inputs = new Array();
     inputs.push(nbname);
     window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.CFG_LIB, "sync_with_js", JSON.stringify(inputs)));

     if (is_dfcleanser_chapter_loaded(DC_CONSOLE_ID)) {
         load_dfcleanser_chapter(DC_CONSOLE_ID);
     }
 };

 //
 // log Jupyter message
 //
 window.log_jupyter_msg = function(message) {
     console.log(log_prefix + "\n" + "     " + message);
 };

 $(document).ready(function() {

     if (!dfc_loaded_flagged) {
         console.log("document ready");
     }
 });


 function add_select_val(selectid, textid) {

     var colname = $("#" + selectid).val();
     var currentColumns = $("#" + textid);

     if (currentColumns.val().indexOf('[') < 0) {
         var newColumns = "[" + colname + "]";
         currentColumns.val(newColumns);
     } else {
         newColumns = currentColumns.val();
         var newColumns = newColumns.replace("]", "," + colname + "]")
         currentColumns.val(newColumns);
     }
 }


 //
 // ------------------------------------------------------
 // ----- dfcleanser chapter maintenance utilities -------
 // ------------------------------------------------------
 //



 /*
  *
  *  check if a dfcleanser chapter is loaded
  * 
  *  @function is_dfcleanser_chapter_loaded
  * 
  *  @param : chapterid
  * 
  */
 function is_dfcleanser_chapter_loaded(chapterid) {

     if (DEBUG_DETAILS_UTILS)
         console.log(log_prefix + "\n" + "     " + "is_dfcleanser_chapter_loaded", chapterid);

     var cells = IPython.notebook.get_cells();
     var cellIndex = null;
     var chapter_metadata = get_dfcleanser_chapter_metadata(chapterid);

     for (var i = 0; i < (IPython.notebook.ncells()); i++) {

         var cell = cells[i];
         var cmdata = cell.metadata;
         var dfc_mdata = cmdata["dfcleanser_metadata"];

         if (dfc_mdata != undefined) {
             var dfc_cell_id = dfc_mdata["dfc_cellid"];

             if (dfc_cell_id == chapter_metadata) {
                 return (true);
             }
         }
     }

     return (false);
 }


 /*
  *
  *  add a dfcleanser chapter
  * 
  *  @function add_dfcleanser_chapter
  * 
  *  @param : chapterid
  * 
  */
 function add_dfcleanser_chapter(chapterid) {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     " + "add_dfcleanser_chapter", chapterid);

     if (chapterid == DC_CENSUS_ID) {
         display_dfc_status("Census Under Construction")
         return;
     }

     if (!is_dfcleanser_chapter_loaded(chapterid)) {

         var chapter_metadata = get_dfcleanser_chapter_metadata(chapterid);

         if (DEBUG_UTILS)
             console.log(log_prefix + "\n" + "     " + "add_dfcleanser_chapter", chapter_metadata);

         var insert_pont = find_dfcleanser_next_chapter_insert_point();

         add_dfc_cell(CODE, window.WORKING_CODE_CELL, chapter_metadata, -1);

         var delayInMilliseconds = 500; //1 second

         setTimeout(function() {
             if ((chapterid == DC_CONSOLE_ID)) {
                 load_dfcleanser_chapter(chapterid)
                 if (DEBUG_UTILS)
                     console.log(log_prefix + "\n" + "     " + "[add_dfcleanser_chapter][load_dfcleanser_chapter]", chapterid);

             } else
                 clear_dfcleanser_chapter_output(chapterid)
         }, delayInMilliseconds);


     } else {
         if ((chapterid == DC_CONSOLE_ID) || (chapterid == DC_CONSOLE_ID))
             load_dfcleanser_chapter(chapterid)
         else
             clear_dfcleanser_chapter_output(chapterid)
     }

     window.scroll_to(chapterid);

 }


 /*
  *
  *  add the dfcleanser working chapter
  * 
  *  @function add_dfcleanser_working_chapter
  * 
  *  @param : 
  * 
  */
 function add_dfcleanser_working_chapter() {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     " + "add_dfcleanser_working_chapter");

     if (!is_dfcleanser_chapter_loaded(DC_WORKING_CELL_ID)) {

         add_dfc_cell(MARKDOWN, window.WORKING_BLANK_LINE, 'DCWorking_DCBlankline', -1);
         add_dfc_cell(MARKDOWN, window.WORKING_TITLE_CELL, 'DCWorkingTitle', -1);
         add_dfc_cell(CODE, window.WORKING_CODE_CELL, 'DCWorking', -1);
         add_dfc_cell(MARKDOWN, window.WORKING_BLANK_LINE, 'DCWorking_DCBlankline_1', -1)

         window.sync_notebook();
     }
 }



 /*
  *
  *  close a dfcleanser chapter
  * 
  *  @function close_dfcleanser_chapter
  * 
  *  @param : chapterid
  * 
  */
 function close_dfcleanser_chapter(chapterid) {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     " + "close_dfcleanser_chapter", chapterid);

     if (is_dfcleanser_chapter_loaded(chapterid)) {

         var dfc_cellid = get_dfcleanser_chapter_metadata(chapterid);
         var dfc_blank_cellid = dfc_cellid + "_BlankLine";

         if (DEBUG_UTILS)
             console.log(log_prefix + "\n" + "     " + "close_dfcleanser_chapter", dfc_cellid, dfc_blank_cellid);

         var cell_to_delete = select_cell_from_metadata(dfc_blank_cellid);
         IPython.notebook.delete_cell(IPython.notebook.find_cell_index(cell_to_delete));

         cell_to_delete = select_cell_from_metadata(dfc_cellid);
         IPython.notebook.delete_cell(IPython.notebook.find_cell_index(cell_to_delete));

         if (chapterid == DC_WORKING_CELL_ID) {

             dfc_cellid = get_dfcleanser_chapter_metadata(DC_WORKING_TITLE_ID);

             var cell_to_delete = select_cell_from_metadata(dfc_cellid);
             IPython.notebook.delete_cell(IPython.notebook.find_cell_index(cell_to_delete));

             dfc_cellid = get_dfcleanser_chapter_metadata(DC_WORKING_CELL_ID);
             var dfc_blank_cellid = dfc_cellid + "_BlankLine_1";

             var cell_to_delete = select_cell_from_metadata(dfc_blank_cellid);
             IPython.notebook.delete_cell(IPython.notebook.find_cell_index(cell_to_delete));

         }

     }

 }


 /*
  *
  *  find next cell to insert chapter after
  * 
  *  @function find_dfcleanser_next_chapter_insert_point
  * 
  *  @param : 
  * 
  */
 window.find_dfcleanser_next_chapter_insert_point = function() {

     if (DEBUG_DETAILS_UTILS)
         console.log(log_prefix + "\n" + "     find_dfcleanser_next_cell_insert_point");

     var cells = IPython.notebook.get_cells();
     var cellIndex = null;

     for (var i = 0; i < (IPython.notebook.ncells()); i++) {
         var cell = cells[i];
         var cmdata = cell.metadata;

         if (DEBUG_DETAILS_UTILS)
             console.log(log_prefix + "\n" + "     find_dfcleanser_next_cell_insert_point : cmdata", i, cmdata);

         if (!(cmdata == undefined)) {

             var dfc_mdata = cmdata["dfcleanser_metadata"];

             if (DEBUG_DETAILS_UTILS)
                 console.log(log_prefix + "\n" + "     find_dfcleanser_next_cell_insert_point : dfc_mdata", dfc_mdata);

             if (!(dfc_mdata == undefined)) {
                 var dfc_cell_id = dfc_mdata["dfc_cellid"];

                 if (DEBUG_DETAILS_UTILS)
                     console.log(log_prefix + "\n" + "     find_dfcleanser_next_cell_insert_point : dfc_cell_id", dfc_cell_id);


                 if (dfc_cell_id == 'DCWorking_DCBlankline') {

                     if (DEBUG_DETAILS_UTILS)
                         console.log(log_prefix + "\n" + "     find_dfcleanser_next_cell_insert_point : cell found", i);

                     if (i > 0) {
                         var foundcell = cells[i - 1];

                         if (DEBUG_DETAILS_UTILS)
                             console.log(log_prefix + "\n" + "     find_dfcleanser_next_cell_insert_point : cell found", foundcell);

                         select_current_cell(foundcell);
                         return (foundcell);
                     } else {
                         return (null);
                     }
                 }
             }
         }
     }

     return (null);
 };


 /*
  *
  *  get metadata for dfcleanser chapter
  * 
  *  @function get_dfcleanser_chapter_metadata
  * 
  *  @param : chapterid 
  * 
  */
 window.get_dfcleanser_chapter_metadata = function(chapterid) {

     return (dfc_cell_ids[chapterid]);
 }


 /*
  *
  *  get cell id for dfcleanser chapter
  * 
  *  @function get_cell_for_dfcleanser_chapter
  * 
  *  @param : chapterid 
  * 
  */
 window.get_cell_for_dfcleanser_chapter = function(chapterid) {

     if (DEBUG_DETAILS_UTILS)
         console.log(log_prefix + "\n" + "     get_cell_for_dfcleanser_chapter", chapterid);

     var cells = IPython.notebook.get_cells();
     var cellInde = null;
     var chapter_metadata = get_dfcleanser_chapter_metadata(chapterid);

     for (var i = 0; i < (IPython.notebook.ncells()); i++) {
         var cell = cells[i];
         var cmdata = cell.metadata;
         var dfc_mdata = cmdata["dfcleanser_metadata"];

         if (dfc_mdata != undefined) {
             var dfc_cell_id = dfc_mdata["dfc_cellid"];

             if (dfc_cell_id == chapter_metadata) {
                 select_current_cell(cell);
                 return (cell);
             }
         }
     }

     return (null);
 };


 /*
  *
  *  Reset the dfc chapters
  *  @function reset_dfc_chapters
  * 
  */
 window.reset_dfc_chapters = function() {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     window.reset_dfc_chapters");

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     reset_dfc_chapters");

     clear_dfcleanser_chapter_output(DC_SYSTEM_ID);
     clear_dfcleanser_chapter_output(DC_DATA_IMPORT_ID);

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     just reset data import");

     clear_dfcleanser_chapter_output(DC_DATA_INSPECTION_ID);
     clear_dfcleanser_chapter_output(DC_DATA_CLEANSING_ID);
     clear_dfcleanser_chapter_output(DC_DATA_TRANSFORM_ID);
     clear_dfcleanser_chapter_output(DC_DATA_EXPORT_ID);
     clear_dfcleanser_chapter_output(DC_GEOCODE_UTILITY_ID);
     clear_dfcleanser_chapter_output(DC_DF_BROWSER_ID);
     clear_dfcleanser_chapter(DC_CENSUS_ID);
     clear_dfcleanser_chapter_output(DC_ZIPCODE_UTILITY_ID)
     load_dfcleanser_chapter(DC_WORKING_CELL_ID);

     window.shut_off_autoscroll();

     window.scroll_to(DC_CONSOLE_ID);
 };


 /*
  *
  *  close the dfcleanser chapters
  *  @function close_dfc_chapters
  * 
  */
 window.close_dfc_chapters = function() {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     close_dfc_chapters");

     close_dfcleanser_chapter(DC_SYSTEM_ID);
     close_dfcleanser_chapter(DC_DATA_IMPORT_ID);
     close_dfcleanser_chapter(DC_DATA_INSPECTION_ID);
     close_dfcleanser_chapter(DC_DATA_CLEANSING_ID);
     close_dfcleanser_chapter(DC_DATA_TRANSFORM_ID);
     close_dfcleanser_chapter(DC_DATA_EXPORT_ID);
     close_dfcleanser_chapter(DC_GEOCODE_UTILITY_ID);
     close_dfcleanser_chapter(DC_DF_BROWSER_ID);
     close_dfcleanser_chapter(DC_CENSUS_ID);
     close_dfcleanser_chapter(DC_ZIPCODE_UTILITY_ID);

 }

 /*
  *
  *  UnLoad the dfcleanser utility 
  *  @function unload_dfcleanser
  * 
  */
 window.unload_dfcleanser = function() {

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     unload_dfcleanser");

     if (get_dfc_mode() == 1)
         delete_popupcodecell('unload_dfcleanser');

     else {

         close_dfcleanser_chapter(DC_CONSOLE_ID);
         close_dfc_chapters();
         close_dfcleanser_chapter(DC_WORKING_CELL_ID);
     }

     if (DEBUG_UTILS)
         console.log(log_prefix + "\n" + "     unload_dfcleanser - end");


 };



 function chgval(formid, uniqueval) {
     /**
      * unique list dynamic change value dhtml.
      *
      * Parameters:
      *  uniqueval - value to change from
      */

     if (DEBUG_UTILS)
         console.log("chgval", formid, uniqueval);

     if (!(formid == "NOCOPY")) {
         if (!(formid == "CATSELECT")) {
             $("#" + formid).val(uniqueval);
         } else {
             var listtype = $("#" + "catconvcatsflag").val();
             var textareaid = "";

             if (DEBUG_UTILS)
                 console.log("chgval", listtype);

             if (!(listtype == "all")) {
                 if (listtype == "use include list")
                     textareaid = "catconvincludelist";
                 else
                     textareaid = "catconvexcludelist";

                 var valslistform = $("#" + textareaid);
                 var valslist = valslistform.val();
                 var newvalslist = ""

                 if (DEBUG_UTILS)
                     console.log("chgval", valslist);

                 if (valslist.length > 0) {
                     var endlist = valslist.indexOf("]");
                     var collist = valslist.slice(0, endlist);
                     newvalslist = collist + "," + uniqueval + "]";
                 } else { newvalslist = "[" + uniqueval + "]"; }

                 if (DEBUG_UTILS)
                     console.log("chgval", newvalslist);

                 valslistform.val(newvalslist);

             }
         }
     }
 }

 /*
  *
  *  display additional parms
  *  @function show_addl_parms
  * 
  */
 function show_addl_parms(importflag, formid) {

     if (DEBUG_UTILS)
         console.log("show_addl_parms", importflag, formid);

     var inputs = new Array();
     inputs.push(formid);
     var inputParms = window.get_input_form_parms(formid);
     inputs.push(inputParms);

     if (importflag == 0) {
         window.run_code_in_cell(window.DC_DATA_IMPORT_ID, window.getJSPCode(window.IMPORT_LIB, "display_addl_parms", "11" + "," + JSON.stringify(inputs)));
         window.scroll_to(DC_DATA_IMPORT_ID);
     } else {
         window.run_code_in_cell(window.DC_DATA_EXPORT_ID, window.getJSPCode(window.EXPORT_LIB, "display_export_addl_parms", "11" + "," + JSON.stringify(inputs)));
         window.scroll_to(DC_DATA_EXPORT_ID);
     }
 }

 function add_addl_parm(parmname) {

     if (DEBUG_UTILS)
         console.log("add_addl_parm", parmname);

     var inputs = new Array();
     inputs.push(parmname);
     var importid = getimportid();
     inputs.push(importid);
     var parmvalue = getdefaultvalue(parmname);
     inputs.push(parmvalue);

     if (DEBUG_UTILS)
         console.log("add_addl_parm", inputs);

     switch (importid) {
         case "0":
             var addlparmsid = $("#csvaddlParms");
             break;
         case "1":
             var addlparmsid = $("#fwfaddlParms");
             break;
         case "2":
             var addlparmsid = $("#exceladdlParms");
             break;
         case "3":
             var addlparmsid = $("#jsonaddlParms");
             break;
         case "4":
             var addlparmsid = $("#htmladdlParms");
             break;
         case "10":
             var addlparmsid = $("#ecsvaddlParms");
             break;
         case "11":
             var addlparmsid = $("#eexceladdlParms");
             break;
         case "12":
             var addlparmsid = $("#exhtmladdlParmsl");
             break;
         case "13":
             var addlparmsid = $("#ejsonaddlParmsl");
             break;
     }

     var addlparmsval = addlparmsid.val();

     if (parmvalue == "False") parmvalue = '"False"'
     if (parmvalue == "True") parmvalue = '"True"'
     if (parmvalue == "None") parmvalue = '"None"'

     if (addlparmsval.length > 0) {
         var newvals = addlparmsid.val();
         newvals = newvals.replace("}", ",\n" + '"' + parmname + '"' + " : " + parmvalue + "}");

         if (DEBUG_UTILS)
             console.log("newvals", newvals);

         addlparmsid.val(newvals);
     } else {
         addlparmsid.val("{" + '"' + parmname + '"' + " : " + parmvalue + "}");
     }

 }


 const DISPLAY_CENSUS_DETAILS = 50




 window.display_dfc_status = function(message) {

     window.alert(message);

 }

 window.display_clock = function() {

     window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "start_clock", "0"));
     return;

 }

 window.shut_off_autoscroll = function() {
     if (DEBUG_POP_UP)
         console.log(log_prefix + "\n" + "     shut_off_autoscroll");

     outputarea.OutputArea.auto_scroll_threshold = -1;
 }