//
// 
// ------------------------------------------------------
// Data Cleansing Chapter javascript functions
// ------------------------------------------------------
//
// 
const DEBUG_CLEANSING = false


//
// display column outliers
// 
window.display_Column_Outliers = function(dftitle, colname) {

    var code = "from dfcleanser.Qt.data_cleansing.ColumnOutliers import showOutliers" + NEW_LINE;
    code = code + "showOutliers('" + dftitle + "','" + colname + "')";
    window.run_code_in_cell(window.DC_WORKING_CELL_ID, code);

};

//
// display column uniques
// 
window.display_Column_Uniques = function(dftitle, colname) {

    var code = "from dfcleanser.Qt.data_cleansing.ColumnUniques import showUniques" + NEW_LINE;
    code = code + "showUniques('" + dftitle + "','" + colname + "')";
    window.run_code_in_cell(window.DC_WORKING_CELL_ID, code);

};

//
// display column uniques
// 
window.display_Column_Uniques_To_Drop = function(dftitle, colname) {

    var code = "from dfcleanser.Qt.data_cleansing.ColumnUniques import showUniques" + NEW_LINE;
    code = code + "showUniques('" + dftitle + "','" + colname + "',True)";
    window.run_code_in_cell(window.DC_WORKING_CELL_ID, code);

};