//
// 
// ------------------------------------------------------
// Geocode Utilities Chapter javascript functions
// ------------------------------------------------------
//
//

const DEBUG_GEOCODE = false

const ArcGISId = 0
const BaiduId = 1
const BingId = 2
const GoogleId = 7
const OpenMapQuestId = 9
const NominatimId = 11


function select_bulk_geocoder(gcid) {
    /**
     * select geocoder display.
     *
     * Parameters:
     *  gcid - geocoder id
     */

    var id = -1;
    switch (gcid) {

        case ("ArcGIS"):
            id = ArcGISId;
            break;
        case ("Baidu"):
            id = BaiduId;
            break;
        case ("Bing"):
            id = BingId;
            break;
        case ("GoogleV3"):
            id = GoogleId;
            break;
        case ("OpenMapQuest"):
            id = OpenMapQuestId;
            break;
        case ("Nominatim"):
            id = NominatimId;
            break;
    }

    var inputs = [id, 1, []];
    window.run_code_in_cell(window.DC_GEOCODE_UTILITY_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_geocode_utility", "3, " + JSON.stringify(inputs)));
    window.scroll_to(DC_GEOCODE_UTILITY_ID);
}

function process_bulk_tuning() {
    /**
     * geocodong change center points df.
     *
     * Parameters:
     */

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     " + "process_bulk_tuning");

    inputId = "bulktune";

    if (inputId != "") {
        var inputs = window.get_input_form_parms(inputId);
        window.run_code_in_cell(window.DC_GEOCODE_UTILITY_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_geocode_utility", fid + "," + JSON.stringify(inputs)));
        window.scroll_to(DC_GEOCODE_UTILITY_ID);
    }

}

function display_bulk_tuning(gid, gmode) {
    /**
     * display geocoders.
     *
     * Parameters:
     *  gid   - geocoder id
     *  gmode - geocode mode
     */

    var inputs = [gid, gmode];
    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_bulk_tuning", JSON.stringify(inputs)));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function geocode_return() {
    /**
     * return to start.
     *
     */

    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_bulk_geocoders", "-1"));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function display_geocoders(gid, gmode) {
    /**
     * display geocoders.
     *
     * Parameters:
     *  gid   - geocoder id
     *  gmode - geocode mode
     */

    var inputs = [gid, gmode];
    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_geocode_utility", "3" + ", " + JSON.stringify(inputs)));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function browse_bulk_geocoding_df(df_name) {
    /**
     * geocoder bulk reverse processing.
     *
     * Parameters:
     *  fid- function id
     */

    var inputs = [df_name];
    window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_INSPECTION_LIB, "browseDataframe", JSON.stringify(df_name)));
}

function export_bulk_geocoding_df(df_name) {
    /**
     * geocoder bulk reverse processing.
     *
     * Parameters:
     *  fid- function id
     */

    var inputs = [df_name];
    window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.QT_EXPORT_LIB, "exportDataframe", JSON.stringify(df_name)));
}

DISPLAY_BULK_RESULTS_APPEND = 1
DISPLAY_BULK_RESULTS_RETURN = 23

function display_bulk_geocoding_results(fid) {
    /**
     * geocoder bulk reverse processing.
     *
     * Parameters:
     *  fid- function id
     */

    var inputs = [fid];

    if (fid == DISPLAY_BULK_RESULTS_RETURN) {
        window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_bulk_geocoders", ("-1")));
        window.scroll_to(DC_GEOCODE_BULK_ID);
    } else {
        window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_CONTROL_LIB, "add_geocode_results_to_user_df", ("0")));
        window.scroll_to(DC_GEOCODE_BULK_ID);
    }
}

function browse_df_in_df_browser(df_title) {
    /**
     * geocoder bulk reverse processing.
     *
     * Parameters:
     *  fid- function id
     */

    var inputs = [df_title];
    window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.DF_BROWSER_LIB, "showDfBrowser", JSON.stringify(df_title)));
}


const PROCESS_BULK_RESULTS_APPEND_PROCESS = 7
const PROCESS_BULK_RESULTS_APPEND_CLEAR = 8

function process_bulk_geocoding_results(fid) {
    /**
     * geocoder bulk geocoding processing.
     *
     * Parameters:
     *  fid- function id
     */

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     process_bulk_geocoding_results", fid);

    var formid = "";

    switch (fid) {

        case PROCESS_BULK_RESULTS_APPEND_CLEAR:
            formid = "geocodebulkproc";
            break;
        case PROCESS_BULK_RESULTS_APPEND_PROCESS:
            formid = "bulkcsvappend";
            break;

        case 10:
        case 11:
        case 12:
        case 13:
            formid = "reversebulkproc";
            break;

        case 15:
        case 16:
        case 17:
        case 18:
            formid = "bulkcsvexport";
            break;

        case 24:
            window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "open_as_excel", "1"));
            return;
            break;
        case 25:
            window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "open_as_excel", "2"));
            return;
            break;
        case 26:
        case 27:
        case 28:
            formid = "bulkerrorscsvexport";
            break;
        case 30:
            window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "open_as_excel", "3"));
            return;
            break;

    }

    if (formid != "") {
        var fparms = get_input_form_parms(formid);
    } else {
        fparms = [];
    }
    var inputs = [fid, fparms];

    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_geocode_utility", ("30, " + JSON.stringify(inputs))));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function controlbulkrun(fid) {
    /**
     * geocoder bulk run control.
     *
     * Parameters:
     *  fid- function id
     */

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     controlbulkrun", fid);

    if (fid == 26) {
        window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_CONTROL_LIB, "process_bulk_geocoding_run_cmd", fid));
        window.scroll_to(window.DC_GEOCODE_BULK_ID);
    } else {
        window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_CONTROL_LIB, "process_bulk_geocoding_run_cmd", fid));
        window.scroll_to(window.DC_GEOCODE_BULK_ID);
    }
}

function set_bulk_progress_bar(barid, barvalue) {
    /**
     * set progress value
     *
     * Parameters:
     *  barid    - progress bar id
     *  barvalue - progress bar value
     */

    var progressbar = $("#" + barid);
    progressbar.text(barvalue.toString() + "%");
    progressbar.attr('aria-valuenow', barvalue).css('width', barvalue + "%");

}

function view_geocode_errors() {
    /**
     * view_geocode_errors
     *
     * Parameters:
     */

    var ids = new Array("didfdataframe");
    var inputs = new Array("Current_Geocoding_Error_Log_df");

    var parms = new Array();
    parms.push(ids);
    parms.push(inputs);
    fparms = JSON.stringify(parms);

    var inputcbs = new Array("False", "False", "True", "False", "False");
    cbs = JSON.stringify(inputcbs);

    var inputs = [fparms, cbs];
    window.clear_cell_output(window.DC_DATA_INSPECTION_ID);
    window.run_code_in_cell(window.DC_DATA_INSPECTION_ID, window.getJSPCode(window.INSPECTION_LIB, "display_data_inspection", "1" + ", " + JSON.stringify(inputs)));
    window.scroll_to(DC_DATA_INSPECTION_ID);
}

function report_geocode_run_error(cmd, msg) {
    /**
     * report a geocode run error
     *
     * Parameters:
     *  geocid  - geocoder id
     *  cmd     - run cmd
     *  msg     - error message
     */


    var parms = new Array();
    parms.push(cmd);
    parms.push(msg);

    window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_CONTROL_LIB, "process_bulk_geocoding_run_cmd", "31, " + JSON.stringify(parms)));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function change_bulk_df(selectid) {
    /**
     * view_geocode_errors
     *
     * Parameters:
     */

    var dfname = $("#" + selectid).val();

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     change_bulk_df", dfname);

    var parms = new Array();
    parms.push(dfname);

    window.run_code_in_cell(window.DC_GEOCODE_UTILITY_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_geocode_utility", "32, " + JSON.stringify(parms)));
    window.scroll_to(DC_GEOCODE_UTILITY_ID);
}

function change_bulk_reverse_df(selectid) {
    /**
     * view_geocode_errors
     *
     * Parameters:
     */

    var dfname = $("#" + selectid).val();

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     change_bulk_reverse_df", dfname);

    var parms = new Array();
    parms.push(dfname);

    window.run_code_in_cell(window.DC_GEOCODE_UTILITY_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_geocode_utility", "33, " + JSON.stringify(parms)));
    window.scroll_to(DC_GEOCODE_UTILITY_ID);
}

function get_df_center_col(selectid) {
    /**
     * change get center pt df col
     *
     * Parameters:
     *  selectid   - colname
     * 
     */

    var colname = $("#" + selectid).val();
    var currentColumns = $('#centerdflatlng');

    change_df_lat_lng_columns(colname, currentColumns);
}

function exit_bulk_geocoding() {

    if (window.confirm("Exit will delete all current geocoding data upon. Exit?")) {
        window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_bulk_geocoders", "-1"));
        window.scroll_to(DC_GEOCODE_BULK_ID);
    }
}


// 
// ------------------------------------------------------
//              Zipcode Utility functions 
// ------------------------------------------------------
//

function display_zipcode(fid) {
    /**
     * display zipcodes.
     *
     * Parameters:
     *  fid  - function id
     */

    var inputs = [fid];
    window.run_code_in_cell(window.DC_ZIPCODE_UTILITY_ID, window.getJSPCode(window.SW_UTILS_ZIPCODE_LIB, "display_zipcode_utility", fid));
    window.scroll_to(DC_ZIPCODE_UTILITY_ID);
}



//
// display map by url
//
function display_map_url(url) {
    window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_LIB, "display_geocode_map", JSON.stringify(url)));
    return true;
}


function test_geocoder(geocodeid) {
    /**
     * test geocoder.
     *
     * Parameters:
     *  gid   - geocoder id
     *  gmode - geocode mode
     */
    if (geocodeid == BingId)
        id = "bingbulkgeocoder";
    else
        id = "googlebulkgeocoder";

    var fparms = get_input_form_parms(id);
    //var inputs = [gid, gmode, fparms];

    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "test_bulk_geocoder_connection", geocodeid + ", " + JSON.stringify(fparms)));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}


function display_geocoding_query_callback(geocodeid) {
    /**
     * geocoder inputs processing.
     *
     * Parameters:
     *  geocodeid  - geocoder id
     */

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     display_geocoding_query_callback", geocodeid);

    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_bulk_query_geocoding", geocodeid));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function display_geocoding_reverse_callback(geocodeid) {
    /**
     * geocoder inputs processing.
     *
     * Parameters:
     *  geocodeid  - geocoder id
     */

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     display_geocoding_reverse_callback", geocodeid);

    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_bulk_reverse_geocoding", geocodeid));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function select_bulk_geocoder(geocodeid) {

    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "display_bulk_geocoders", geocodeid));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function select_addr_col(geoid, colname) {

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     select_addr_col", geoid, colname);

    if (geoid == 2)
        var currentAddress = $("#bbqaddress");
    else
        var currentAddress = $("#bgqaddress");
    var newAddress = "";
    if (currentAddress.val().length > 0) { newAddress = currentAddress.val() + " + " + colname; } else { newAddress = colname; }
    currentAddress.val(newAddress);
}

function select_lat_lng_col(geoid, colname) {

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     select_lat_lng_col", geoid, colname);

    if (geoid == 2)
        var currentAddress = $("#bbrcolumnname");
    else
        var currentAddress = $("#bgrcolumnname");
    var newAddress = "";
    if (currentAddress.val().length > 0) { newAddress = currentAddress.val() + " + " + colname; } else { newAddress = colname; }
    currentAddress.val(newAddress);
}

function add_addr_comp(geoid, addrcomp) {

    console.log(log_prefix + "\n" + "     add_addr_comp", geoid, addrcomp);

    if (geoid == 2)
        var currentAddress = $("#bbraddrcomps");
    else
        var currentAddress = $("#bgraddresscomponents");

    console.log(log_prefix + "\n" + "     currentAddress.val()", currentAddress.val());

    var newAddress = "";

    if (currentAddress.val().length > 0) {
        newAddress = currentAddress.val().replace("]", " ," + addrcomp + "]");
    } else { newAddress = "[" + addrcomp + "]"; }
    currentAddress.val(newAddress);
}

function add_location_type(geoid, location) {

    if (geoid == 2)
        var currentLocations = $("#bgqloctypes");
    else {
        var currentLocations = $("#bgqloctypes");
    }
    var newLocations = "";

    if (currentLocations.val().length > 0) {
        newLocations = currentLocations.val().replace("]", " ," + location + "]");
    } else { newLocations = "[" + location + "]"; }

    currentLocations.val(newLocations);
}

function process_geocoding_query_callback(geocodeid) {
    /**
     * geocoder inputs processing.
     *
     * Parameters:
     *  geocodeid  - geocoder id
     */

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     process_geocoding_query_callback", geocodeid);

    if (geocodeid == 2)
        var fparms = get_input_form_parms("bingbulkquery");
    else
        var fparms = get_input_form_parms("googlebulkquery");
    //var inputs = [geocodeid];

    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "process_bulk_query_geocoding", geocodeid + ", " + fparms));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function process_geocoding_reverse_callback(geocodeid) {
    /**
     * geocoder inputs processing.
     *
     * Parameters:
     *  geocodeid  - geocoder id
     */

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     process_geocoding_reverse_callback", geocodeid);

    if (geocodeid == 2)
        var fparms = get_input_form_parms("bingbulkreverse");
    else
        var fparms = get_input_form_parms("googlebulkreverse");

    window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_LIB, "process_bulk_reverse_geocoding", geocodeid + ", " + fparms));
    window.scroll_to(DC_GEOCODE_BULK_ID);
}

function merge_query_geocoding_results(geocoderid) {
    /**
     * geocoder inputs processing.
     *
     * Parameters:
     *  geocodeid  - geocoder id
     */

    if (1) //DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     merge_query_geocoding_results", geocoderid);

    if (geocoderid == 7)
        var inputId = "googleadjustbulkquery";
    else
        var inputId = "bingbulkadjustquery";


    if (inputId != "") {
        var inputs = window.get_input_form_parms(inputId);

        if (1) //DEBUG_GEOCODE)
            console.log(log_prefix + "\n" + "     merge_query_geocoding_results", inputs);

        window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_CONTROL_LIB, "merge_bulk_results", geocoderid + ", 1," + JSON.stringify(inputs)));
        window.scroll_to(DC_GEOCODE_BULK_ID);

    }
}

function merge_reverse_geocoding_results(geocoderid) {
    /**
     * geocoder inputs processing.
     *
     * Parameters:
     *  geocodeid  - geocoder id
     */

    if (DEBUG_GEOCODE)
        console.log(log_prefix + "\n" + "     merge_reverse_geocoding_results", geocodeid);

    if (geocoderid == 7)
        var inputId = "googlebulkreverseadjust";
    else
        var inputId = "bingbulkreverseadjust";


    if (inputId != "") {
        var inputs = window.get_input_form_parms(inputId);
        window.run_code_in_cell(window.DC_GEOCODE_BULK_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_BULK_CONTROL_LIB, "merge_bulk_results", geocoderid + ", 2," + JSON.stringify(inputs)));
        window.scroll_to(DC_GEOCODE_BULK_ID);
    }
}