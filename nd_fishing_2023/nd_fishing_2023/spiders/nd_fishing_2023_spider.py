import scrapy
from scrapy import FormRequest,Request
import pandas as pd
import numpy as np
import io
import logging
from scrapy.shell import inspect_response



class NDFishingSpider(scrapy.Spider):
    name = "nd_fishing_2023"
    allowed_domains = ["gfappspublic.nd.gov"]
    
    def __init__(self, lake_results="", *args, **kwargs):
        super(NDFishingSpider,self).__init__(*args,**kwargs)
        #self.stryear = year
        self.url = lake_results
        logging.getLogger('scrapy').setLevel(logging.WARNING)

    def start_requests(self):
        yield Request(self.url,self.parse)
        print("Fishing Spider Start Requests\n")
        print(self.url,"\n")

    custom_settings = {}


    def parse(self, response):
        print("Fishing Spider Parse\n")
        for lakes in response.xpath('//*[@id="dvResultsList"]').getall():
            print("XPath Response: ",lakes)
            yield lakes.to_dict
            #Request(self.url,self.tab2)
        

    
    # def datacapture(self,response):
    #     iostring = io.StringIO(response.text)
    #     dfs = pd.read_html(iostring)
    #     #Re-arrange Code-and-class table such that it is in 2 columns
    #     df1 = dfs[2]
    #     df2 = df1[[2,3]].copy()
    #     df2.columns = ['Attribute','Value']
    #     df1 = df1.drop(df1.columns[[2,3]],axis = 1)
    #     df1.columns = ['Attribute','Value']
    #     frame = [df1,df2]
    #     candc = pd.concat(frame)
    #     #pull only current year data from table
    #     df3 = dfs[3]
    #     df3.drop(df3.columns[[2,3,4,5]],axis=1,inplace = True)
    #     df3.rename(columns={df3.columns[0]:'Attribute'},inplace = True)
    #     df3.rename(columns={df3.columns[1]:'Value'},inplace = True)
    #     result = [candc,df3]
    #     out = pd.concat(result) # this is stitched frame, containing all current year data
    #     out = out.T #transpose so it is a single row of relevant data
    #     print("\nOutput Dataframe: ",out)
    #     length = len(out.index)
    #     yrdata = np.full((length),self.stryear)

    #     #add a column to the dataframe indicating which year the data is from
    #     yrdata[0] = "Year"
    #     out.insert(1,"",yrdata) #add year # to column 1
    #     #print("\nOutput Dataframe: ",out)
    #     rawschool = response.xpath("//html/body/form/div[2]/div[2]/h2/text()").get()
    #     district, sep, tail = rawschool.partition(')')
    #     name, sep, id = district.partition('(')
    #     #create arrays full of the district name and ID
    #     namedata = np.full((length),name)
    #     iddata = np.full((length),id)
    #     out.insert(0,"ID",iddata)
    #     out.insert(0,"Name",namedata)
    #     yield out.to_dict()

    def tab2(self,response):
        print ("\nTab2:", response)
        inspect_response(response,self)