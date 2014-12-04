##encoding=utf8

from __future__ import print_function
from six import iterkeys, itervalues, iteritems

class DictTree(object):
    @staticmethod
    def initial(key, **kwarg):
        d = dict()
        DictTree.setattr(d, key = key, **kwarg)
        return d
    
    @staticmethod
    def setattr(d, **kwarg):
        if "!!" not in d:
            d["!!"] = dict()
        for k, v in kwarg.items():
            d["!!"][k] = v
    
    @staticmethod
    def add_children(d, key, **kwarg):
        if kwarg:
            d[key] = {"!!": kwarg}
        else:
            d[key] = dict()

    @staticmethod
    def ac(d, key, **kwarg):
        if kwarg:
            d[key] = {"!!": kwarg}
        else:
            d[key] = dict()
            
    @staticmethod
    def k(d):
        return (key for key in iterkeys(d) if key != "!!")

    @staticmethod
    def v(d):
        return (value for key, value in iteritems(d) if key != "!!")

    @staticmethod
    def kv(d):
        return ((key, value) for key, value in iteritems(d) if key != "!!")
    
    @staticmethod
    def k_level1(d, level, counter = 1):
        """level has to be greater equal than 1
        """
        if counter == level:
            for key in DictTree.k(d):
                yield key
        else:
            counter += 1
            for node in DictTree.v(d):
                for key in DictTree.k_level(node, level, counter):
                    yield key

    @staticmethod
    def k_level(d, level, counter = 1):
        """level has to be greater equal than 0
        """
        if level == 0:
            yield d["!!"]["key"]
        else:
            if counter == level:
                for key in DictTree.k(d):
                    yield key
            else:
                counter += 1
                for node in DictTree.v(d):
                    for key in DictTree.k_level(node, level, counter):
                        yield key

    @staticmethod
    def v_level(d, level):
        """level has to be greater equal than 0
        """
        if level == 0:
            yield d
        else:
            for node in DictTree.v(d):
                for node1 in DictTree.v_level(node, level-1):
                    yield node1

    @staticmethod
    def kv_level(d, level, counter = 1):
        """level has to be greater equal than 0
        """
        if level == 0:
            yield d["!!"]["key"], d
        else:
            if counter == level:
                for key, node in DictTree.kv(d):
                    yield key, node
            else:
                counter += 1
                for node in DictTree.v(d):
                    for key, node in DictTree.kv_level(node, level, counter):
                        yield key, node

    @staticmethod   
    def length(d):
        if "!!" in d:
            return len(d) - 1
        else:
            return len(d)
    
    @staticmethod
    def len_on_level(d, level):
        """相对level
        """
        counter = 0
        for node in DictTree.v_level(d, level-1):
            counter += DictTree.length(node)
        return counter
    
    @staticmethod
    def stats_on_level(d, level):
        num_of_emptynode, total = 0, 0
        for key, node in DictTree.kv_level(d, level):
            if DictTree.length(node) == 0:
                num_of_emptynode += 1
            total += 1
        print("On level %s, number of empty node = %s, total node = %s" % (level, 
                                                                           num_of_emptynode, 
                                                                           total))

    @staticmethod
    def del_level(d, level):
        for node in DictTree.v_level(d, level-1):
            for key in [key for key in DictTree.k(node)]:
                del node[key]
                
if __name__ == "__main__":
    try:
        from .js import load_js, dump_js, safe_dump_js, prt_js, js2str
        from .pk import load_pk, dump_pk, safe_dump_pk, obj2str, str2obj
    except:
        from js import load_js, dump_js, safe_dump_js, prt_js, js2str
        from pk import load_pk, dump_pk, safe_dump_pk, obj2str, str2obj
    
    d = DictTree.initial("root")
    DictTree.setattr(d, pop = 299999999)
    DictTree.add_children(d, "VA", name = "virginia", population = 100000)
    DictTree.add_children(d, "MD", name = "maryland", population = 200000)
    
    DictTree.add_children(d["VA"], "arlington", name = "arlington county", population = 5000)
    DictTree.add_children(d["VA"], "vienna", name = "vienna county", population = 1500)
    DictTree.add_children(d["MD"], "bethesta", name = "montgomery country", population = 5800)
    DictTree.add_children(d["MD"], "germentown", name = "fredrick country", population = 1400)
    
    DictTree.add_children(d["VA"]["arlington"], "riverhouse", name = "RiverHouse 1400", population = 437)
    DictTree.add_children(d["VA"]["arlington"], "crystal plaza", name = "Crystal plaza South", population = 681)
    DictTree.add_children(d["VA"]["arlington"], "loft", name = "loft hotel", population = 216)
    
#     prt_js(d)
    
    def test1():
        """test for loop
        """
        print("{:=^100}".format("test for loop behavior"))
        global d
        
        print("\n{:=^60}".format("iter keys, behaive like dict.iterkeys"))
        for k in DictTree.k(d):
            print(k)
            
        print("\n{:=^60}".format("iter values, behaive like dict.itervalues"))
        for v in DictTree.v(d):
            print(v)
            
        print("\n{:=^60}".format("iter key, value pair, behaive like dict.iteritems"))
        for k, v in DictTree.kv(d):
            print(k, v)
            
#     test1()

    def test2():
        """test iter keys or values on specific level
        """
        global d
        
        print("\n{:=^60}".format("iter keys on specific depth level"))
        for key in DictTree.k_level(d, 0):
            print(key)      

        print("\n{:=^60}".format("iter values on specific depth level"))
        for node in DictTree.v_level(d, 0):
            print(node)

        print("\n{:=^60}".format("iter key and values on specific depth level"))
        for key, node in DictTree.kv_level(d, 3):
            print(key, node)

#     test2()

    def test3():
        """test length, and number of node on specific level
        """
        global d
        print(DictTree.length(d))                     # 2
        print(DictTree.length(d["VA"]))               # 2
        print(DictTree.length(d["VA"]["arlington"]))  # 3
        
        print(DictTree.len_on_level(d, 0)) # 0
        print(DictTree.len_on_level(d, 1)) # 2
        print(DictTree.len_on_level(d, 2)) # 4
        print(DictTree.len_on_level(d, 3)) # 3
        print(DictTree.len_on_level(d, 4)) # 0 there's no node depth = 4
        
        print(DictTree.len_on_level(d["VA"], 2)) # 3
        
        DictTree.stats_on_level(d, 0)
        DictTree.stats_on_level(d, 1)
        DictTree.stats_on_level(d, 2)
        DictTree.stats_on_level(d, 3)
        DictTree.stats_on_level(d, 4)
        
        print("VA" in d)
        print("arlington" in d["VA"])
    
    test3()

    def test4():
        """delete behavior, delete the whole level
        """
        global d
        print("{:=^40}".format("before"))
        prt_js(d)
        DictTree.del_level(d, 2)
        print("{:=^40}".format("after"))
        prt_js(d)
        
#     test4()