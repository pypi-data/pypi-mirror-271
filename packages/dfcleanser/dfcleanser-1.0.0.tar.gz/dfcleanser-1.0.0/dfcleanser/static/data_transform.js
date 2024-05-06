//
// 
// ------------------------------------------------------
// Data Transform Chapter javascript functions
// ------------------------------------------------------
//
// 

const DEBUG_TRANSFORM = false


const PROCESS = 0
const RETURN = 1


function change_convert_dtype_callback(selectid) {
    /**
     * change convert datetime column callback.
     *
     * Parameters:
     *  optionId  - option id
     */

    var selected_value = $("#" + selectid + " :selected").text();
    var newcolname = $("#dttdrescolname").val();
    var units = $("#dttdunits").val();

    if (selected_value == "timedelta") {
        $("#dttdunits").prop("disabled", true);
        units = "timedelta";
    } else {
        $("#dttdunits").prop("disabled", false);
    }

    var found = newcolname.indexOf("_timedelta");

    if (newcolname.indexOf("_timedelta") > -1) { newcolname = newcolname.replace("_timedelta", "_" + units); } else {
        if (newcolname.indexOf("_Days") > -1) { newcolname = newcolname.replace("_Days", "_" + units); } else {
            if (newcolname.indexOf("_Hours") > -1) { newcolname = newcolname.replace("_Hours", "_" + units); } else {
                if (newcolname.indexOf("_Minutes") > -1) { newcolname = newcolname.replace("_Minutes", "_" + units); } else {
                    if (newcolname.indexOf("_Seconds") > -1) { newcolname = newcolname.replace("_Seconds", "_" + units); } else {
                        if (newcolname.indexOf("_MilliSeconds") > -1) { newcolname = newcolname.replace("_MilliSeconds", "_" + units); } else {
                            if (newcolname.indexOf("_MicroSeconds") > -1) { newcolname = newcolname.replace("_MicroSeconds", "_" + units); }
                        }
                    }
                }
            }
        }
    }

    $("#dttdrescolname").val(newcolname);

}

function change_convert_units_callback(selectid) {
    /**
     * change convert datetime column callback.
     *
     * Parameters:
     *  selectid  - select id
     */

    var units = $("#" + selectid + " :selected").text();
    var colname = $("#dttdrescolname").val();

    if (colname.indexOf("_Days") > -1) { colname = colname.replace("_Days", "_" + units); } else {
        if (colname.indexOf("_Hours") > -1) { colname = colname.replace("_Hours", "_" + units); } else {
            if (colname.indexOf("_Minutes") > -1) { colname = colname.replace("_Minutes", "_" + units); } else {
                if (colname.indexOf("_Seconds") > -1) { colname = colname.replace("_Seconds", "_" + units); } else {
                    if (colname.indexOf("_MilliSeconds") > -1) { colname = colname.replace("_MilliSeconds", "_" + units); } else {
                        if (colname.indexOf("_MicroSeconds") > -1) { colname = colname.replace("_MicroSeconds", "_" + units); }
                    }
                }
            }
        }
    }

    $("#dttdrescolname").val(colname);

}


/*
 -----------------------------------------------
 -----------------------------------------------
 * Dataframe Transform remote calls
 -----------------------------------------------
 -----------------------------------------------
*/

function change_reset_index_callback(selectid) {
    add_select_val(selectid, "resetindexdroplevels");
}