//
// 
// ------------------------------------------------------
// Data Import javascript functions
// ------------------------------------------------------
//
// 

const DEBUG_IMPORT = false



function dfcleanser_test_con_callback(sqlid, dbid) {
    /**
     * test db connection callbacks.
     *
     * Parameters:
     *  sqlid    - table or query or export
     *  dbid     - database server id
     */

    if (DEBUG_IMPORT)
        console.log(log_prefix + "\n" + "     dfcleanser_test_con_callback : " + sqlid.toString() + " : " + dbid.toString());

    var sqlinputparms = null;

    switch (dbid) {
        case 0:
            sqlinputparms = window.get_input_form_parms("MySQLdbconnector");
            break;
        case 1:
            sqlinputparms = window.get_input_form_parms("MSSQLServerdbconnector");
            break;
        case 2:
            sqlinputparms = window.get_input_form_parms("SQLitedbconnector");
            break;
        case 3:
            sqlinputparms = window.get_input_form_parms("Postgresqldbconnector");
            break;
        case 4:
            sqlinputparms = window.get_input_form_parms("Oracledbconnector");
            break;
        case 5:
            sqlinputparms = window.get_input_form_parms("customdbconnector");
            break;
    }

    if (sqlinputparms != null) {
        window.run_code_in_cell(window.DC_DATA_IMPORT_ID, window.getJSPCode(window.IMPORT_LIB, "test_import_sql_db_connector", sqlid + ", " + dbid + ", " + sqlinputparms));
    }

    window.scroll_to(DC_DATA_IMPORT_ID);
}




function maintain_dbconnectors(fid, sqlid, connectorkey, formid = null) {
    /**
     * Custom Import callbacks.
     *
     * Parameters:
     *  fid             - function id
     *  connectorkey    - connector to maintain
     */

    if (DEBUG_IMPORT)
        console.log("maintain_dbconnectors", fid, sqlid, connectorkey, formid);

    if ((fid != 5) && (fid != 6)) {

        var inputs = new Array();
        inputs.push(fid);
        inputs.push(sqlid);
        inputs.push(connectorkey);

        if (!(formid == null)) {
            var parms = get_input_form_parms(formid);
            inputs.push(parms);
        }

        if (DEBUG_IMPORT)
            console.log("maintain_dbconnectors", inputs);

        if (sqlid == 0)
            window.run_code_in_cell(window.DC_DATA_IMPORT_ID, window.getJSPCode(window.IMPORT_LIB, "process_dbconnector_cmd", JSON.stringify(inputs)));
        else
            window.run_code_in_cell(window.DC_DATA_EXPORT_ID, window.getJSPCode(window.EXPORT_LIB, "process_export_dbconnector_cmd", JSON.stringify(inputs)));


    } else {

        if (fid == 5) {

            if (sqlid == 0) {
                if (connectorkey == 0)
                    window.run_code_in_cell(window.DC_DATA_IMPORT_ID, window.getJSPCode(window.IMPORT_LIB, "display_import_forms", "0"));
                else
                    window.run_code_in_cell(window.DC_DATA_IMPORT_ID, window.getJSPCode(window.IMPORT_LIB, "display_import_forms", "0"));
            } else {
                if (connectorkey == 0)
                    window.run_code_in_cell(window.DC_DATA_EXPORT_ID, window.getJSPCode(window.EXPORT_LIB, "display_export_forms", "0"));
                else
                    window.run_code_in_cell(window.DC_DATA_EXPORT_ID, window.getJSPCode(window.EXPORT_LIB, "display_export_forms", "0"));
            }
        } else {

            if (sqlid == 0) {
                if (connectorkey == 0)
                    window.run_code_in_cell(window.DC_DATA_IMPORT_ID, window.getJSPCode(window.IMPORT_LIB, "display_import_forms", "7, 5"));
                else
                    window.run_code_in_cell(window.DC_DATA_IMPORT_ID, window.getJSPCode(window.IMPORT_LIB, "display_import_forms", "7, 6"));
            } else {
                if (connectorkey == 0)
                    window.run_code_in_cell(window.DC_DATA_EXPORT_ID, window.getJSPCode(window.EXPORT_LIB, "display_export_forms", "2, 4"));
                else
                    window.run_code_in_cell(window.DC_DATA_EXPORT_ID, window.getJSPCode(window.EXPORT_LIB, "display_export_forms", "2, 4"));
            }
        }
    }

    if (sqlid == 0)
        window.scroll_to(DC_DATA_IMPORT_ID);
    else
        window.scroll_to(DC_DATA_EXPORT_ID);

}