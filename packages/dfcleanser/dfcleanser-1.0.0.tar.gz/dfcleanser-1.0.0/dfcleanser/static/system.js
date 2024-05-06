//
// 
// ------------------------------------------------------
// System Environment Chapter javascript functions
// ------------------------------------------------------
//
// 

const DEBUG_SYSTEM = false



window.set_textarea = function(formid, istring) {
    var mstring = istring.replace(/dfc_new_line/g, '\n');
    $("#" + formid).val(mstring);
};