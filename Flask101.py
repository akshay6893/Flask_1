
import pandas as pd
import numpy as np
import json
# FOR DETAILED DESCRIPTION OF THE CODE SEE THE README FILE

class Add_columns():                      # This class adds extra columns to the data table 
                                          # these extra columns will be helpful in parsing data easily
    def __init__(self,data):              # columns are Ids,discount,brand.name,discount_diff
        
        self.data = data
        
        Ids = []
        for mr in range(len(self.data["_id"])):
                Ids.append(self.data["_id"][mr]["$oid"])
        self.data["Ids"] = Ids
        
        ty = []
        basket_price = []
        for x in range(len(self.data["price"])):
            y = self.data["price"][x]["regular_price"]["value"]
            z = self.data["price"][x]["offer_price"]["value"]
            basket_price.append(self.data["price"][x]["basket_price"]["value"])
            ty.append((((y-z)/y)*100))
        self.data["discount"] = ty
        
        
        by = []
        for x in range(len(self.data["brand"])):
            y = self.data["brand"][x]["name"]
            by.append(y)
        self.data["brand.name"] = by
        
        
        comp_list = []
        under_list = []
        discount1 = []
        for ry in range(len(self.data["similar_products"])):
            one_product = self.data["similar_products"][ry]
            compt_ids = [*one_product["website_results"]]
            comp_dict = {}
            product_comp_discount= []
            product_comp_list= []
            undercut = []
            for v in compt_ids:
                comp_basket = one_product["website_results"][f"{v}"]["meta"]["avg_price"]["basket"]
                our_basket = basket_price[ry]

                if comp_basket!=0 :

                    undercut1 = comp_basket-our_basket
                    perc = ((undercut1)/our_basket)*100
                    product_comp_discount.append(perc)
                    product_comp_list.append(v)

            for m,n in zip(range(len(product_comp_list)),range(len(product_comp_discount))):
                comp_dict[product_comp_list[m]]=product_comp_discount[n]


            comp_list.append(comp_dict)   

        self.data["discount_diff"] = comp_list


class Filters(Add_columns):                    # Filter class is a collectiion of all the filter methods
                                               
    def __init__(self,data,f1=None,f2=None,f3=None):
        super().__init__(data)               
        self.f1 = f1                        
        self.f2 = f2
        self.f3 = f3
        
    def discount(self):
    
        discount_list = []
        # returns product ids
        qi = self.f1.index("discount")
        discount_list1 = eval(f"self.data['_id'][self.data['{self.f1[qi]}']{self.f2[qi]}{self.f3[qi]}]")
        for i in range(len(discount_list1)):

            discount_list.append(discount_list1.values[i]['$oid'])

        return discount_list

    
    def undercut(self):                       # This is the filter for expensive_list
        
        te = []
        for xv in range(len(self.data["discount_diff"].values)):
            fg = list(((self.data["discount_diff"].values)[xv].values()))
            for z in fg:
                if z<0 :
                    te.append(xv)
                    break
                    
        discount_list = []
        # returns product ids
        for bv in te:
            discount_list1 = (self.data['Ids'])[bv]
            discount_list.append(discount_list1)
        return discount_list
    
    def brand_name(self):
        brand_list = []
        ui = self.f1.index("brand.name")
        brand_list1 = eval(f"self.data['_id'][self.data['{self.f1[ui]}']{self.f2[ui]}'{self.f3[ui]}']")
        for i in range(len(brand_list1)):
            brand_list.append(brand_list1.values[i]['$oid'])
        return brand_list
        
    def competition(self):
    
        competition_list = []

        ui = self.f1.index("competition")
        for ni in range(len(self.data["discount_diff"])):
            try:
                self.data["discount_diff"][ni][self.f3[ui]]
            except Exception:
                continue

            competition_list1 = self.data["_id"][ni]["$oid"]
            competition_list.append(competition_list1)

        return competition_list
    

    def prod_to_dis(self,list1 = None):             # It's a simple method for converting product list 
                                                    # to corrosponding dicount on that product
        discount_lis = []
        for mr in list1:
            discount_lis.append(self.data["discount"][self.data["Ids"]==mr].values)    
        return discount_lis
    
    def discount_diff(self):           
    
        product_id = []

        ui = self.f1.index("discount_diff")

        for i in range(len(self.data["discount_diff"])):
            
            comp = self.data["discount_diff"][i].values()
            for xv in comp:
                if not eval(f"xv{self.f2[ui]}{self.f3[ui]}"):
                    continue    
                else :
                    product_id.append(self.data["Ids"][i])

        return product_id 



class Queries(Filters):                                # This Class has methods for each Query
    
    def __init__(self,data,f1,f2,f3):
        super().__init__(data,f1,f2,f3)
        
    def discounted_products_list(self):
    
        trio = ["list1","list2","list3","list4"]
        the_trio = []
        
        try:
            list1 = set(self.discount())                                   
        except Exception:
            the_trio.append("list1")    
        
        try:
            list2 = set(self.brand_name())                   
        except Exception:
            the_trio.append("list2")
        
        try:
            list3 = set(self.competition())                   
        except Exception:
            the_trio.append("list3")

        try:
            list4 = set(self.discount_diff())
        except Exception:
            the_trio.append("list4")
        
        present = list(set(trio)^set(the_trio))     

        x = len(present)
        
        if x==4:
            inter2 = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))
            inter1 = inter2&(eval(f"{present[2]}"))
            inter = inter1&(eval(f"{present[3]}"))
        
        if x==3:
            inter1 = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))
            inter = inter1&(eval(f"{present[2]}"))

        if x==2:
            inter = set(eval(f"{present[0]}"))&set(eval(f"{present[1]}"))

        if x==1:
            inter = set(eval(f"{present[0]}"))

        return list(inter)
    
    def products_count_avg(self):
    
        trio = ["list1","list2","list3","list4"]
        the_trio = []
        
        try:
            list1 = set(self.discount()) 
        except Exception:
            the_trio.append("list1")    
        try:
            list2 = set(self.brand_name())
        except Exception:
            the_trio.append("list2")
        try:
            list3 = set(self.competition())
        except Exception:
            the_trio.append("list3")

        try:
            list4 = set(self.discount_diff())
        except Exception:
            the_trio.append("list4")
        
        present = list(set(trio)^set(the_trio))

        x = len(present)
        
        if x==4:
            inter2 = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))
            inter1 = inter2&(eval(f"{present[2]}"))
            inter = inter1&(eval(f"{present[3]}"))
        
        if x==3:
            
            inter1 = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))
            inter = inter1&(eval(f"{present[2]}"))

        if x==2:
            inter = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))

        if x==1:
        
            inter = (eval(f"{present[0]}"))
            
            
        listofarray = (self.prod_to_dis(inter))

        count = len(listofarray)
        avg = ((sum(listofarray))/(count)).tolist()

        return [f"The number of discounts for these filters are {count}",f"The average discount for these filters is {avg}"]
    
    def expensive_list(self):
    
        trio = ["list1","list2","list3","list4"]
        the_trio = []
        try:
            list1 = set(self.discount())
        except Exception:
            the_trio.append("list1")    
        try:
            list2 = set(self.brand_name())
        except Exception:
            the_trio.append("list2")
        try:
            list3 = set(self.competition())
        except Exception:
            the_trio.append("list3")


        list4 = set(self.undercut())

        present = list(set(trio)^set(the_trio))

        x = len(present)

        if x==4:
            inter2 = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))
            inter1 = inter2&(eval(f"{present[2]}"))
            inter = inter1&(eval(f"{present[3]}"))

        if x==3:
            inter1 = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))
            inter = inter1&(eval(f"{present[2]}"))

        if x==2:
            inter = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))

        if x==1:
            inter = (eval(f"{present[0]}"))


        return list(inter) 
    
    
    def competition_discount_diff_list(self):
        
        trio = ["list1","list2","list3","list4"]
        the_trio = []
        try:
            list1 = set(self.discount_diff())
        except Exception:
            the_trio.append("list1")    
        try:
            list2 = set(self.brand_name())
        except Exception:
            the_trio.append("list2")
        try:
            list3 = set(self.competition())
        except Exception:
            the_trio.append("list3")
        
        try:
            list4 = set(self.discount())
        except Exception:
            the_trio.append("list4")

        present = list(set(trio)^set(the_trio))

        x = len(present)

        if x==4:
            inter2 = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))
            inter1 = inter2&(eval(f"{present[2]}"))
            inter = inter1&(eval(f"{present[3]}"))

        if x==3:
            inter1 = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))
            inter = inter1&(eval(f"{present[2]}"))

        if x==2:
            inter = (eval(f"{present[0]}"))&(eval(f"{present[1]}"))

        if x==1:
            inter = (eval(f"{present[0]}"))


        return list(inter)
        


class Input(Queries):               # This class has a method which assigns queries to right query methods
    
    def __init__(self,data,f1,f2,f3,query):
        super().__init__(data,f1,f2,f3)
        self.query = query
        
    def __repr__(self):
         return "Input({},{},{},{},{})".format(self.data,self.f1,self.f2,self.f3,f"{self.query}")
    
    def get_results(self):
        
        if self.query == "discounted_products_list":
            return self.discounted_products_list()
            
        if self.query == "discounted_products_count|avg_discount":
            return self.products_count_avg()
            
        if self.query == "expensive_list":
            return self.expensive_list()
            
        if self.query == "competition_discount_diff_list":
            return self.competition_discount_diff_list()
    
    @classmethod        
    def convert(cls,data_file,q1):                      # It's a class method for transforming inputs.
        
        cls.q1 = q1
        cls.data_file =data_file
        
        df = [json.loads(line) for line in open('netaporter_gb_similar.json', 'r')]
        data=pd.DataFrame(df)
        # data = pd.read_json(cls.data_file,lines=True,orient='columns')     

        query = cls.q1["query_type"]
        if query == "expensive_list":
            try: 
                filters = cls.q1["filters"]
            except Exception:
                f1 = []
                f2 = []
                f3 = []
                return cls(data,f1,f2,f3,f"{query}")
                
        
        else :
            
            filters = cls.q1["filters"]
        
        f1 = []
        f2 = []
        f3 = []
        for xc in range(len(filters)):
            fa = filters[xc]["operand1"]
            fb = filters[xc]["operator"]
            fc = filters[xc]["operand2"]
            f1.append(fa)
            f2.append(fb)
            f3.append(fc)
        
        
        return cls(data,f1,f2,f3,f"{query}")
    
