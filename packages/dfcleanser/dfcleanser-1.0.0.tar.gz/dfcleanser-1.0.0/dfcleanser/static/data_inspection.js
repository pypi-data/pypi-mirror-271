"use strict";

//
// 
// ------------------------------------------------------
// Data Inspection Chapter javascript functions
// ------------------------------------------------------
//
//  

const DEBUG_INSPECT = false

const HEAT_MAP_GRAPH = 2;
const BOXPLOT_GRAPH = 3;
const HISTOGRAM_GRAPH = 0;
const ZSCORES_GRAPH = 1;

function display_column_graph(graphid, dftitle, column_name) {

    if (DEBUG_INSPECT)
        console.log(log_prefix + "\n" + "     " + "display_column_graph", typeof(graphid), graphid, dftitle, column_name);

    var code = "from dfcleanser.Qt.data_inspection.DataInspectiondfcGraphs import showdfcGraph" + NEW_LINE;
    code = code + "showdfcGraph('" + dftitle + "','" + column_name + "','" + graphid + "')";
    window.run_code_in_cell(window.DC_WORKING_CELL_ID, code);

}











function add_graphs_chapter(graphid, dftitle, column_name) {

    if (DEBUG_INSPECT)
        console.log(log_prefix + "\n" + "     " + "add_graphs_chapter", typeof(graphid), graphid, dftitle, column_name);

    if (!(is_dfcleanser_chapter_loaded(DC_INSPECTION_GRAPHS_ID))) {

        add_dfcleanser_chapter(DC_INSPECTION_GRAPHS_ID);
    }

    switch (graphid) {
        case HEAT_MAP_GRAPH:
            window.run_code_in_cell(window.DC_INSPECTION_GRAPHS_ID, window.getJSPCode(window.INSPECTION_GRAPHS_LIB, "display_heat_map_graph", "'" + dftitle + "','" + column_name + "'"));
            window.scroll_to(DC_INSPECTION_GRAPHS_ID);
            break;
        case BOXPLOT_GRAPH:
            window.run_code_in_cell(window.DC_INSPECTION_GRAPHS_ID, window.getJSPCode(window.INSPECTION_GRAPHS_LIB, "display_box_plot_graph", "'" + dftitle + "','" + column_name + "'"));
            window.scroll_to(DC_INSPECTION_GRAPHS_ID);
            break;
        case HISTOGRAM_GRAPH:
            window.run_code_in_cell(window.DC_INSPECTION_GRAPHS_ID, window.getJSPCode(window.INSPECTION_GRAPHS_LIB, "display_histogram_graph", "'" + dftitle + "','" + column_name + "'"));
            window.scroll_to(DC_INSPECTION_GRAPHS_ID);
            break;
        case ZSCORES_GRAPH:
            window.run_code_in_cell(window.DC_INSPECTION_GRAPHS_ID, window.getJSPCode(window.INSPECTION_GRAPHS_LIB, "display_zscores_graph", "'" + dftitle + "','" + column_name + "'"));
            window.scroll_to(DC_INSPECTION_GRAPHS_ID);
            break;
    }


}