# Example Project Using LinearSpider

标签（空格分隔）： 未分类

----------

Let's learn this framework with an easy example project

##**CVS store information crawler**


----------


###**Come up with a plan**

Suppose you want all CVS store data over US. We can find a [webpage][1] on CVS websites. So there's list of state in US, each states has a list of cities, each city has a list of CVS store, and each of CSV store has a link. In this link, you can see **address**, **phone number**, **services**, **office hour**. You can view a CSV store example [here][2].

So now we got this idea:

> Take the webpage has US state list as entrance
Then we travel through all city, all store
Finally visit the store webpage to extract the information we need.

----------
###**Understand the framework**

In the CVS example, the path from the entrance to the target data like a pyramid, which has couple of layers.

- level0 is the entrance
- level1 is state page (which has list of city)
- level2 is city page (which has list of store)
- level3 is store page (which has the data we need)

So basically we crawl from level1 to level3. But the strategy is that, go to the next level until you finished the current level. You may noticed that, in this three level, we are actually just extracting link and building a tree structure. After this we finally start do the "real" crawling.

Basically, working with LinearSpider framework, the only thing need you to define is:

> - link extractor to get all link at level1, level2, level3
- extractor to get target data from url at level3
- LinearSpider will take care of everything else. :)

----------

###**Start crawling**

Let's go back to the [entrance][1]. First let's take a look at this page. 


    <div class="states">
    	<ul>						
    		<li>
    		<a href="/stores/cvs-pharmacy-locations/Alabama">
    			Alabama
    		</a>
    		</li>						
    
    		<li style="line-height:20px">Alaska<span>(currently no CVS/pharmacy stores)</span></li>
    
    		<li>
    		<a href="/stores/cvs-pharmacy-locations/Arizona">
    			Arizona
    		</a>
    		</li>
    		...... there's a lot
    	</ul>
    	<br class="clear">
    </div>

This is the html code has the state link we need. So basically, we
find the "div" element by it's class, and find all "a" element in "div". The body text is the state name, and the "href" attribute of "a" is the link.
(complete link is http://www.cvs.com/stores/cvs-pharmacy-locations/Alabama)

There's many option you can use for extracting text from html. Here we recommend [BeautifulSoup][3], but you can also try [lxml][4], Xpath syntax.


  [1]: http://www.cvs.com/stores/cvs-pharmacy-locations
  [2]: http://www.cvs.com/stores/cvs-pharmacy-address/520+Highway+119-Alabaster-AL-35007/storeid=4867
  [3]: http://www.crummy.com/software/BeautifulSoup/
  [4]: http://lxml.de/