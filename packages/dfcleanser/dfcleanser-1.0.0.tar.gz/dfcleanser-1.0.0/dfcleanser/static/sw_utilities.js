//
// 
// ------------------------------------------------------
// Software Utilities Chapter javascript functions
// ------------------------------------------------------
//
//

const DEBUG_SWUTILITIES = false



// 
// ------------------------------------------------------
//              Census Utility functions 
// ------------------------------------------------------
//

const DISPLAY_DOWNLOAD_CENSUS_DATA = 1
const DISPLAY_CONFIGURE_CENSUS_DATA = 3
const PROCESS_CONFIGURE_CENSUS_DATA = 4
const DISPLAY_LOAD_CENSUS_DATA_TO_DB = 6
const DISPLAY_CENSUS_DATASETS_FOR_INSERT = 7

const VERIFY_CONFIGURE_CENSUS_DATA = 14
const PROCESS_LOAD_CENSUS_DATA_TO_DB = 25
const SHOW_SELECTED_COLUMNS = 30

function get_census_callback(fid) {
    /**
     * census process command callback.
     *
     * Parameters:
     *  fid - function id
     */

    if (DEBUG_SWUTILITIES)
        console.log("get_census_callback", fid);

    switch (fid) {

        case DISPLAY_MAIN:
        case DISPLAY_DOWNLOAD_CENSUS_DATA:
        case DISPLAY_CONFIGURE_CENSUS_DATA:
        case DISPLAY_LOAD_CENSUS_DATA_TO_DB:
        case DISPLAY_CENSUS_DATASETS_FOR_INSERT:

        case 17:
        case 18:
        case 19:
        case 20:
        case 21:
        case 23:

        case 32:
        case 33:
        case 35:
        case 37:

            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", fid));
            break;

        case 2:

            var inputs = new Array();
            var datasetids = ["Economic", "Education", "Employment", "Health_Insurance", "Housing", "Immigration", "Internet", "Population", "Social", "Transportation"];
            var datacontentcbs = new Array();


            for (var i = 0; i < datasetids.length; i++) {
                for (var j = 1; j < 6; j++) {

                    var currentcb = $("#cb" + j.toString() + datasetids[i]).prop("checked");
                    if (currentcb == true)
                        datacontentcbs.push("True");
                    else
                        datacontentcbs.push("False");
                }

                inputs.push(datacontentcbs);
                datacontentcbs = new Array();
            }

            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("2, " + JSON.stringify(inputs))));
            break;

        case PROCESS_CONFIGURE_CENSUS_DATA:

            var inputs = new Array();
            var datasetcbs = getsubsetconfiguredata();

            if (DEBUG_SWUTILITIES)
                console.log("datasetcbs", datasetcbs);

            inputs.push(datasetcbs);

            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("4, " + JSON.stringify(inputs))));
            break;

        case 24:

            var inputs = new Array();
            var datasetids = ["Economic", "Education", "Employment", "Health_Insurance", "Housing", "Immigration", "Internet", "Population", "Social", "Transportation"];
            var datacontentcbs = new Array();

            for (var i = 0; i < datasetids.length; i++) {
                for (var j = 1; j < 5; j++) {

                    var currentcb = $("#cb" + j.toString() + datasetids[i]).prop("checked");
                    if (currentcb == true)
                        datacontentcbs.push("True");
                    else
                        datacontentcbs.push("False");
                }

                inputs.push(datacontentcbs);
                datacontentcbs = new Array();
            }

            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", (fid.toString() + " ," + JSON.stringify(inputs))));
            break;

        case PROCESS_LOAD_CENSUS_DATA_TO_DB:
        case 36:
            var dfstoload = getdfloaddfsdata();

            if (DEBUG_SWUTILITIES)
                console.log("dfstoload", dfstoload);

            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", (fid.toString() + " ," + JSON.stringify(dfstoload))));
            break;

        case 28:
        case 29:

            var selected_values = $('#subdatacolnames').val();
            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", (fid.toString() + " ," + JSON.stringify(selected_values))));
            break;

        case SHOW_SELECTED_COLUMNS:

            var inputs = new Array();
            var inparms = getdfjoincolsdata();
            inputs.push(inparms);

            if (DEBUG_SWUTILITIES)
                console.log("SHOW_SELECTED_COLUMNS", inparms);

            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", SHOW_SELECTED_COLUMNS.toString() + ", " + JSON.stringify(inputs)));

            break;

        case 34:
            var fparms = get_input_form_parms("insertcoldf");
            window.clear_cell_output(window.DC_CENSUS_ID);
            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", (fid.toString() + " ," + fparms)));
            break;

        case 44:
            var inputs = new Array();
            inputs.push($("#colstoinsert option:selected").text());
            inputs.push($("#colstoinsert").val());

            window.clear_cell_output(window.DC_CENSUS_ID);
            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", 30 + ", " + JSON.stringify(inputs)));
            break;

        case 46:
            var inputs = new Array();
            inputs.push($("#colstoinsert option:selected").text());
            inputs.push($("#colstoinsert").val());
            inputs.push($('#newcoldtype').val());
            inputs.push($('#newcolnanval').val());

            window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "change_dfc_census_col_attrs", JSON.stringify(inputs)));
            break;

        case 47:
            var inputs = new Array();
            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", 47 + ", " + JSON.stringify(inputs)));
            break;

        case 48:
            var inputs = new Array();
            window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", 48 + ", " + JSON.stringify(inputs)));
            break;

    }

    window.scroll_to(DC_CENSUS_ID);
}

function get_census_dataset_details(datasetid) {
    /**
     * census process command callback.
     *
     * Parameters:
     *  datasetid - dataset id
     */

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("11, " + JSON.stringify(datasetid))));
    window.scroll_to(DC_CENSUS_ID);
}

function get_census_subData_details(datasetid, subdataid) {
    /**
     * census process command callback.
     *
     * Parameters:
     *  datasetid - dataset id
     *  subdataid - subset id
     */

    if (DEBUG_SWUTILITIES)
        console.log("get_census_subData_details", datasetid, subdataid);


    var inputs = new Array();
    inputs.push(datasetid);
    inputs.push(subdataid);

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("22, " + JSON.stringify(inputs))));
    window.scroll_to(DC_CENSUS_ID);
}

function get_load_cols_subData_details(datasetid, subdataid) {
    /**
     * census process command callback.
     *
     * Parameters:
     *  datasetid - dataset id
     *  subdataid - subset id
     */

    if (DEBUG_SWUTILITIES)
        console.log("get_load_cols_subData_details", datasetid, subdataid);

    var inputs = new Array();

    inputs.push(datasetid);
    inputs.push(subdataid);

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("7, " + JSON.stringify(inputs))));
    window.scroll_to(DC_CENSUS_ID);
}

function get_configure_subData_details(datasetid, subdataid) {
    /**
     * census process command callback.
     *
     * Parameters:
     *  datasetid - dataset id
     *  subdataid - subset id
     */

    if (DEBUG_SWUTILITIES)
        console.log("get_configure_subData_details", datasetid, subdataid);

    var inputs = new Array();
    inputs.push(datasetid);
    inputs.push(subdataid);

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("22, " + JSON.stringify(inputs))));
    window.scroll_to(DC_CENSUS_ID);
}

function get_configure_dataset_details(dtid, datasetid) {
    /**
     * census process command callback.
     *
     * Parameters:
     *  datasetid - dataset id
     */

    if (DEBUG_SWUTILITIES)
        console.log("get_configure_dataset_details", dtid, datasetid);

    var inputs = new Array();
    inputs.push(datasetid);
    inputs.push(dtid);
    inputs.push("1");

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("21, " + JSON.stringify(inputs))));
    window.scroll_to(DC_CENSUS_ID);
}


function get_df_census_dataset_details(datasetid) {
    /**
     * census process command callback.
     *
     * Parameters:
     *  datasetid - dataset id
     */

    if (DEBUG_SWUTILITIES)
        console.log("get_df_census_dataset_details", datasetid);

    var inputs = new Array();
    inputs.push(datasetid);
    inputs.push(dtid);
    inputs.push("0");

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("21, " + JSON.stringify(inputs))));
    window.scroll_to(DC_CENSUS_ID);
}

function scroll_census_cols(datasetid, subdataid, colnameid, direction) {
    /**
     * census process command callback.
     *
     * Parameters:
     *  datasetid - dataset id
     *  subdataid - subset id
     *  colnameid - subset id
     *  direction - direction
     */

    var inputs = new Array();
    inputs.push(datasetid);
    inputs.push(subdataid);
    inputs.push(colnameid);
    inputs.push(direction);

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     scroll_census_cols", inputs);

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("15, " + JSON.stringify(inputs))));
    window.scroll_to(DC_CENSUS_ID);
}

function get_select_cols_subData_details(datasetid, subdataid) {
    /**
     * census process command callback.
     *
     * Parameters:
     *  datasetid - dataset id
     *  subdataid - subset id
     */

    var inputs = new Array();
    inputs.push(datasetid);
    inputs.push(subdataid);

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     get_select_cols_subData_details", inputs);

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("30, " + JSON.stringify(inputs))));
    window.scroll_to(DC_CENSUS_ID);
}

function set_census_cbs(cbid) {
    /**
     * census process checkbox callback.
     *
     * Parameters:
     *  cbid - checkbox id
     */

    var idnum = 0;
    var datasetid = "";
    var i = 0;

    if (cbid.indexOf("cb1") > -1) idnum = 1;
    else if (cbid.indexOf("cb2") > -1) idnum = 2;
    else if (cbid.indexOf("cb3") > -1) idnum = 3;
    else if (cbid.indexOf("cb4") > -1) idnum = 4;
    else if (cbid.indexOf("cb5") > -1) idnum = 5;
    else if (cbid.indexOf("cb6") > -1) idnum = 6;
    else idnum = 0;

    if (cbid.indexOf("Economic") > -1) datasetid = "Economic";
    else if (cbid.indexOf("Education") > -1) datasetid = "Education";
    else if (cbid.indexOf("Employment") > -1) datasetid = "Employment";
    else if (cbid.indexOf("Health_Insurance") > -1) datasetid = "Health_Insurance";
    else if (cbid.indexOf("Housing") > -1) datasetid = "Housing";
    else if (cbid.indexOf("Immigration") > -1) datasetid = "Immigration";
    else if (cbid.indexOf("Internet") > -1) datasetid = "Internet";
    else if (cbid.indexOf("Population") > -1) datasetid = "Population";
    else if (cbid.indexOf("Social") > -1) datasetid = "Social";
    else if (cbid.indexOf("Transportation") > -1) datasetid = "Transportation";
    else datasetid = ""

    if ($("#" + cbid).prop("checked") == true) {
        if (idnum == 6) {
            for (i = 1; i < 6; i++) {
                $("#cb" + i.toString() + datasetid).prop("checked", false);
            }
        } else {
            $("#cb6" + datasetid).prop("checked", false);
        }
    }
}

function get_census_cols(dtid) {

    var fparms;

    switch (dtid) {

        case 0:
            fparms = get_input_form_parms("dcdfcensusgetcolsinput");
            break;
        case 1:
            fparms = get_input_form_parms("dcdfcensusgetcolscityinput");
            break;
        case 2:
            fparms = get_input_form_parms("dcdfcensusgetcolscountyinput");
            break;
        case 3:
            fparms = get_input_form_parms("dcdfcensusgetcolsstatesinput");
            break;
    }

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("8, " + JSON.stringify(fparms))));
    window.scroll_to(DC_CENSUS_ID);
}

function export_census_to_db(dfid) {
    /**
     * export a census df to a db
     *
     * Parameters:
     *  dfid   - dataframe id
     * 
     */

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "export_census_to_db", dfid);

}

function export_census_to_df(dfid) {
    /**
     * export a census df to a destination
     *
     * Parameters:
     *  dfid   - dataframe id
     * 
     */

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "export_census_to_df", dfid);

}

function select_new_insert_df(selectid) {
    /**
     * select a new df to insert cols into
     *
     * Parameters:
     *  dfid   - dataframe id
     * 
     */

    var dftitle = $("#" + selectid).val();

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "select_new_insert_df", dftitle);

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", ("33, " + JSON.stringify(dftitle))));
    window.scroll_to(DC_CENSUS_ID);
}

function select_new_insert_df_index_type(selid) {
    /**
     * select a new col to use as index
     *
     * Parameters:
     *  dfid   - dataframe id
     * 
     */

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "select_new_insert_df_index_type", selid);

    $("#censusindexcols").val("");

}

function select_new_insert_df_col(selectid) {
    /**
     * select a new col to use as index
     *
     * Parameters:
     *  dfid   - dataframe id
     * 
     */

    var itype = $("#censusindextype").val();
    var index = 0;

    var icols = $("#censusindexcols").val();

    var colname = $("#" + selectid).val();

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "select_new_insert_df_col", colname, itype, icols);

    switch (itype) {

        case "[zipcode]":
            index = 0;
            break;
        case "[city,state]":
            index = 1;
            break;
        case "[county,state]":
            index = 2;
            break;
        default:
            index = 3;
            break;
    }

    if ((index == 0) || (index == 3)) {
        $("#censusindexcols").val("[" + colname + "]");
    } else {

        if (icols.indexOf("[") > -1) {
            if (icols.indexOf(",]") > -1) {
                icols = icols.replace(",]", "," + colname + "]")
                $("#censusindexcols").val(icols);
            } else {
                $("#censusindexcols").val("[" + colname + ",]");
            }
        } else {
            $("#censusindexcols").val("[" + colname + ",]");
        }
    }
}

function export_df_from_census(datasetid) {

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "export_df_from_census", datasetid);

    window.run_code_in_cell(window.DC_DATA_EXPORT_ID, window.getJSPCode(window.EXPORT_LIB, "process_export_form", ("4" + ", " + JSON.stringify(datasetid))));
    window.scroll_to(DC_DATA_EXPORT_ID);

}

function export_to_db_from_census(datasetid) {

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "export_to_db_from_census", datasetid);

    window.run_code_in_cell(window.DC_DATA_EXPORT_ID, window.getJSPCode(window.EXPORT_LIB, "process_export_form", ("5" + ", " + JSON.stringify(datasetid))));
    window.scroll_to(DC_DATA_EXPORT_ID);

}





// 
// ------------------------------------------------------
//              Census Utility functions 
// ------------------------------------------------------
//
function change_census_df(selectid) {

    var dfname = $("#" + selectid + " option:selected").text();
    var df_list = $("#censusdfstoload").val();
    var df_keys = $("#userdfsindexkeys").val();
    userdfsindexkeys

    var inputs = new Array();
    inputs.push(df_list);
    inputs.push(dfname);
    inputs.push(df_keys);
    //inputs.push(colval);

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "change_census_df", selectid, inputs);

    window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "change_census_df_to_insert_from", JSON.stringify(inputs)));

}



function get_census_dataset_columns(datasetid, keyid) {

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "get_census_dataset_columns", datasetid, keyid);

    var inputs = new Array();
    inputs.push(datasetid);
    inputs.push(keyid);

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", "38, " + JSON.stringify(inputs)));
    window.scroll_to(DC_CENSUS_ID);
}

function get_census_cols_details(datasetid, subsetid) {

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "get_census_cols_details", datasetid, subsetid);

    var inputs = new Array();
    inputs.push(datasetid);
    inputs.push(subsetid);

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", "40, " + JSON.stringify(inputs)));
    window.scroll_to(DC_CENSUS_ID);
}

function select_dataset_radio(datasetid) {

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "select_dataset_radio", datasetid);


    var datasetids = new Array("Economic", "Education", "Employment", "Health_Insurance", "Housing", "Immigration", "Internet", "Population", "Social", "Transportation");
    var keytypes = new Array("ZipCode", "City", "County", "State");

    var i, j;

    for (i = 0; i < datasetids.length; i++) {
        if (!(datasetids[i] == datasetid)) {
            for (j = 0; j < keytypes.length; j++) {
                $("#radio" + datasetids[i] + keytypes[j]).prop("checked", false);
            }
        }
    }
}

function change_subset_col_selected_attrs(selectid) {

    var colname = $("#" + selectid + " option:selected").text();
    var colval = $("#" + selectid).val();

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "change_subset_col_selected_attrs", selectid, colname, colval);

    var inputs = new Array();
    inputs.push(colname);
    inputs.push(colval);

    window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "change_selected_dfc_census_col", JSON.stringify(inputs)));

}

function change_user_df(selectid) {

    var census_df_name = $("#censusdfstoload").val();
    var dfname = $("#" + selectid + " option:selected").text();
    var dfkeys = $("#userdfsindexkeys").val();

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "change_user_df", selectid, census_df_name, dfname);

    var inputs = new Array();
    inputs.push(census_df_name);
    inputs.push(dfname);
    inputs.push(dfkeys);

    window.run_code_in_cell(window.DC_CENSUS_ID, window.getJSPCode(window.SW_UTILS_CENSUS_LIB, "display_census_utility", "49, " + JSON.stringify(inputs)));
    window.scroll_to(DC_CENSUS_ID);
}


function change_user_df_col(selectid) {

    var colname = $("#" + selectid + " option:selected").text();
    var current_keys = $("#userdfsindexkeys").val();
    current_keys = current_keys.replace("[", "");
    current_keys = current_keys.replace("]", "");

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "change_user_df_col", selectid, colname, current_keys);

    var firstkey = "";
    var secondkey = "";

    var commaloc = current_keys.indexOf(",");
    if (commaloc > -1) {
        firstkey = current_keys.substr(0, commaloc);
        secondkey = current_keys.substr(commaloc + 1, current_keys.length);
    } else {
        firstkey = current_keys
        secondkey = ""
    }

    if (firstkey.indexOf("key col") > -1) {
        firstkey = colname;
    } else {

        if (secondkey.indexOf("key col") > -1) {
            secondkey = colname;
        } else {
            firstkey = colname;
        }
    }

    var new_keys = "[" + firstkey;
    if (secondkey.length > 0) {
        new_keys = new_keys + "," + secondkey;
    }
    new_keys = new_keys + "]"

    $("#userdfsindexkeys").val(new_keys);
}


function download_dfc_census_dataset(datasetid) {

    if (DEBUG_SWUTILITIES)
        console.log(log_prefix + "\n" + "     " + "download_dfc_census_dataset", datasetid);

    var url = "https://github.com/RickKrasinski/dfc_census_zips/blob/master/";

    switch (datasetid) {
        case 0:
            url = url + "economic.zip";
            break;
        case 1:
            url = url + "education.zip";
            break;
        case 2:
            url = url + "employment.zip";
            break;
        case 3:
            url = url + "health_insurance.zip";
            break;
        case 4:
            url = url + "housing.zip";
            break;
        case 5:
            url = url + "immigration.zip";
            break;
        case 6:
            url = url + "internet.zip";
            break;
        case 7:
            url = url + "population.zip";
            break;
        case 8:
            url = url + "social.zip";
            break;
        case 9:
            url = url + "transportation.zip";
            break;
    }

    window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.COMMON_LIB, "display_url", JSON.stringify(url)));
}


function add_user_df_to_join(user_df) {


    console.log(log_prefix + "\n" + "     " + "add_user_df_to_join", user_df);

    var currentuserdfs = $("#" + user_df + " option:selected");
    var currentval = currentuserdfs.val();
    var currentuserdfs = $('#joindscolsuserdfs');

    var currentval = $("#" + user_df + " option:selected").text();
    var newval = "";

    console.log("currentval", currentval);

    if (currentval.length == 0) {
        newval = "[" + currentval + "]"
    } else {
        var endlist = currentval.indexOf("]");
        newval = currentval.slice(0, endlist);
        newval = newval + ", " + currentval + "]";
    }

    if (DEBUG_SWUTILITIES)
        console.log("currentval", currentval);

    currentuserdfs.val(currentval);
}

//
// display map by url
//
function display_map_url(url) {
    window.run_code_in_cell(window.DC_WORKING_CELL_ID, window.getJSPCode(window.SW_UTILS_GEOCODE_LIB, "display_geocode_map", JSON.stringify(url)));
    return true;
};