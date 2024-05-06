"""
# cfg 
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sept 13 22:29:22 2017

@author: Rick
"""
import sys
this = sys.modules[__name__]

import json 
import os

DEBUG_DISPLAY_PARMS     =   False
DEBUG_DFC_MGR           =   False


"""
#--------------------------------------------------------------------------
#   local helper functions
#--------------------------------------------------------------------------
"""
def display_javascript_HTML(html) :
    from IPython.core.display import display 
    display(html)#, metadata=dict(isolated=True))


def run_javascript(jscript, errmsg) :

    try :            
        from IPython.core.magics.display import Javascript
        display_javascript_HTML(Javascript(jscript))
    except :
        print(errmsg,jscript)
        
def does_dir_exist(path) :
    if(os.path.exists(path)) :
        if(os.path.isdir(path)) :   
            return(True)
        else :
            return(False)
    
def make_dir(path) :
    try :
        os.mkdir(path)
        return()
    
    except FileExistsError:
        return()

def does_file_exist(path) :
    if(os.path.exists(path)) :
        if(os.path.isfile(path)) :   
            return(True)
        else :
            return(False)
"""
#--------------------------------------------------------------------------
#   dfcleanser common notebook file and path functions
#--------------------------------------------------------------------------
"""
    
def get_common_files_path() :
    common_files_path = os.path.join(get_dfcleanser_location(),"files")
    return(common_files_path + "\\")   

def get_notebook_files_path() :
    notebook_files_path = os.path.join(get_dfcleanser_location(),"files","notebooks")
    return(notebook_files_path + "\\")   

def get_dfcleanser_location()  :

    import os
    import dfcleanser
    ppath = os.path.abspath(dfcleanser.__file__)
    #print("dfc path",len(ppath),ppath)   

    initpyloc = ppath.find("__init__.py")
    
   # print("initpyloc",initpyloc)
    if(initpyloc > 0) :
        ppath = ppath[:initpyloc]
        #print("ppath",ppath)

    return(ppath)

"""    
#--------------------------------------------------------------------------
#   dfcleanser sync jupyter with js 
#--------------------------------------------------------------------------
"""
def sync_with_js(parms) :
    DataframeCleansercfg.sync_js(parms)    

def get_notebookname() :
    try :
        run_javascript("window.getNotebookName();","Unable to get notebook name")
    except :
        print("getNotebookName error")
        
def get_notebookpath() :
    try :
        run_javascript("window.getNotebookPath();","Unable to get notebook path")
    except :
        print("getNotebookPath error")
    


        
"""
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#   dfcleanser dataframe objects
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
"""

"""
#--------------------------------------------------------------------------
#   javascript chapter ids
#--------------------------------------------------------------------------
"""

DC_CONSOLE_ID               =   0
DC_SYSTEM_ID                =   1
DC_DATA_IMPORT_ID           =   2
DC_DATA_IMPORT_MORE_ID      =   14
DC_DATA_INSPECTION_ID       =   3  
DC_DATA_CLEANSING_ID        =   4
DC_DATA_TRANSFORM_ID        =   5
DC_DATA_EXPORT_ID           =   6

DC_GEOCODE_UTILITY_ID       =   7
DC_DF_BROWSER_ID            =   8
DC_CENSUS_ID                =   9
DC_ZIPCODE_UTILITY_ID       =   10
DC_GEOCODE_BULK_ID          =   11
DC_WORKING_TITLE_ID         =   12
DC_WORKING_CELL_ID          =   13


"""
#--------------------------------------------------------------------------
#   dfcleanser chapter ids
#--------------------------------------------------------------------------
"""
DataCleansing_ID        =   "DataCleansing"
DataExport_ID           =   "DataExport"
DataImport_ID           =   "DataImport"
DataInspection_ID       =   "DataInspection"
DataScripting_ID        =   "DataScripting"
DataTransform_ID        =   "DataTransform"
SWUtilities_ID          =   "SWUtilities"
SWGeocodeUtility_ID     =   "SWGeocodeUtility"
SWBulkGeocodeUtility_ID     =   "SWBulkGeocodeUtility"
SWZipcodeUtility_ID     =   "SWZipcodeUtility"
SWCensusUtility_ID      =   "SWCensusUtility"
System_ID               =   "System"
dfBrowserUtility_ID     =   "SWdfBrowserUtility"

DBUtils_ID              =   "DBUtils"
DumpUtils_ID            =   "DumpUtils"
Help_ID                 =   "Help"
GenFunction_ID          =   "GenFunction"


"""
#--------------------------------------------------------------------------
#    chapter current dataframe objects   
#--------------------------------------------------------------------------
"""
chapter_select_df_input_title             =   "Dataframe To Inspect"
chapter_select_df_input_id                =   "datainspectdf"
chapter_select_df_input_idList            =   ["didfdataframe"]

chapter_select_df_input_labelList         =   ["dataframe_to_inspect"]

chapter_select_df_input_typeList          =   ["select"]

chapter_select_df_input_placeholderList   =   ["dataframe to inspect"]

chapter_select_df_input_jsList            =   [None]

chapter_select_df_input_reqList           =   [0]

chapter_select_df_input_form              =   [chapter_select_df_input_id,
                                               chapter_select_df_input_idList,
                                               chapter_select_df_input_labelList,
                                               chapter_select_df_input_typeList,
                                               chapter_select_df_input_placeholderList,
                                               chapter_select_df_input_jsList,
                                               chapter_select_df_input_reqList]  



data_cleansing_df_input_id                =   "datacleansedf"
data_transform_df_input_id                =   "datatransformdf"
data_export_df_input_id                   =   "dataexportdf"
data_subset_df_input_id                   =   "datasubsetdf"



def display_no_dfs(chapterid) :
    """
    * --------------------------------------------------------
    * function : display status fro no dfs
    * 
    * parms :
    *  chapterid    -   chapter id
    *
    * returns : N/A
    * --------------------------------------------------------
    """
    
    if(chapterid == DataCleansing_ID) :         msg    =   "No dataframe imported to select for data cleansing"
    elif(chapterid == DataInspection_ID) :      msg    =   "No dataframe imported to select for data inspection"
    elif(chapterid == DataExport_ID) :          msg    =   "No dataframe imported to select for data export"
    elif(chapterid == DataTransform_ID) :       msg    =   "No dataframe imported to select for data transform"
    elif(chapterid == DataImport_ID)        :   msg    =   "No dataframe imported to select for data import"
    elif(chapterid == SWGeocodeUtility_ID)  :   msg    =   "No dataframe imported to select for geocoding"
    
    from dfcleanser.sw_utilities.DisplayUtils import get_status_note_msg_html
    get_status_note_msg_html(msg,width=50,left=180,display=True)

def delete_df(df) :
    """
    * -------------------------------------------------------------------------- 
    * function : delete df and memory
    * 
    * parms :
    *  df    -   df to delete
    *
    * returns : N/A
    * --------------------------------------------------------
    """
    
    del df
    import gc
    gc.collect()


"""
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#  dfc dataframe objects and methods
#
#   a dfc dataframe is an object that contains a descriptive, 
#   a pandas dataframe and descriptive notes
#
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
"""

"""
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#  dfc signals and slots
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
"""

"""
#--------------------------------------------------------------------------
#  dfc add and drop dataframe signals and slots
#--------------------------------------------------------------------------
"""

from PyQt5.QtCore import (pyqtSignal,QObject)
class add_df_signal(QObject) :

    new_add_df_signal   =   pyqtSignal(str)

    def issue_notice(self,dftitle) :
        self.new_add_df_signal.emit(dftitle)

    def connectSignal(self,callback) :
        self.new_add_df_signal.connect(callback)

#from dfcleanser.Qt.data_transform.DataTransform import DataTransformGui
DataTransform_add_df_signal     =   add_df_signal()
DataInspection_add_df_signal    =   add_df_signal()
DataCleansing_add_df_signal     =   add_df_signal()
DataExport_add_df_signal        =   add_df_signal()


"""
#--------------------------------------------------------------------------
#  df column changes
#--------------------------------------------------------------------------
"""

from PyQt5.QtCore import (pyqtSignal,QObject)
class df_column_change_signal(QObject) :

    new_column_change_signal   =   pyqtSignal(str)

    def issue_notice(self,dftitle) :
        self.new_column_change_signal.emit(dftitle)

    def connectSignal(self,callback) :
        self.new_column_change_signal.connect(callback)

#from dfcleanser.Qt.data_transform.DataTransform import DataTransformGui
df_Column_Changed_signal        =   df_column_change_signal()

#DataInspection_add_df_signal    =   add_df_signal()
#DataCleansing_add_df_signal     =   add_df_signal()
#DataExport_add_df_signal        =   add_df_signal()



"""
#--------------------------------------------------------------------------
#   dfcleanser Dataframe helper methods
#--------------------------------------------------------------------------
"""

def is_a_dfc_dataframe_loaded() :
    """
    * ---------------------------------------------------------------------
    * function : chek if a dfc dataframe is loaed in memory for usage
    *
    * returns : 
    *  True if a dfc dataframe loaded else False
    * --------------------------------------------------------------------
    """
    
    total_dfs   =   dfc_df_history.get_df_titles()
    
    if(total_dfs is None) :
        return(False)
    else :
        return(True)
    
    #return(dfc_dfs.is_a_dfc_dataframe_loaded()) 

   
def get_dfc_dataframe_df(df_title) :
    """
    * ---------------------------------------------------------------------
    * function : get a dfc datframe object dataframe attribute
    *
    * Parms : 
    *  title    :   dfc dataframe title
    * --------------------------------------------------------------------
    """
    
    df_info     =   dfc_df_history.get_df_info(df_title)
    
    if(df_info is None) :
        return(None)
    else :
        return(df_info.get_df())

    
def set_dfc_dataframe_df(df_title,df) :
    """
    * ---------------------------------------------------------------------
    * function : set a dfc datframe pandas dataframe attribute
    *
    * Parms : 
    *  title    :   dfc dataframe title
    * --------------------------------------------------------------------
    """
    
    dfc_df_history.set_df_info_dataframe(df_title,df)

    df_Column_Changed_signal.issue_notice(df_title)

    

def get_dfc_dataframe_notes(df_title) :
    """
    * ---------------------------------------------------------------------
    * function : get a dfc datframe note attribute
    *
    * Parms : 
    *  title    :   dfc dataframe title
    * --------------------------------------------------------------------
    """
    
    df_info     =   dfc_df_history.get_df_info(df_title)
    return(df_info.get_df_notes())

    
def set_dfc_dataframe_notes(df_title,notes) :
    """
    * ---------------------------------------------------------------------
    * function : set a dfc datframe note attribute
    *
    * Parms : 
    *  title    :   dfc dataframe title
    * --------------------------------------------------------------------
    """
    
    dfc_df_history.set_df_info_notes(df_title,notes)



def append_dfc_dataframe_notes(title,notes) :
    """
    * ---------------------------------------------------------------------
    * function : append a note to the dfc dataframe notes
    *
    * Parms : 
    *  title    :   dfc dataframe title
    * --------------------------------------------------------------------
    """
    dfc_notes   =   get_dfc_dataframe_notes(title)
    dfc_notes   =   dfc_notes + "\n--------\n" + notes
    dfc_dfs.set_dataframe_notes(title,notes)


"""
* --------------------------------------
* dfcleanser dataframe object methods
* --------------------------------------
"""  

def get_total_dfc_dataframes() :
    
    total_dfs   =   dfc_df_history.get_df_titles()
    if(not(total_dfs is None)) :
        return(len(total_dfs))
    else :
        return(0)

     
def rename_dfc_dataframe(oldtitle,newtitle) :
    """
    * ---------------------------------------------------------------------
    * function : rename a dfc datframe title attribute
    *
    * Parms : 
    *  title    :   dfc dataframe title
    * --------------------------------------------------------------------
    """
    
    dfc_dfs.rename_dataframe(oldtitle,newtitle)

     
def drop_dfc_dataframe(df_title) :
    """
    * ---------------------------------------------------------------------
    * function : drop a dfc datframe 
    *
    * Parms : 
    *  df_title    :   dfc dataframe title
    * --------------------------------------------------------------------
    """
    
    dfc_df_history.drop_dfc_dataframe(df_title)
    
    df_selects_list     =   ["didfdataframe","dcdfdataframe","dtdfdataframe","dedfdataframe","dgdfdataframe"]
    df_selects_cfgs_id  =   [CURRENT_INSPECTION_DF,CURRENT_CLEANSE_DF,CURRENT_TRANSFORM_DF,CURRENT_EXPORT_DF,CURRENT_GEOCODE_DF]  
    
    for i in range(len(df_selects_list)) : 
        
        drop_js     =   '$("#' + df_selects_list[i] + ' option[value=' + "'" + df_title + "'" + ']").remove();'
        run_javascript(drop_js,"fail update select : ") 
        
        current_df  =   get_config_value(df_selects_cfgs_id[i])
        
        if(current_df == df_title) :
            
            drop_config_value(df_selects_cfgs_id[i])    

            if(get_total_dfc_dataframes() > 0) :
        
                df_titles   =   get_dfc_dataframes_titles_list()
                change_selected_js = "$('#" + df_titles[0] + "').prop('selectedIndex', 1);" 
                run_javascript(change_selected_js,"fail update select : ")
                
                set_config_value(df_selects_cfgs_id[i],df_titles[0])


def add_df_to_dfc(df_title,df,df_source="",df_notes="")  :
    """
    * ---------------------------------------------------------------------
    * function : add a dfc dataframe object to available list
    * 
    * parms :
    *  df_title     - df title
    *
    * returns : 
    *  N/A 
    * --------------------------------------------------------------------
    """

    if(DEBUG_DFC_MGR) :
        print("[add_df_to_dfc] df_title : ",df_title)#,df)
    
    #add_df_signal
    dfc_df_history.add_dfc_df(df_title,df,df_source,df_notes)

    DataTransform_add_df_signal.issue_notice(df_title)
    DataInspection_add_df_signal.issue_notice(df_title)
    DataCleansing_add_df_signal.issue_notice(df_title)
    DataExport_add_df_signal.issue_notice(df_title)

    if(DEBUG_DFC_MGR) :
        print("[add_df_to_dfc] added : ",df_title,dfc_df_history.get_df_titles())


def rename_dfc_dataframe(oldName,newName) :

    print("[rename_dfc_dataframe] oldName,newName",oldName,newName)
    print("[rename_dfc_dataframe] get_dfc_dataframes_titles_list()",get_dfc_dataframes_titles_list())

    dfc_df_history.rename_dataframe(oldName,newName)

    print("[rename_dfc_dataframe] get_dfc_dataframes_titles_list()",get_dfc_dataframes_titles_list())


    DataTransform_add_df_signal.issue_notice(oldName)
    DataInspection_add_df_signal.issue_notice(oldName)
    DataCleansing_add_df_signal.issue_notice(oldName)
    DataExport_add_df_signal.issue_notice(oldName)

    DataTransform_add_df_signal.issue_notice(newName)
    DataInspection_add_df_signal.issue_notice(newName)
    DataCleansing_add_df_signal.issue_notice(newName)
    DataExport_add_df_signal.issue_notice(newName)



def get_dfc_dataframes_titles_list() :
    """
    * ---------------------------------------------------------
    * class : get a python list of dfc dataframes titles 
    * 
    * returns : 
    *  list of dfc dataframe titles 
    * --------------------------------------------------------
    """
    
    return(dfc_df_history.get_df_titles())


def get_dfc_dataframes_select_list(chapterid) :
    """
    * ---------------------------------------------------------
    * class : get the list of dfc dataframes for a select 
    * 
    * returns : 
    *  select list of dfc dataframe objects 
    * --------------------------------------------------------
    """
    
    df_select           =   {}
    df_select_titles    =   get_dfc_dataframes_titles_list()

    if(chapterid == DataInspection_ID)      :   default_df  =   get_config_value(CURRENT_INSPECTION_DF)
    elif(chapterid == DataCleansing_ID)     :   default_df  =   get_config_value(CURRENT_CLEANSE_DF)
    elif(chapterid == DataTransform_ID)     :   default_df  =   get_config_value(CURRENT_TRANSFORM_DF)
    elif(chapterid == DataExport_ID)        :   default_df  =   get_config_value(CURRENT_EXPORT_DF)
    elif(chapterid == DataImport_ID)        :   default_df  =   get_config_value(CURRENT_IMPORT_DF)
    elif(chapterid == SWGeocodeUtility_ID)  :   default_df  =   get_config_value(CURRENT_GEOCODE_DF)
    else                                    :   default_df  =   None
   
    if(not (df_select_titles is None) ) :
        if(default_df is None) :
            df_select.update({"default": df_select_titles[0]})
        else :
            df_select.update({"default": default_df})
            
        df_select.update({"list":df_select_titles})
        df_select.update({"callback":"select_chapter_df"})
        return(df_select)
    else :
        return(None)


"""
#--------------------------------------------------------------------------
#   user defined dataframe objects
#--------------------------------------------------------------------------
"""

def get_user_defined_df() :
    return(user_defined_df.get_user_df())   
def set_user_defined_df(user_df) :
    user_defined_df.set_user_df(user_df)  

class user_dataframe :
    """
    * ---------------------------------------------------------
    * class : dfc dataframe object
    * 
    * attributes :
    *  title     - dataframe title 
    *  df        - pandas dataframe object 
    *  notes     - dataframe descriptive notes 
    *
    * returns : 
    *  dataframe cleanser dataframe object 
    * --------------------------------------------------------
    """
    
    user_df    =   None
    
    def __init__(self):
        self.user_df     =   None
        
    def get_user_df(self)           : return(self.user_df)       
    def set_user_df(self,user_df)   : self.user_df = user_df       
 
user_defined_df     =   user_dataframe()




"""
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#   dfc dataframe objects
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
"""

"""
#--------------------------------------------------------------------------
#   individual dfc dataframe object
#--------------------------------------------------------------------------
"""
class dfc_dataframe :
    """
    * ---------------------------------------------------------
    * class : dfc dataframe object
    * 
    * attributes :
    *  title     - dataframe title 
    *  df        - pandas dataframe object 
    *  notes     - dataframe descriptive notes 
    *
    * returns : 
    *  dataframe cleanser dataframe object 
    * --------------------------------------------------------
    """
    
    dfc_df    =   [None,None,None]
    
    def __init__(self,titleparm,dfparm,notesparm=""):
        self.dfc_df     =   [titleparm,dfparm,notesparm]
        
    def get_title(self)     : return(self.dfc_df[0])       
    def get_df(self)        : return(self.dfc_df[1])       
    def get_notes(self)     : return(self.dfc_df[2])       

    def set_title(self,title)   : self.dfc_df[0] = title       
    def set_df(self,df)         : self.dfc_df[1] = df     
    def set_notes(self,notes)   : self.dfc_df[2] = notes  


CURRENT_INSPECTION_DF                   =   "currentinspectiondf"
CURRENT_CLEANSE_DF                      =   "currentcleansedf"
CURRENT_TRANSFORM_DF                    =   "currenttransformdf"
CURRENT_EXPORT_DF                       =   "currentexportdf"
CURRENT_IMPORT_DF                       =   "currentimportdf"
CURRENT_GEOCODE_DF                      =   "currentgeocodedf"
CURRENT_BULKGEOCODE_DF                  =   "currentbulkgeocodedf"
CURRENT_CENSUS_DF                       =   "currentcensusdf"
    

"""
#--------------------------------------------------------------------------
#   Dataframe Cleanser new dfc df 
#--------------------------------------------------------------------------
"""

def set_df_to_add_to_dfc(df) :
    df_to_add_to_dfc.set_df_to_add(df)    
def get_df_to_add_to_dfc() :
    return(df_to_add_to_dfc.get_df_to_add())    

class new_dfc_df_to_add :
    
    # instance variables
    df_to_add                 =   None
    
    # full constructor
    def __init__(self) :
        self.df_to_add                  =   None
    def set_df_to_add(self,df) :
        self.df_to_add                  =   df
    def get_df_to_add(self) :
        return(self.df_to_add)

df_to_add_to_dfc    =   new_dfc_df_to_add()


"""
#--------------------------------------------------------------------------
#   dfc dataframe dfs
#--------------------------------------------------------------------------
"""

def get_current_chapter_dfc_df_title(chapterId) :
    
    if(is_a_dfc_dataframe_loaded()) : 
        
        if(chapterId == DataCleansing_ID)           :   dftitle     =   CURRENT_CLEANSE_DF
        elif(chapterId == DataExport_ID)            :   dftitle     =   CURRENT_EXPORT_DF
        elif(chapterId == DataImport_ID)            :   dftitle     =   CURRENT_IMPORT_DF
        elif(chapterId == DataInspection_ID)        :   dftitle     =   CURRENT_INSPECTION_DF
        elif(chapterId == DataTransform_ID)         :   dftitle     =   CURRENT_TRANSFORM_DF
        elif(chapterId == SWGeocodeUtility_ID)      :   dftitle     =   CURRENT_GEOCODE_DF
        elif(chapterId == SWBulkGeocodeUtility_ID)  :   dftitle     =   CURRENT_BULKGEOCODE_DF
        elif(chapterId == SWCensusUtility_ID)       :   dftitle     =   CURRENT_CENSUS_DF
        else                                        :   dftitle     =   None
        
        if(dftitle is None) :
            return(None)
        else :
            
            current_df  =   get_config_value(dftitle)
            return(current_df)
    
    else :
        return(None)


def get_current_chapter_df(chapterId) :
    
    if(is_a_dfc_dataframe_loaded()) : 
        
        if(chapterId == DataCleansing_ID)           :   dftitle     =   CURRENT_CLEANSE_DF
        elif(chapterId == DataExport_ID)            :   dftitle     =   CURRENT_EXPORT_DF
        elif(chapterId == DataImport_ID)            :   dftitle     =   CURRENT_IMPORT_DF
        elif(chapterId == DataInspection_ID)        :   dftitle     =   CURRENT_INSPECTION_DF
        elif(chapterId == DataTransform_ID)         :   dftitle     =   CURRENT_TRANSFORM_DF
        elif(chapterId == SWGeocodeUtility_ID)      :   dftitle     =   CURRENT_GEOCODE_DF
        elif(chapterId == SWBulkGeocodeUtility_ID)  :   dftitle     =   CURRENT_BULKGEOCODE_DF 
        elif(chapterId == SWCensusUtility_ID)       :   dftitle     =   CURRENT_CENSUS_DF
        else                                        :   dftitle     =   None
        
        if(dftitle is None) :
            return(None)
        else :
        
            saved_df    =   get_config_value(dftitle)
            df          =   get_dfc_dataframe_df(saved_df)
            
            if(df is None) :
                drop_config_value(saved_df)
                return(None)
            else :
                return(df)
    
    else :
        return(None)

def set_current_chapter_df(chapterId,df,opstat) :
    
    if(is_a_dfc_dataframe_loaded()) : 
        
        if(chapterId == DataCleansing_ID)           :   dftitle     =   CURRENT_CLEANSE_DF
        elif(chapterId == DataExport_ID)            :   dftitle     =   CURRENT_EXPORT_DF
        elif(chapterId == DataImport_ID)            :   dftitle     =   CURRENT_IMPORT_DF
        elif(chapterId == DataInspection_ID)        :   dftitle     =   CURRENT_INSPECTION_DF
        elif(chapterId == DataTransform_ID)         :   dftitle     =   CURRENT_TRANSFORM_DF
        elif(chapterId == SWGeocodeUtility_ID)      :   dftitle     =   CURRENT_GEOCODE_DF
        elif(chapterId == SWBulkGeocodeUtility_ID)  :   dftitle     =   CURRENT_BULKGEOCODE_DF
        elif(chapterId == SWCensusUtility_ID)       :   dftitle     =   CURRENT_CENSUS_DF
        else                                        :   dftitle     =   None
        
        set_config_value(dftitle,chapterId)
     
        if(dftitle is None) :
            opstat.set_status(False)
            opstat.set_errorMsg("invalid chapter id")
        
        else :
            
            if(df is None) :
                opstat.set_status(False)
                opstat.set_errorMsg("invalid df")
            
            else :
                saved_df    =   get_config_value(dftitle)
                set_dfc_dataframe_df(saved_df,df)
            


"""
#--------------------------------------------------------------------------
#   dfc qt chapter objects
#--------------------------------------------------------------------------
"""

INSPECTION_QT_CHAPTER_ID        =   0
CLEANSE_QT_CHAPTER_ID           =   1
TRANSFORM_QT_CHAPTER_ID         =   2
EXPORT_QT_CHAPTER_ID            =   3
IMPORT_QT_CHAPTER_ID            =   4
SYSTEM_QT_CHAPTER_ID            =   5
GEOCODE_QT_CHAPTER_ID           =   6
ZIPCODE_QT_CHAPTER_ID           =   7
UNIQUES_QT_CHAPTER_ID           =   8
OUTLIERS_QT_CHAPTER_ID          =   9
DF_BROWSER_QT_CHAPTER_ID        =   10
CENSUS_QT_CHAPTER_ID            =   11


cell_title_template    =   """
    <div>
        <div style="text-align:center; background-color: #ffffff;">
            <table width="400" style="margin-left:0px; background-color: #ffffff;">
                <tr>
                    <td width="35%"><span style="vertical-align:top; "><img src="https://rickkrasinski.github.io/dfcleanser/graphics/CELLIMAGE" title="Click on to Control Chapter" width="100" height="100" onclick="control_qt_chapter(CALLBACKID)"; ></span></td>
                    <td width="65%"><span style="background-color: #ffffff; align:left; nowrap;  border:0; font-size:20px; font-weight:bold; margin-top:4px; vertical-align:top;">CELLTITLE</span></td>
                </tr>
            </table>
        </div>
        <br/>
    </div>
    <br>
"""

def build_qt_cell_title(chapterid) :

    new_title   =   str(cell_title_template)

    if(chapterid    ==  ZIPCODE_QT_CHAPTER_ID) :
        new_title   =   new_title.replace("CELLTITLE","Zipcode Utility&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =   new_title.replace("CELLIMAGE","ZipCodeChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(ZIPCODE_QT_CHAPTER_ID))
        return(new_title)

    elif(chapterid    ==  GEOCODE_QT_CHAPTER_ID) :
        new_title   =    new_title.replace("CELLTITLE","Geocode Utility&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =    new_title.replace("CELLIMAGE","GeocodeChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(GEOCODE_QT_CHAPTER_ID))
        return(new_title)
    
    elif(chapterid    ==  CENSUS_QT_CHAPTER_ID) :
        new_title   =    new_title.replace("CELLTITLE","Census Utility&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =    new_title.replace("CELLIMAGE","CensusChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(CENSUS_QT_CHAPTER_ID))
        return(new_title)
     
    elif(chapterid    ==  DF_BROWSER_QT_CHAPTER_ID) :
        new_title   =    new_title.replace("CELLTITLE","dataframe Browser&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =    new_title.replace("CELLIMAGE","DfBrowserChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(DF_BROWSER_QT_CHAPTER_ID))
        return(new_title)
   
    elif(chapterid    ==  SYSTEM_QT_CHAPTER_ID) :
        new_title   =   new_title.replace("CELLTITLE","System Utilities&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =   new_title.replace("CELLIMAGE","SystemChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(SYSTEM_QT_CHAPTER_ID))
        return(new_title)
    
    elif(chapterid    ==  IMPORT_QT_CHAPTER_ID) :
        new_title   =   new_title.replace("CELLTITLE","Data Import&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =   new_title.replace("CELLIMAGE","DataImportChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(IMPORT_QT_CHAPTER_ID))
        return(new_title)

    elif(chapterid    ==  INSPECTION_QT_CHAPTER_ID) :
        new_title   =   new_title.replace("CELLTITLE","Data Inspection&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =   new_title.replace("CELLIMAGE","DataInspectionChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(INSPECTION_QT_CHAPTER_ID))
        return(new_title)

    elif(chapterid    ==  CLEANSE_QT_CHAPTER_ID) :
        new_title   =   new_title.replace("CELLTITLE","Data Cleansing&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =   new_title.replace("CELLIMAGE","DataCleansingChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(CLEANSE_QT_CHAPTER_ID))
        return(new_title)

    elif(chapterid    ==  TRANSFORM_QT_CHAPTER_ID) :
        new_title   =   new_title.replace("CELLTITLE","Data Transform&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =   new_title.replace("CELLIMAGE","DataTransformChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(TRANSFORM_QT_CHAPTER_ID))
        return(new_title)
    
    elif(chapterid    ==  EXPORT_QT_CHAPTER_ID) :
        new_title   =   new_title.replace("CELLTITLE","Data Export&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_title   =   new_title.replace("CELLIMAGE","DataExportChapter.png")
        new_title   =   new_title.replace("CALLBACKID",str(EXPORT_QT_CHAPTER_ID))
        return(new_title)
CENSUS_QT_CHAPTER_ID

ZIPCODE_TITLE = build_qt_cell_title(ZIPCODE_QT_CHAPTER_ID)
GEOCODE_TITLE = build_qt_cell_title(GEOCODE_QT_CHAPTER_ID)
CENSUS_TITLE = build_qt_cell_title(CENSUS_QT_CHAPTER_ID)
DF_BROWSER_TITLE = build_qt_cell_title(DF_BROWSER_QT_CHAPTER_ID)
SYSTEM_TITLE = build_qt_cell_title(SYSTEM_QT_CHAPTER_ID)
DATA_IMPORT_TITLE = build_qt_cell_title(IMPORT_QT_CHAPTER_ID)
DATA_INSPECTION_TITLE = build_qt_cell_title(INSPECTION_QT_CHAPTER_ID)
DATA_CLEANSING_TITLE = build_qt_cell_title(CLEANSE_QT_CHAPTER_ID)
DATA_TRANSFORM_TITLE = build_qt_cell_title(TRANSFORM_QT_CHAPTER_ID)
DATA_EXPORT_TITLE = build_qt_cell_title(EXPORT_QT_CHAPTER_ID)


class dfc_qt_chapter :
    """
    * ---------------------------------------------------------
    * class : dfc qt chapter object
    * 
    * attributes :
    *  title        - qt chapter id 
    *  mainwindow   - pandas dataframe object 
    *
    * returns : 
    * --------------------------------------------------------
    """
    
    qt_chapter_id   =   None
    qt_main_window  =   None
    
    def __init__(self,chapter_id,main_window):
        self.qt_chapter_id     =      chapter_id
        self.qt_main_window    =      main_window
       
    def get_chapter_id(self)     : return(self.qt_chapter_id)       
    def get_main_window(self)    : return(self.qt_main_window)  


class dfc_qt_chapter_store :
    """
    * ---------------------------------------------------------
    * class : dfc qt chapter store
    * 
    * attributes :
    *  chapters       - qt chapter id 
    *
    * returns : 
    * --------------------------------------------------------
    """
    
    qt_chapters         =   {}
    
    def __init__(self):
        self.qt_chapters     =      {}

    def get_qt_chapters(self,chapter_key)     : 

        print(self.qt_chapters.get(chapter_key))
        return(self.qt_chapters.get(chapter_key))
    
    def get_qt_chapters_count(self,chapter_key)     : 
        chapter_list    =   self.get_qt_chapters(chapter_key)
        if(chapter_list is None) :
            return(0)
        else :
            return(len(chapter_list))


    def add_qt_chapter(self,chapter_key,gui,chapter_id)   : 

        #print("chapter_id",chapter_id)
        #print("chapter_key",chapter_key)

        new_chapter         =   dfc_qt_chapter(chapter_id,gui)

        current_chapters    =  self.qt_chapters.get(chapter_key)

        if(current_chapters is None) :
            current_chapters    =   []
            current_chapters.append(new_chapter)
            self.qt_chapters.update({chapter_key : current_chapters})
        else :
            current_chapters.append(new_chapter)
            self.qt_chapters.update({chapter_key : current_chapters})

        #self.dump_dfc_qt_chapters()    
 
    def close_qt_chapter(self,chapter_key) :
        chapters     =   self.qt_chapters.get(chapter_key)

        if(not (chapters is None)) :
            for i in range(len(chapters)) :
                chapters[i].get_main_window().close()
                self.qt_chapters.pop(chapter_key)
        
        self.qt_chapters.pop(chapter_key)

    def close_all_qt_chapters(self) :
        qt_chapters_keys    =   list(self.qt_chapters.keys())
        for i in range(len(qt_chapters_keys)) :
            self.close_qt_chapter(qt_chapters_keys[i])

    def close_qt_chapter_type(self,chapter_type) :
        qt_chapters_keys    =   list(self.qt_chapters.keys())
        for i in range(len(qt_chapters_keys)) :
            current_chapter     =   self.qt_chapters.get(qt_chapters_keys[i])
            if(current_chapter.get_chapter_id == chapter_type) :
                current_chapter.get_main_window.close()
                self.qt_chapters.pop(qt_chapters_keys[i])

    def dump_dfc_qt_chapters(self) :

        print("\ndfc_qt_chapters : DUMP")

        dfc_qt_chpts_keys   =   list(self.qt_chapters.keys())
        print("  dfc_qt_chapters keys : ",dfc_qt_chpts_keys)
        for i in range(len(dfc_qt_chpts_keys)) :
            print(    self.qt_chapters.get(dfc_qt_chpts_keys[i]))

"""
* ---------------------------------------------------------
*             global qt chapter store
* --------------------------------------------------------
"""
dfc_qt_chapters     =   dfc_qt_chapter_store()





"""
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#   dfcleanser config objects
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
"""

def get_cfg_parm_from_input_list(formid,label,labellist) :
    """
    * ---------------------------------------------------------
    * function : get a parm from cfg parms list
    * 
    * parms :
    *  formid     - form id
    *  label      - label of parm to get
    *  labellist  - input form label list
    *
    * returns : 
    *  geocoder engine 
    * --------------------------------------------------------
    """

    parmslist   =   get_config_value(formid+"Parms")
    
    if(not (parmslist == None)) :
        
        for i in range(len(labellist)) :
            if(label == labellist[i]) :
                return(parmslist[i])
                
    return(None)

     
"""
#--------------------------------------------------------------------------
#   Generic System config value keys
#--------------------------------------------------------------------------
"""
NOTEBOOK_TITLE          =   "NoteBookName"
NOTEBOOK_PATH           =   "NoteBookPath"
DFC_CELLS_LOADED        =   "dfCcellsLoaded"
DFC_CELLS_CBS           =   "dfCcellcbs"

"""
#--------------------------------------------------------------------------
#   DBUtils config value keys
#--------------------------------------------------------------------------
"""
CURRENT_DB_ID_KEY           =   "currentDBID"
CURRENT_DBLIB_ID_KEY        =   "currentDBLIBID"

"""
#--------------------------------------------------------------------------
#   Data Inspection config value keys
#--------------------------------------------------------------------------
"""
CURRENT_SCROLL_ROW_KEY      =   "currentdfScrollRow"

"""
#--------------------------------------------------------------------------
#   Cleansing config value keys
#--------------------------------------------------------------------------
"""
UNIQUES_FLAG_KEY                        =   "columnUniquesDisplay"
UNIQUES_RANGE_KEY                       =   "columnUniquesRange"

DATA_TYPES_FLAG_KEY                     =   "columnDataTypeChange"

CLEANSING_COL_KEY                       =   "datacleansingcolumn"
CLEANSING_ROW_KEY                       =   "datacleansingrow"
CHKNUM_COL_KEY                          =   "ChknumColumn"

ROW_CLEANSE_LAST_ROW                    =   "datacleansingLastRow"

"""
#--------------------------------------------------------------------------
#   Export config value keys
#--------------------------------------------------------------------------
"""
CURRENT_EXPORTED_FILE_NAME_KEY          =   "currentExportedFileName"
CURRENT_EXPORT_START_TIME               =   "exportStartTime"
CURRENT_EXPORT_HISTORY_TYPE             =   "currentExportHistoryType"

"""
#--------------------------------------------------------------------------
#   Import config value keys
#--------------------------------------------------------------------------
"""
CURRENT_IMPORTED_DATA_SOURCE_KEY        =   "currentImportedDataSource"
CURRENT_SQL_IMPORT_ID_KEY               =   "currentSQLImportID"
CURRENT_IMPORT_START_TIME               =   "importStartTime"
CURRENT_IMPORT_HISTORY_TYPE             =   "currentImportHistoryType"

"""
#--------------------------------------------------------------------------
#   Transform config value keys
#--------------------------------------------------------------------------
"""
DATA_TRANSFORM_COL_SELECTED_KEY         =   "DT_ColumnsSelected"
ADD_COL_COL_NAME_KEY                    =   "AddColumnColName"
ADD_COL_CODE_KEY                        =   "AddColumnCode"
COMPAT_COL_KEY                          =   "CompatColumn"

CURRENT_FN_TO_APPLY_KEY                 =   "CurrentApplyFN"
CURRENT_COL_TO_APPLY_FN_TO_KEY          =   "CurrentApplyCol"


"""
#--------------------------------------------------------------------------
#   Transform convert to category
#--------------------------------------------------------------------------
"""
CONVERT_TO_CAT_CURRENT_COLNAME          =   "DT_ConvCatColName"
CONVERT_TO_CAT_CURRENT_COLNAMES_LIST    =   "DT_ConvCatColNamesList"


"""
#--------------------------------------------------------------------------
#   Uniques List keys
#--------------------------------------------------------------------------
"""
CURRENT_UNIQUES_COLUMN_NAME             =   "CurrentUniqueColumnName"
CURRENT_UNIQUES_LAST_ROW_DISPLAYED      =   "CurrentUniqueLastRowDisplayed"
CURRENT_UNIQUES_ORDER_FLAG              =   "CurrentUniqueOrder"

NO_UNIQUES_RANKING                      =   0
LOW_TO_HIGH_UNIQUES_RANKING             =   1
HIGH_TO_LOW_UNIQUES_RANKING             =   2


"""
#--------------------------------------------------------------------------
#   Scripting config value keys
#--------------------------------------------------------------------------
"""
SCRIPT_LOG_KEY                          =   "ScriptLog"
BACKUP_SCRIPT_LOG_KEY                   =   "BackupScriptLog"
SCRIPTING_FLAG_KEY                      =   "ScriptingFlag"

"""
#--------------------------------------------------------------------------
#   SW Utilities config value keys
#--------------------------------------------------------------------------
"""
CURRENT_GEOCODER_KEY                    =   "currentGeocoder"
ARCGIS_BATCH_MAX_BATCH_SIZE_KEY         =   "arcgisMaxBatchSize"
ARCGIS_BATCH_SUGGESTED_BATCH_SIZE_KEY   =   "arcgisSuggestedBatchSize"

BULK_GEOCODE_MODE_KEY                   =   "bulkGeocodeMode"

BULK_GEOCODE_APPENDED_CSV_ID            =   "bulkgeocodeappendcsvid"
BULK_GEOCODE_EXPORTED_CSV_ID            =   "bulkgeocodeexportcsvid"
BULK_ERRORS_EXPORTED_CSV_ID             =   "bulkerrorsexportcsvid"

CURRENT_GENERIC_FUNCTION                =   "currentGenFunction"

CENSUS_DOWNLOAD_LISTS                   =   "censusdownloadlists"
CENSUS_CURRENT_MODE                     =   "censuscurrentmode"
CENSUS_DROP_DATASET_LISTS               =   "censusdropdataset"
CENSUS_DROP_SUBDATASET_LIST             =   "censusdropsubdataset"
CENSUS_CURRENT_DATASET                  =   "censuscurrentdataset"
CENSUS_CURRENT_GET_COLS_SUBDATA_ID      =   "censuscurrentgetcolssubdataid"
CENSUS_CURRENT_GET_COLS_SUBDATA_LISTS_ID      =   "censuscurrentgetcolssubdataidlists"


CENSUS_DATASET_TO_JOIN_FROM             =   "censusdatasettojoinfrom"

CENSUS_ADD_DATASETS_LIST                =   "censusadddatasets"
CENSUS_DROP_DATASETS_LIST               =   "censusdropdatasets"

CENSUS_CONFIGURE_DATASETS_LIST          =   "censusconfiguredatasets"
CENSUS_LOAD_TO_DFS_DATASETS_LIST        =   "censusloadtodfdatasets"

CENSUS_SELECTED_DATASET_ID              =   "censusdatasetid"
CENSUS_SELECTED_SUBSET_ID               =   "censussubsetid"


"""
#--------------------------------------------------------------------------
#   System config value keys
#--------------------------------------------------------------------------
"""
EULA_FLAG_KEY                           =   "EULARead"
SAVED_FILE_NAME_KEY                     =   "DCS_savedfilenname"
DFC_CURRENTLY_LOADED_KEY                =   "dfcleanserCurrentlyLoaded"
DFC_CHAPTERS_LOADED_KEY                 =   "dfcCurrentlyLoadedChapters"
CURRENT_DF_DISPLAYED_KEY                =   "dfcCurrentSelecteddf"

CURRENT_DFC_DF_DFTITLE                  =   "dfcdfdftitle"
CURRENT_DFC_DF_RUN_STEP                 =   "dfcdfCurrentStep"
CURRENT_DFC_DF_RUN_TSTAMPS              =   "dfcdfCurrentStepTstamp"

"""
#--------------------------------------------------------------------------
#   working column name
#--------------------------------------------------------------------------
"""
CURRENT_COL_NAME    =   "currentColumnName"

def get_current_col_name() :
    return(get_config_value(CURRENT_COL_NAME))


DEBUG_CFG   =   False


"""
#--------------------------------------------------------------------------
#   global keys that should be stored at the dfcleanser level
#--------------------------------------------------------------------------
"""
GlobalKeys     =   ["EULARead","geocoder","GoogleV3_querykwargs",
                    "arcgisgeocoderParms","binggeocoderParms","mapquestgeocoderParms",
                    "nomingeocoderParms","googlegeocoderParms","baidu_geocoderParms",
                    "googlebulkgeocoderParms","arcgisbatchgeocoderParms",
                    "bingbulkgeocoderParms","baidubulkgeocoderParms",
                    "PostgresqldbconnectorParms","MySQLdbconnectorParms","SQLitedbconnectorParms",
                    "OracledbconnectorParms","MSSQLServerdbconnectorParms","customdbconnectorParms",
                    "currentDBID","currentDBLIBID"]

def is_global_parm(key) :
    if(key in GlobalKeys) :
        return(True)
    else :
        return(False)


"""
#--------------------------------------------------------------------------
#   helper functions
#--------------------------------------------------------------------------
"""
def get_config_value(key) :
    return(DataframeCleansercfg.get_config_value(key))

def set_config_value(key, value, write_through=True) :
    DataframeCleansercfg.set_config_value(key,value,write_through)
    
def drop_config_value(key, write_through=True) :
    DataframeCleansercfg.drop_config_value(key, write_through)
    
def set_notebookName(nbname) :
    DataframeCleansercfg.set_notebookname(nbname)
    
def get_notebookName() :
    return(DataframeCleansercfg.get_notebookname())
    
def set_notebookPath(nbpath) :
    DataframeCleansercfg.set_notebookpath(nbpath)

def get_notebookPath() :
    return(DataframeCleansercfg.get_notebookpath())  



"""
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#   Dataframe Cleanser config class
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
"""

class DataframeCleansercfg :
    
    # instance variables
    
    # notebook specific cfg file data
    cfg_data                =   {}
    dfc_cfg_data            =   {}
    
    default_cfg_data        =   {}
    default_dfc_cfg_data    =   {"EULARead":"False"}
    
    notebookName            =   ""
    notebookPath            =   ""
    
    # Jupyter synced flag
    cfg_file_loaded         =   False
    dfc_cfg_file_loaded     =   False
    
    cfg_trace_log           =   []

    
    @staticmethod
    def add_to_cfg_error_log(msg,msg_type=0) :
        add_error_to_log(msg)
    
    """
    #--------------------------------------------------------------------------
    #   Dataframe Cleanser config initialization methods
    #--------------------------------------------------------------------------
    """
    
    # full constructor
    def __init__(self) :
        
        DataframeCleansercfg.init_cfg_file(0) 
        DataframeCleansercfg.init_cfg_file(1)

    @staticmethod
    def init_cfg_file(cfgType) :
        
        if(cfgType == 0) :
            DataframeCleansercfg.init_cfg_file_data(DataframeCleansercfg.get_cfg_dir_name(),
                                                    DataframeCleansercfg.get_cfg_file_name(),
                                                    0,
                                                    DataframeCleansercfg.cfg_file_loaded)
        else :
            DataframeCleansercfg.init_cfg_file_data(DataframeCleansercfg.get_dfc_cfg_dir_name(),
                                                    DataframeCleansercfg.get_dfc_cfg_file_name(),
                                                    1,
                                                    DataframeCleansercfg.dfc_cfg_file_loaded)
    
    @staticmethod
    def init_cfg_file_data(cfg_dirname,cfg_filename,cfgType,storeFlag) :
        
        import time
        
        retry_limit     =   5
        delay_seconds   =   1
        current_retry   =   0
        
        if(not (cfg_dirname is None)) :
            
            if(not (does_dir_exist(cfg_dirname))) :
                make_dir(cfg_dirname)
        
            if(not (does_file_exist(cfg_filename))) :
                
                # The very first cfg file load
                while(current_retry < retry_limit) :

                    try :
                    
                        with open(cfg_filename, 'w') as  cfg_file :
                            if(cfgType == 0) :
                                json.dump(DataframeCleansercfg.default_cfg_data,cfg_file)
                            else :
                                json.dump(DataframeCleansercfg.default_dfc_cfg_data,cfg_file)
                        
                            cfg_file.close()
                            
                        current_retry     =   retry_limit
                        
                        if(cfgType == 0) :
                            
                            DataframeCleansercfg.cfg_data   =   DataframeCleansercfg.default_cfg_data
                            DataframeCleansercfg.cfg_file_loaded = True
                            
                        else :
                            
                            DataframeCleansercfg.dfc_cfg_data   =   DataframeCleansercfg.default_dfc_cfg_data
                            DataframeCleansercfg.dfc_cfg_file_loaded = True
                            
                        break
                    
                    except :
                        current_retry   =   current_retry + 1
                        time.sleep(delay_seconds)
            
            # cfg file does exist
            else :
                
                while(current_retry < retry_limit) :
                    
                    try :

                        with open( cfg_filename, 'r') as  cfg_file :
                            
                            if(cfgType == 0) :
                                DataframeCleansercfg.cfg_data = json.load(cfg_file)
                            else :
                                DataframeCleansercfg.dfc_cfg_data = json.load(cfg_file)
                                
                            cfg_file.close()
                    
                        if(cfgType == 0) :
                            DataframeCleansercfg.cfg_file_loaded = True
                        else :
                            DataframeCleansercfg.dfc_cfg_file_loaded = True
                        
                        current_retry     =   retry_limit
                        
                        break
                    
                    except json.JSONDecodeError :
                        
                        try :
                                
                            with open( cfg_filename, 'w') as  cfg_file :
                                if(cfgType == 0) :
                                    json.dump(DataframeCleansercfg.default_cfg_data,cfg_file)
                                    DataframeCleansercfg.cfg_data = DataframeCleansercfg.default_cfg_data
                                else :
                                    json.dump(DataframeCleansercfg.default_dfc_cfg_data,cfg_file)
                                    DataframeCleansercfg.dfc_cfg_data = DataframeCleansercfg.default_dfc_cfg_data
                                
                            cfg_file.close()
                                
                        except :
                            add_error_to_log("[Load default cfg file Error - for json decode error] "  + str(sys.exc_info()[0].__name__),SEVERE_ERROR)


    """
    #--------------------------------------------------------------------------
    #   Dataframe Cleanser config files dirs and names
    #--------------------------------------------------------------------------
    """

    @staticmethod
    def get_dfc_qt_dir_name() :
        
        dfcdir  =   get_dfcleanser_location() 
        return(os.path.join(dfcdir,"Qt"))
   
    @staticmethod 
    def get_cfg_dir_name() :
        
        nbdir   =   DataframeCleansercfg.get_notebookpath()
        nbname  =   DataframeCleansercfg.get_notebookname()
        
        if((nbdir is None)or(nbname is None)) :
            return(None)
        else :
            return(os.path.join(nbdir,nbname + "_files"))
    
    @staticmethod
    def get_cfg_file_name() :
        
        cfgdir  =   DataframeCleansercfg.get_cfg_dir_name()
        nbname  =   DataframeCleansercfg.get_notebookname()
        
        if((cfgdir is None)or(nbname is None)) :
            return(None)
        else :
            return(os.path.join(cfgdir,nbname + "_config.json"))    
    
    @staticmethod
    def get_dfc_cfg_dir_name() :
        
        dfcdir  =   get_dfcleanser_location() 
        return(os.path.join(dfcdir,"files"))
    
    @staticmethod
    def get_dfc_cfg_file_name() :

        dfcdir  =   DataframeCleansercfg.get_dfc_cfg_dir_name()   
        
        if(dfcdir is None) :
            return(None)
        else :
            return(os.path.join(dfcdir,"dfcleanserCommon_config.json")) 
    
    @staticmethod
    def save_cfg_file(cfgType) :
        
        if(cfgType == 0) :
        
            if(DataframeCleansercfg.cfg_file_loaded) :
    
                try :
                    
                    with open(DataframeCleansercfg.get_cfg_file_name(), 'w') as cfg_file :
                        json.dump(DataframeCleansercfg.cfg_data,cfg_file)
                        cfg_file.close()
                    
                except :
                    add_error_to_log("[Save cfg file Error][cfg file] "  + str(sys.exc_info()[0].__name__),SEVERE_ERROR)
                     
            else :
                add_error_to_log("[Unable to Save cfg file Error : because cfg not loaded] ",SEVERE_ERROR)
       
        else :
            
            if(DataframeCleansercfg.dfc_cfg_file_loaded) :

                try :
                    with open(DataframeCleansercfg.get_dfc_cfg_file_name(), 'w') as cfg_file :
                        json.dump(DataframeCleansercfg.dfc_cfg_data,cfg_file)
                        cfg_file.close()
            
                except :
                    add_error_to_log("[Save dfc cfg file Error][dfc cfg file] "  + str(sys.exc_info()[0].__name__),SEVERE_ERROR)
        
    @staticmethod
    def is_loaded(cfgtype) :

        if(cfgtype == 0) :
        
            if(not (DataframeCleansercfg.cfg_file_loaded)) :
                DataframeCleansercfg.wait_for_cfg_file_load(0)
        
            if(not (DataframeCleansercfg.cfg_file_loaded)) :
                return(False)
            else :
                return(True)
                
        else :
            
            if(not (DataframeCleansercfg.dfc_cfg_file_loaded)) :
                DataframeCleansercfg.wait_for_cfg_file_load(1)
        
            if(not (DataframeCleansercfg.dfc_cfg_file_loaded)) :
                return(False)
            else :
                return(True)

    @staticmethod
    def wait_for_cfg_file_load(cfgtype) :
        
        import time
        
        if(cfgtype == 0) :
            load_flag   =   DataframeCleansercfg.cfg_file_loaded
        else :
            load_flag   =   DataframeCleansercfg.dfc_cfg_file_loaded
        
        if(not (load_flag)) :
            
            wait_for_load   =   True
            retry_limit     =   10
            retry_count     =   0
            retry_delay     =   0.1
            
            while(wait_for_load)  :
                
                time.sleep(retry_delay)  
                retry_count     =   retry_count + 1
                
                if(retry_count == retry_limit) :
                    wait_for_load = False
                else :
                    if(cfgtype == 0) :
                        if(DataframeCleansercfg.cfg_file_loaded) :
                            wait_for_load = False  
                    else :
                        if(DataframeCleansercfg.dfc_cfg_file_loaded) :
                            wait_for_load = False  
        
        if(cfgtype == 0) :
            
            if(not (DataframeCleansercfg.cfg_file_loaded)) :
                return(False)
            else :
                return(True)
                
        else :
            
            if(not (DataframeCleansercfg.dfc_cfg_file_loaded)) :
                return(False)
            else :
                return(True)

    @staticmethod        
    def get_config_value(key) :
        
        if(not(is_global_parm(key))) :
            
            if(DataframeCleansercfg.is_loaded(0)) :
                return(DataframeCleansercfg.cfg_data.get(key,None))
            else :
                DataframeCleansercfg.add_to_cfg_log("[get_config_value _ unable to load cfg_data] : "  + str(key) + " " + str(len(DataframeCleansercfg.cfg_data)),1)
                return(None)
                
        else :
            
            if(DataframeCleansercfg.is_loaded(1)) :
                return(DataframeCleansercfg.dfc_cfg_data.get(key,None))
            else :
                add_error_to_log("[get_config_value _ unable to load dfc_cfg_data] : "  + str(key) + " " + str(len(DataframeCleansercfg.cfg_data)),SEVERE_ERROR)
                return(None)
        
    @staticmethod        
    def set_config_value(key, value, write_through=True) :

        if(not(is_global_parm(key))) :
            
            if(DataframeCleansercfg.is_loaded(0)) :
                DataframeCleansercfg.cfg_data.update({key : value})
                if(write_through) :
                    DataframeCleansercfg.save_cfg_file(0)
            else :
                add_error_to_log("[set_config_value - unable to load cfg_data] : "  + str(key) + " " + str(len(DataframeCleansercfg.cfg_data)),SEVERE_ERROR)
                
        else :
            
            if(DataframeCleansercfg.is_loaded(1)) :
                DataframeCleansercfg.dfc_cfg_data.update({key : value})
                DataframeCleansercfg.save_cfg_file(1)
            else :
                add_error_to_log("[set_config_value - unable to load dfc_cfg_data] : "  + str(key) + " " + str(len(DataframeCleansercfg.dfc_cfg_data)),SEVERE_ERROR)
        
    @staticmethod       
    def drop_config_value(key, write_through) :
        
        if(not(is_global_parm(key))) :
            
            if(DataframeCleansercfg.is_loaded(0)) :
                popped  =   DataframeCleansercfg.cfg_data.pop(key,None)
                if(not (popped is None)) :
                    if(write_through) :
                        DataframeCleansercfg.save_cfg_file(0)
            else :
                add_error_to_log("[drop_config_value - unable to load cfg_data] : "  + str(key) + " " + str(len(DataframeCleansercfg.cfg_data)),SEVERE_ERROR)
                
        else :
            
            if(DataframeCleansercfg.is_loaded(1)) :
                popped  =   DataframeCleansercfg.dfc_cfg_data.pop(key,None)
                if(not (popped is None)) :
                    DataframeCleansercfg.save_cfg_file(1)
            else :
                add_error_to_log("[drop_config_value - unable to load dfc_cfg_data] : "  + str(key) + " " + str(len(DataframeCleansercfg.dfc_cfg_data)),SEVERE_ERROR)


    #---------------------------------------------------
    #   dfcleanser common values
    #--------------------------------------------------- 
    @staticmethod
    def set_notebookname(nbname) :
        DataframeCleansercfg.notebookName = nbname

    @staticmethod
    def set_notebookpath(nbpath) :
        DataframeCleansercfg.notebookPath = nbpath
        DataframeCleansercfg.init_cfg_file(0)
        DataframeCleansercfg.init_cfg_file(1)
        
    @staticmethod    
    def get_notebookname() :
        return(DataframeCleansercfg.notebookName) 
    @staticmethod    
    def get_notebookpath() :
        return(DataframeCleansercfg.notebookPath) 

    @staticmethod
    def sync_js(parms) :

        nbname  =   parms[0]
        DataframeCleansercfg.set_notebookname(nbname)
        get_notebookpath()
        
        print("sync_js : reset_dfcleanser_chapter")
        init_dfc_console_js  =   "reset_dfcleanser_chapter(0);"
        #print(set_current_value_js)
        from dfcleanser.common.common_utils import run_jscript
        run_jscript(init_dfc_console_js,"fail to change col stats html : ")

        
"""
* ----------------------------------------------------
# static instantiation of the config data object
* ----------------------------------------------------
"""    
DataframeCleanserCfgData    =   DataframeCleansercfg()

def get_df_notebookpath() :
    return(DataframeCleanserCfgData.get_notebookpath())

def get_df_notebookname() :
    return(DataframeCleanserCfgData.get_notebookname())

def get_df_cfg_dir_name() :
    return(DataframeCleanserCfgData.get_cfg_dir_name())



"""
#------------------------------------------------------------------
#------------------------------------------------------------------
#   generic dfcleanser error logger
#------------------------------------------------------------------
#------------------------------------------------------------------
"""  

SEVERE_ERROR    =   1
MINOR_ERROR     =   2


def add_error_to_log(msg,errType) :
    dfc_erorr_log.add_error_to_dfc_log(msg)

def dump_error_log() :
    elog    =   dfc_erorr_log.get_error_log() 
    
    if(len(elog) > 0) :
        for i in range(len(elog)) :
            print("[",str(i),"] : ",str(elog[i]))
   
def clear_error_log() :
    dfc_erorr_log.clear_log() 


class DataframeCleanserErrorLogger :
    
    # instance variables
    
    # error log
    error_log               =   []
    error_log_loaded        =   False
    
    # full constructor
    def __init__(self) :
        
        self.error_log               =   []
        self.error_log_loaded        =   False
 
        self.init_errorlog_file() 
        
    def get_errorlog_dir_name(self) :
        
        from dfcleanser.common.cfg import get_notebookPath, get_notebookName
        nbdir   =   get_notebookPath()
        nbname  =   get_notebookName()
        
        if((nbdir is None)or(nbname is None)) :
            return(None)
        else :
            return(os.path.join(nbdir,nbname + "_files"))
   
    def get_errorlog_file_name(self) :
        
        from dfcleanser.common.cfg import get_notebookName
        eldir   =   self.get_errorlog_dir_name()
        nbname  =   get_notebookName()
        
        if((eldir is None)or(nbname is None)) :
            return(None)
        else :
            return(os.path.join(eldir,nbname + "_errorlog.json"))    
    
    def init_errorlog_file(self) :
        
        errorlog_dirname   =   self.get_errorlog_dir_name()
        if(not (errorlog_dirname is None)) :
            
            if(not (does_dir_exist(errorlog_dirname))) :
                make_dir(errorlog_dirname)
        
            errorlog_filename   =   self.get_errorlog_file_name()
        
            if(not (does_file_exist(errorlog_filename))) :

                with open(errorlog_filename, 'w') as error_file :
                    json.dump(self.error_log,error_file)
                    error_file.close()
            else :
                
                try :

                    with open(errorlog_filename, 'r') as errorlog_file :
                        self.errorlog = json.load(errorlog_file)
                        errorlog_file.close()
                        
                    self.error_log_loaded = True
                    
                except json.JSONDecodeError :
                    self.errorlog.append("Error Log File Corrupted")
                except :
                    self.errorlog.append("[Load Error Log Error] "  + str(sys.exc_info()[0].__name__))
        
    def save_errorlog_file(self) :
        
        if(1) :#self.error_log_loaded) :
    
            try :
                with open(self.get_errorlog_file_name(), 'w') as errorlog_file :
                    json.dump(self.error_log,errorlog_file)
                    errorlog_file.close()
            
            except :
                self.add_error_to_dfc_log("[Save Error Log Error] "  + str(sys.exc_info()[0].__name__))    
   
    def add_error_to_dfc_log(self,msg) :
        
        import datetime
        date = datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        
        self.error_log.append("[" + date + "]" + msg) 
        self.save_errorlog_file()   
  
    def get_error_log(self) :
        
        return(self.error_log) 

    def clear_log(self) :
        self.error_log               =   []
        

    
dfc_erorr_log   =   DataframeCleanserErrorLogger()  



"""
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#  dfc dataframe storage class
#
#   a dfc dataframe is an object that contains a description, 
#   a pandas dataframe and descriptive notes
#
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
"""


"""
#--------------------------------------------------------------------------
#   dfc dataframes store
#--------------------------------------------------------------------------
"""


class dfc_dataframes :
    
    dcdataframes    =   []

    def __init__(self):
        self.dcdataframes   =   []
        
        drop_config_value(CURRENT_INSPECTION_DF)
        drop_config_value(CURRENT_CLEANSE_DF)
        drop_config_value(CURRENT_TRANSFORM_DF)
        drop_config_value(CURRENT_EXPORT_DF)
        drop_config_value(CURRENT_IMPORT_DF)
        drop_config_value(CURRENT_GEOCODE_DF)

    def is_a_dfc_dataframe_loaded(self) :
        if(len(self.dcdataframes) > 0) :
            return(True)
        else :
            return(False)
        
    """
    * ------------------------------------
    * add or drop dfc dataframes 
    * ------------------------------------
    """        
    def add_dataframe(self,dfcdf) :
        for i in range(len(self.dcdataframes)) :
            if(self.dcdataframes[i].get_title() == dfcdf.get_title()) :
                self.drop_dataframe(dfcdf.get_title())    
        
        self.dcdataframes.append(dfcdf)
        
    def drop_dataframe(self,title) :
            
        dfindex     =   self.get_df_index(title)
        if(dfindex > -1) :
            del self.dcdataframes[dfindex]

    """
    * ------------------------------------
    * get dfc dataframe components
    * ------------------------------------
    """        
    def get_dataframe(self,title=None) :
        if(title == None) :
            dfindex     =   self.get_df_index(self.current_df)
        else :
            dfindex     =   self.get_df_index(title)
            
        if(dfindex > -1) :            
            return(self.dcdataframes[dfindex].get_df())
        else :
            return(None)
    
    def update_dataframe(self,title,df) :
        if(title == None) :
            dfindex     =   self.get_df_index(self.current_df)
        else :
            dfindex     =   self.get_df_index(title)
            
        if(dfindex > -1) :            
            return(self.dcdataframes[dfindex].set_df(df))
        else :
            print("no dataframe found for " + title)
                
    def get_dfc_dataframe(self,title) : 
        dfc_index   =  self.get_df_index(title)
        if(dfc_index == -1) :
            return(None)
        else :
            return(self.dcdataframes[dfc_index])
    
    def get_dataframe_notes(self,title) :
        if(title == None) :
            dfindex     =   self.get_df_index(self.current_df)
            if(dfindex > -1) :            
                return(self.dcdataframes[dfindex].get_notes())
            else :
                return(None)
        else :
            dfindex     =   self.get_df_index(title)
            if(dfindex > -1) :            
                return(self.dcdataframes[dfindex].get_notes())
            else :
                return(None)
    
    def set_dataframe_notes(self,title,notes) :
        if(title == None) :
            dfindex     =   self.get_df_index(self.current_df)
            if(dfindex > -1) :            
                self.dcdataframes[dfindex].set_notes(notes)
        else :
            dfindex     =   self.get_df_index(title)
            if(dfindex > -1) :            
                self.dcdataframes[dfindex].set_notes(notes)

    def rename_dataframe(self,oldName,newName) :

        print("\n[rename_dataframe] oldName,newName",oldName,newName)
        print("[rename_dataframe] self.dcdataframes",self.get_dataframe_titles(),self.dcdataframes)
        dfindex     =   self.get_df_index(oldName)

        print("[rename_dataframe] dfindex",dfindex)
        if(dfindex > -1) :  

            df_info     =   self.dcdataframes[dfindex].get_df()
            print("\n[rename_dataframe] oldName,newName",oldName,newName)          
            self.dcdataframes[dfindex].set_title(newName)

            print("\n[rename_dataframe] self.dcdataframes",self.get_dataframe_titles())
            
        #    if(oldName == self.current_df) :
        #        self.current_df     =   newName
                
    def get_dataframe_titles(self) :
        
        if(len(self.dcdataframes) > 0) :
            titles  =   []
            for i in range(len(self.dcdataframes)) :
                titles.append(self.dcdataframes[i].get_title())
                
            return(titles)
        else :
            return(None)
            
    def get_df_index(self,title) :
        
        for i in range(len(self.dcdataframes)) :

            print("get_title",self.dcdataframes[i].get_title(),title)
            if(self.dcdataframes[i].get_title() == title) :
                return(i)
                
        return(-1)
        
    def get_df_count(self) :
        return(len(self.dcdataframes))
        
"""
#--------------------------------------------------------------------------
#   dfc dataframe factory object
#--------------------------------------------------------------------------
"""
dfc_dfs     =   dfc_dataframes()




"""
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#   dfcleanser cells functions
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
"""


def get_util_chapters_loaded() :
    
    cellsList   =   get_config_value(DFC_CHAPTERS_LOADED_KEY)
    utilcbs     =   [0,0,0,0,0,0]

    if(not (cellsList == None)) :
        
        if(cellsList[21])    :   utilcbs[0] = 1
        if(cellsList[22])    :   utilcbs[1] = 1
        if(cellsList[23])    :   utilcbs[2] = 1
        if(cellsList[24])    :   utilcbs[3] = 1
        if(cellsList[25])    :   utilcbs[4] = 1
        if(cellsList[26])    :   utilcbs[5] = 1
        
    return(utilcbs)
   

def set_chapters_loaded(cellsList) :
    
    set_config_value(DFC_CHAPTERS_LOADED_KEY, cellsList,True)
   

#def get_loaded_cells() :

#    run_javascript("window.getdfcChaptersLoaded();",
#                   "Unable to get cells loaded")
    
#    from dfcleanser.common.common_utils import log_debug_dfc
#    log_debug_dfc(-1,"get_loaded_cells")


def check_if_dc_init() :
    
    if( not(DataframeCleanserCfgData.get_notebookname() == None) ) :
        if( not(DataframeCleanserCfgData.get_notebookpath() == None) ) :  
            return(True)
    else :
        return(False)

        
def save_current_notebook() :

    run_javascript("window.saveCurrentNotebook();",
                   "Unable to save notebook")
    
    from dfcleanser.common.common_utils import log_debug_dfc
    log_debug_dfc(-1,"save current notebook")



"""
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#   dfcleanser common notebook and path functions
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
"""

def create_notebook_dir_and_cfg_files(notebookname,nbpath) :
    
    # create the proper dir
    os.chdir(os.path.join(nbpath))
    os.makedirs("./" + notebookname + "_files" + "/")
    os.chdir(nbpath + "/" + notebookname + "_files")
                
    # create the notebook specific files
    fname = notebookname + "_config.json"
    initcfg = {NOTEBOOK_TITLE : notebookname}
                
    with open(fname,'w') as dfc_cfg_file :
        json.dump(initcfg,dfc_cfg_file)
        dfc_cfg_file.close()
                
    fname = notebookname + "_scriptlog.json"
    initslog = {NOTEBOOK_TITLE : notebookname}
                
    with open(fname,'w') as dfc_script_file :
        json.dump(initslog,dfc_script_file)
        dfc_script_file.close()
    

def check_notebook_dir_and_cfg_files(notebookname) :
    
    nbpath  =  DataframeCleanserCfgData.get_notebookpath()
    
    if(not(nbpath == None)) :

        if(os.path.exists(nbpath + "/" + notebookname + "_files")) :
            if(os.path.isdir(nbpath + "/" + notebookname + "_files")) :
                
                # if no config file create one
                if(not(os.path.exists(nbpath + "/" + notebookname + "_files" + "/" + notebookname + "_config.json"))) : 
                    # create the initial config file 
                    fname = notebookname + "_config.json"
                    initcfg = {NOTEBOOK_TITLE : notebookname}
                    
                    with open(fname,'w') as dfc_cfg_file :
                        json.dump(initcfg,dfc_cfg_file)
                        dfc_cfg_file.close()
                
                # if no scriptlog file create one
                if(not(os.path.exists(nbpath + "/" + notebookname + "_files" + "/" + notebookname + "_scriptlog.json"))) : 
                    # create the initial config file 
                    fname = notebookname + "_scriptlog.json"
                    initslog = {NOTEBOOK_TITLE : notebookname}
                    
                    with open(fname,'w') as dfc_script_file :
                        json.dump(initslog,dfc_script_file)
                        dfc_script_file.close()
                
            else :
                # delete it if it is a file and not a dir
                try :
                    os.remove(nbpath + "/" + notebookname)
                    
                    import win32api
                    win32api.MessageBox(None,"remove cfg dir file","remove",1)

                    create_notebook_dir_and_cfg_files(notebookname,nbpath)
                except FileNotFoundError :
                    print("[create_notebook_dir_and_cfg_files : remove dir ] ",nbpath + "_files" + "\\" + notebookname,str(sys.exc_info()[0].__name__))
                except Exception :
                    print("[create_notebook_dir_and_cfg_files : remove dir ] ",nbpath + "_files" + "\\" + notebookname,str(sys.exc_info()[0].__name__))
                
        else :
            
            # notebook path and name not found so create them
            try :
                create_notebook_dir_and_cfg_files(notebookname,nbpath)
            except FileNotFoundError :
                print("[create_notebook_dir_and_cfg_files : remove dir ] ",nbpath + "_files" + "\\" + notebookname,str(sys.exc_info()[0].__name__))
            except Exception :
                print("[create_notebook_dir_and_cfg_files : remove dir ] ",nbpath + "_files" + "\\" + notebookname,str(sys.exc_info()[0].__name__))



"""
#------------------------------------------------------------------
#   dfc dataframe object
#------------------------------------------------------------------
"""
class dfc_df_mgr_dataframe :
    
    df_dataframe                =   None
    df_title                    =   None
    
    df_source                   =   ""
    df_notes                    =   ""
    
    # full constructor
    def __init__(self,df,title,source="",notes="") :

        self.df_dataframe       =   df
        self.df_title           =   title
        self.df_source          =   source
        self.df_notes           =   notes
    
    def get_df(self) :
        return(self.df_dataframe)
        
    def get_df_title(self) :
        return(self.df_title)
        
    def get_df_source(self) :
        return(self.df_source)
       
    def get_df_notes(self) :
        return(self.df_notes)
    
    def set_df(self,df) :
        self.df_dataframe = df
    
    def set_df_title(self,df_title) :
        self.df_title = df_title
        
    def set_df_notes(self,df_notes) :
        self.df_notes = df_notes
       
    def set_df_source(self,df_source) :
        self.df_source = df_source
        
    def dump(self) :
        print("\ndf",len(self.df_dataframe))        
        print("df_title",self.df_title)
        print("df_source",self.df_source)
        print("df_notes",self.df_notes)



"""
#------------------------------------------------------------------
#   dfc dataframe history object
#------------------------------------------------------------------
"""
class dfc_df_mgr_dataframe_store :
    
    dfc_df_mgr_history          =   {}
    new_df                      =   None
    
    # full constructor
    def __init__(self) :
        
        self.dfc_df_mgr_history          =   {}
        #self.load_history_file()

        self.new_df     =   add_df_signal()
    
    def get_new_df_signal(self) :

        return(self.new_df)

    def send_new_df_signal(self,dftitle) :

        self.new_df.issue_notice(dftitle)
    
    def get_df_titles(self) :
    
        if(len(self.dfc_df_mgr_history) > 0) :
        
            df_titles   =   list(self.dfc_df_mgr_history.keys())
            df_titles.sort()
            return(df_titles)
        
        else :
            return(None)
    
    def get_df_info(self,df_title) :
    
        if(len(self.dfc_df_mgr_history)) :
            return(self.dfc_df_mgr_history.get(df_title))
        else :
            return(None)
 
    def add_dfc_df(self,df_title,df,df_source,df_notes) :
        
        try :
            df_info     =   dfc_df_mgr_dataframe(df,df_title,df_source,df_notes)
            self.dfc_df_mgr_history.update({df_title : df_info})
            self.new_df.emit()
        except :
            from dfcleanser.common.cfg import add_error_to_log, SEVERE_ERROR
            add_error_to_log("[add_dfc_df Error] " + df_title + str(sys.exc_info()[0].__name__),SEVERE_ERROR)
            
    def set_df_info_dataframe(self,df_title,df) :
        
        df_info     =   self.get_df_info(df_title)
        
        if(not (df_info is None)) :
            
            df_info.set_df(df)
            self.dfc_df_mgr_history.update({df_title : df_info})  
            
    def set_df_info_notes(self,df_title,notes) :
        
        df_info     =   self.get_df_info(df_title)
        
        if(not (df_info is None)) :
            
            df_info.set_df_notes(notes)
            self.dfc_df_mgr_history.update({df_title : df_info})  
            
    def rename_dataframe(self,oldtitle,newtitle) :

        df_info     =   self.get_df_info(oldtitle) 

        if(not (df_info is None)) :

            self.dfc_df_mgr_history.pop(oldtitle)
            df_info.set_df_title(newtitle)
            self.dfc_df_mgr_history.update({newtitle : df_info})             
    
    def drop_dfc_dataframe(self,df_title) :
        
        try :
            self.dfc_df_mgr_history.pop(df_title)
        except :
            from dfcleanser.common.cfg import add_error_to_log, SEVERE_ERROR
            add_error_to_log("[drop_dfc_df Error] " + df_title + str(sys.exc_info()[0].__name__),SEVERE_ERROR)
          
    def dump(self) :
        print("\ndf_titles",self.get_df_titles())

dfc_df_history  =   dfc_df_mgr_dataframe_store()

