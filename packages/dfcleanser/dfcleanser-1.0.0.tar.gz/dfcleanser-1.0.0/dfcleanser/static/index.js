define([
    'require',
    'jquery',
    'base/js/namespace',
    'base/js/utils',
    'base/js/dialog',
    'base/js/events',
    'notebook/js/codecell',
    './js_utils',
    './data_cleansing',
    './data_export',
    './data_import',
    './data_inspection',
    './data_transform',
    './geocode_utility',
    './system',
    './pop_up_cell'
], function(requirejs, $, Jupyter, utils, dialog, events, codecell) {

    "use strict";

    var log_prefix = '[' + "dfcleanser" + ']';

    Jupyter.notebook.events.on('notebook_renamed.Notebook', callback_notebook_renamed);

    var CodeCell = codecell.CodeCell;

    function load_buttons() {
        if (!Jupyter.toolbar) {
            $([Jupyter.notebook.events]).on("app_initialized.NotebookApp", place_button);
            return;
        }
        Jupyter.toolbar.add_buttons_group([{
            label: 'dfc',
            icon: 'fa-table',
            callback: toggle_dfcleanser
        }])

        setup_popupcodecell();

    }

    function toggle_dfcleanser() {

        if (window.is_dfcleanser_loaded()) {
            if (get_dfc_mode() == 1) {
                if (is_pop_up_visible()) {
                    console.log(log_prefix + "\n" + "     toggle_dfcleanser : unload");
                    toggle_popupcodecell();
                    if (window.confirm("UnLoad dfcleanser?")) {
                        console.log(log_prefix + "\n" + "     toggle_dfcleanser : unloaded");
                        window.unload_dfcleanser();
                    }
                } else {
                    toggle_popupcodecell();
                }
            } else {
                if (window.confirm("Reset dfcleanser?")) {
                    process_pop_up_cmd(6);
                } else {
                    if (window.confirm("Unload dfcleanser?")) {
                        console.log(log_prefix + "\n" + "     toggle_dfcleanser : unload");
                        window.unload_dfcleanser();
                    }
                }
            }
        } else {

            if (window.confirm("Load dfcleanser?")) {
                console.log(log_prefix + "\n" + "     toggle_dfcleanser : load dfcleanser");
            } else {
                return;
            }

            window.load_dfcleanser_from_toolbar();
        }
    }

    function reset_dfcleanser() {
        console.log(log_prefix + "\n" + "reset_dfcleanser");
        if (window.is_dfcleanser_loaded()) {
            window.load_dfcleanser_chapter(0);
        }
    }

    function callback_notebook_renamed() {
        console.log(log_prefix + "\n" + "callback_notebook_renamed");
    }

    function load_ipython_extension() {


        // add css
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = requirejs.toUrl("./dfcleanser.css");
        document.getElementsByTagName("head")[0].appendChild(link);

        /*
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = requirejs.toUrl("./slick-default-theme.css");
        document.getElementsByTagName("head")[0].appendChild(link);
        */

        /*
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = requirejs.toUrl("./jquery-ui-1.8.16.custom.css");
        document.getElementsByTagName("head")[0].appendChild(link);
        */

        /*
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = requirejs.toUrl("./examples.css");
        document.getElementsByTagName("head")[0].appendChild(link);
        */


        /*
        var link = document.createElement("link");
        link.type = "text/css";
        link.rel = "stylesheet";
        link.href = requirejs.toUrl("./slick.grid.css");
        document.getElementsByTagName("head")[1].appendChild(link);
        */


        load_buttons();

        if (Jupyter.notebook.kernel) {
            console.log(log_prefix + "[Load]\n" + "     dfcleanser extension loaded");
            events.on('kernel_ready.Kernel', sync_notebook);
        } else {
            events.on('kernel_ready.Kernel', sync_notebook);
        }
    }

    //$([IPython.events]).on('notebook_renamed.Notebook', function(){
    //    console.log("Notebook name has been changed");
    //   /* Here u can call your code */
    //});


    return {
        load_ipython_extension: load_ipython_extension
    };

});