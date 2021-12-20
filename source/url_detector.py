import json
from selenium_driver  import SeleniumDriver

#ignore warning
import sys
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")


################################################################################################
##################### DOCKERHUB CONTAINER PLATFORM ############################################
################################################################################################
class DockerHub(SeleniumDriver):

    def __init__(self, url):
        SeleniumDriver.__init__(self)
        self.url = url

    def get_base_os(self, url):
        """
        Args:
        
        Returns: 
            List of base OS containers or None if no base OS if found

        """
        self.open_driver(url)
        container_elems = self.find_element_by_class_name()
        
        if container_elems == None:
            return  "NA"
        else:

            container_elements = container_elems.find_elements_by_tag_name("a")
            containers = {}
            containers["Official image"] = []
            containers["Verified Publisher"] = []

            for cont in container_elements:

                if cont.get_attribute("data-testid") == "imageSearchResult": 
                    if len(containers) < 5:
                       
                        if "Official" in cont.text : containers["Official image"].append(cont.get_attribute("href"))
                        else: containers["Verified Publisher"].append(cont.get_attribute("href"))

                    else: break
            return  containers

    def search_base_os(self,entity:str) -> str:
        """
        Args:
            entity: 
        Returns:
            dict: a dictionary containing windows and linux based OS
        """
        base_os = {}
        search_url = "https://hub.docker.com/search?q="+entity+"&type=image"

        #Filter for official product and verified publisher
        filter = "&image_filter=store%2Cofficial" 
    
        windows_base_images =   search_url+filter+'&operating_system=windows'
        linux_base_images   =   search_url+filter+'&operating_system=linux'


        self.url = windows_base_images
        base_os["Windows base os"] =  self.get_base_os(self.url)

        self.url = linux_base_images
        base_os["linux base os"] =  self.get_base_os(self.url)

        self.close_driver()
        return base_os

    def save_search_results(self,search_results):

        with open("base_os.json", "w", encoding = 'utf-8') as base_os_file:
            base_os_file.write(json.dumps(search_results, indent= 4))


    def search_result(self,entities):

        search_results = {}
        for _  ,   image in  entities.items():  
            search_results[image] = self.search_base_os(image)
        return search_results


#####################################################################################################
#################### REDHAT OPERATOR PLATFORM ######################################################
#####################################################################################################
class OpenShiftOperator(SeleniumDriver):

    def __init__(self, url) -> None:
        SeleniumDriver.__init__(self)
        self.home_url = url

    
    def get_operator(self, search_url):
        
        self.open_driver(search_url)
        
        #check if web content is empty
        body = self.search_body(empty_body_element_class_name="oh-hub-page__content")

        if "No Results Match the Filter Criteria" in body : print("No Results Match the Filter Criteria")
        else: 
            selector = ".catalog-tile-view-pf"
            elems = self.find_element_by_css_selector(selector)
            operator_elements = elems.find_elements_by_tag_name("a")
            for operator in operator_elements:
                print(operator.get_attribute("href"))

    def search_operator(self, entity):

        home_url ="https://operatorhub.io/"
        search_url = home_url+ "?keyword=" + entity
        self.get_operator(search_url)


####################################################################################################
##################       OPENSHIFT CONTAINER PLATFORM   ###########################################
####################################################################################################
class Openshift(SeleniumDriver):


    def __init__(self, url):
        SeleniumDriver.__init__(self)
        self.home_url = url

    def get_containers(self, search_url):
        
        self.open_driver(search_url)

        search_body = self.search_body()

        #Check if web content is empty
        if search_body != '': 
            print(search_body)
            return  search_body
        else:

            #num_page = self.get_number_of_pages()

            selector = "#nr-search-all"
            container_elems = self.find_element_by_css_selector(selector)

            if container_elems != None:
                container_elements = container_elems.find_elements_by_tag_name("a")
                for cont in container_elements:
                    print(cont.get_attribute("href"))
            else: 
                print("No search elements found")


    def get_number_of_pages(self):

        selector_class = ".pf-c-pagination__nav-page-select > input:nth-child(1)"
        num_pages_element = self.find_element_by_css_selector(selector_class)
        if num_pages_element == None : return 0
        else: return num_pages_element.get_attribute("max")


    def search_redhat_containers(self,container_name):
        """
        
        """
        provider = "Red Hat" # Only select images from RED HAT amongt other providers 
        base_url = "https://catalog.redhat.com/software/containers/search?q="+container_name+"&p=1"
        search_url = base_url+"&vendor_name=" + provider

        self.get_containers(search_url)   


if __name__ == "__main__":

    #Sample single input data
    sample_entity_name = "tomcat"
    input_data = {"entity name": sample_entity_name}   


    doc = DockerHub("https://hub.docker.com/")
    print("DOCKERHUB CONTAINER IMAGES\n")
    print(doc.search_result(input_data))


    print("OPENSHIFT CONTAINER IMAGES\n")
    openshift_instance = Openshift("https://catalog.redhat.com/software/containers/search")
    openshift_instance.search_redhat_containers(input_data["entity name"])


    print("OPERATORS\n")
    opr = OpenShiftOperator("https://operatorhub.io/")
    opr.search_operator(input_data["entity name"])








    
    
        


    