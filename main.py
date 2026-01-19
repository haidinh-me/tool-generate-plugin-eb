# lib parser
import argparse
# lib logging
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, 
    handlers=[logging.StreamHandler()],
    datefmt='%Y-%m-%d %H:%M:%S', 
    format='[%(asctime)s  %(levelname)s] --> %(module)s : %(message)s'
)

import re
import os
import glob
import shutil

def Read_Argument():
    parser = argparse.ArgumentParser(description="write args") 
    parser.add_argument("-m", "--module", help="Name your module!", nargs='+', default=None) 
    return parser.parse_args()

class mTest():
    Userconfig_variable = "Userconfig.py"
    if(os.path.exists(Userconfig_variable)):
        exec(open(Userconfig_variable).read())

    variable = "Variable.py"
    if(os.path.exists(variable)):
        exec(open(variable).read())

class mRunTool():
    def __init__(self, module_name):
        self.MODULE = module_name
        self.mTest = mTest()
        self.State = "FAILED"
        print("")

    def LetStart(self):
        logging.info(f"******************************************")
        logging.info(f"Start generate plugin {self.MODULE}")
        logging.info(f"******************************************")

    def LetEnd(self):
        logging.info(f"******************************************")
        logging.info(f"End generate plugin {self.MODULE} ==> [{self.State}] ")
        logging.info(f"******************************************\n")

    def Copy_Module(self):
        shutil.copytree('Template_Empty', f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}')
    
    def Replace_In_File(self,dir_replace):
        with open(f'Template/{dir_replace}',"r") as file:
            data = file.read()
            data = data.replace("@MODULE@", self.MODULE)
            data = data.replace("@VERSION_MAJOR@", self.mTest.VERSION_MAJOR)
            data = data.replace("@VERSION_MINOR@", self.mTest.VERSION_MINOR)
            data = data.replace("@VERSION_PATCH@", self.mTest.VERSION_PATCH)
            data = data.replace("@RELEASE_TYPE@", self.mTest.RELEASE_TYPE)
            data = data.replace("@AUTOSAR_RELEASE_VERSION_MAJOR@", self.mTest.AUTOSAR_RELEASE_VERSION_MAJOR)
            data = data.replace("@AUTOSAR_RELEASE_VERSION_MINOR@", self.mTest.AUTOSAR_RELEASE_VERSION_MINOR)
            data = data.replace("@AUTOSAR_RELEASE_VERSION_PATCH@", self.mTest.VERSION_MAJOR)
            data = data.replace("@ASC_AUTOSAR_VERSION@", self.mTest.ASC_AUTOSAR_VERSION)
            data = data.replace("@AUTOSAR_VERSION@", self.mTest.AUTOSAR_VERSION)
            data = data.replace("@COMPANY_NAME@", self.mTest.COMPANY_NAME)
            data = data.replace("@VENDOR_ID@", self.mTest.VENDOR_ID)
            data = data.replace("@MANDATORY_T@", self.mTest.MANDATORY_T)
            data = data.replace("@INSTANCE_ID@", self.mTest.INSTANCE_ID)
            data = data.replace("@RESOURCE_PACKAGE@", self.mTest.RESOURCE_PACKAGE)
            data = data.replace("@TARGET_ARCHITECTURE@", self.mTest.TARGET_ARCHITECTURE)
            data = data.replace("@SILICON_NAME@", self.mTest.SILICON_NAME)
            data = data.replace("@RELEASE_NAME@", self.mTest.RELEASE_NAME)
            data = data.replace("@COPYRIGHT@", self.mTest.COPYRIGHT)
        with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/{dir_replace}',"w+") as outfile:
            outfile.write(data)

    def Replace_Variable(self):
        self.Replace_In_File("META-INF/MANIFEST.MF")
        self.Replace_In_File("anchors.xml")
        self.Replace_In_File("ant_generator.xml")
        self.Replace_In_File("plugin.xml")
    
    def Remove_Block(self):
        # ----------------------------------------------Remove Multi Instance Block----------------------------------------------#
        if(self.mTest.MULTI_INSTANCE == "No"):
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"r") as file:
                data = file.read()
                matches = re.findall("(#START_REMOVE_MULTI_INSTANCE#.*?#END_REMOVE_MULTI_INSTANCE#)", data, re.DOTALL | re.MULTILINE)
                for match in matches: 
                    data = data.replace(match, "")
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"w+") as outfile:
                outfile.write(data)
        else:
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"r") as file:
                data = file.read()
                data = data.replace("#START_REMOVE_MULTI_INSTANCE#", "")
                data = data.replace("#END_REMOVE_MULTI_INSTANCE#", "")
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"w+") as outfile:
                outfile.write(data)

        # ----------------------------------------------Remove Ecuc PostBuild Block----------------------------------------------#
        if(self.MODULE.lower() == "ecuc"):
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"r") as file:
                data = file.read()
                data = data.replace("#START_REMOVE_ECUC_POSTBUILD#", "")
                data = data.replace("#END_REMOVE_ECUC_POSTBUILD#", "")
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"w+") as outfile:
                outfile.write(data)
            os.makedirs(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/config', mode=0o777, exist_ok=True)
            shutil.copyfile("Template/config/EcuC.xdm", f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/config/Ecuc.xdm')
        else: 
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"r") as file:
                data = file.read()
                matches = re.findall("(#START_REMOVE_ECUC_POSTBUILD#.*?#END_REMOVE_ECUC_POSTBUILD#)", data, re.DOTALL | re.MULTILINE)
                for match in matches: 
                    data = data.replace(match, "")
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"w+") as outfile:
                outfile.write(data)

        # ----------------------------------------------Remove Resource Support Block----------------------------------------------#
        if(self.MODULE.lower() == "resource"):
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"r") as file:
                data = file.read()
                data = data.replace("#START_REMOVE_RESOURCE_SUPPORT#", "")
                data = data.replace("#END_REMOVE_RESOURCE_SUPPORT#", "")
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"w+") as outfile:
                outfile.write(data)
            os.makedirs(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/config', mode=0o777, exist_ok=True)
            shutil.copyfile("Template/config/Resource.xdm", f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/config/Resource.xdm')
            shutil.copytree("Template/Resource", f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/Resource', dirs_exist_ok=True)
        else: 
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"r") as file:
                data = file.read()
                matches = re.findall("(#START_REMOVE_RESOURCE_SUPPORT#.*?#END_REMOVE_RESOURCE_SUPPORT#)", data, re.DOTALL | re.MULTILINE)
                for match in matches: 
                    data = data.replace(match, "")
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/plugin.xml',"w+") as outfile:
                outfile.write(data)

    def Copy_Template_Code(self):
        if(self.MODULE.lower() != "resource" and self.MODULE.lower() != "ecuc"):
            os.makedirs(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/config', mode=0o777, exist_ok=True)
            shutil.copyfile("Template/config/Module.xdm", f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/config/{self.MODULE}.xdm')
            shutil.copytree("Template/generate_PB", f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/generate_PB')
            shutil.copytree("Template/generate_PC", f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/generate_PC')

            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/config/{self.MODULE}.xdm',"r") as file:
                data = file.read()
                data = data.replace("@MODULE@", self.MODULE)
                data = data.replace("@SILICON_NAME@", self.mTest.SILICON_NAME)
            with open(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/config/{self.MODULE}.xdm',"w+") as outfile:
                outfile.write(data)

    def Start(self):
        self.LetStart()
        if os.path.exists(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}/META-INF/MANIFEST.MF'):
            shutil.rmtree(f'output/{self.MODULE}_{self.mTest.COMPANY_NAME}')
        self.Copy_Module()
        self.Replace_Variable()
        self.Remove_Block()
        self.Copy_Template_Code()
        self.State = "SUCCESSFULLY"  
        self.LetEnd()

if __name__ == "__main__":
    args = Read_Argument()
    logging.info("module = %s", args.module[0])
    RunNew = mRunTool(args.module[0])
    RunNew.Start()