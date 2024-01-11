#main.py

from twisted.internet import reactor, defer
from nd_fishing_2023.nd_fishing_2023.spiders.nd_fishing_2023_spider import NDFishingSpider
from nd_fishing_2023.nd_fishing_2023 import pipelines as nd_fishing_pipeline
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os
import pandas as pd
#from excel_utils import create_title, export_workbook
from scrapy.utils.log import configure_logging


PROJECT_ROOT =  os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)



lake_results = ["https://gfappspublic.nd.gov/wheretofish/Results.aspx"]

def main():

    configure_logging(
        {"LOG_LEVEL":"INFO"}
    )

    settings_file_path = 'nd_fishing_2023.nd_fishing_2023.settings'   #Relative Location of Settings File
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE',settings_file_path)
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks #type: ignore
    def crawl():
        for results in lake_results:  #loop through the list of available standard reports
                 
            yield runner.crawl(NDFishingSpider,lake_results= results)
            #add more spiders here
        
            comp_df = pd.DataFrame()
            for item in nd_fishing_pipeline.items:
                print("Main Item: ",item)
                df = pd.DataFrame.from_dict(item)
                #df = df.drop(index = (len(df)-1)) #remove last row from table
                #if nd_fishing_pipeline.items.index(item) != 0 : #if not the first iteration, drop the column headers
                #    df = df.drop(index = [0,1])
                #comp_df = pd.concat([comp_df,df])
            nd_fishing_pipeline.items.clear()
        
            #title = create_title(report) #create a Spreadsheet title from site address
            #export_workbook(title,comp_df)# take dataframe and turn it into a formatted Excel Workbook

        reactor.stop() # type: ignore
        
    crawl()
     
    reactor.run() # type: ignore

 #this only runs if the module was *not* imported
if __name__ == "__main__":
    main()
    