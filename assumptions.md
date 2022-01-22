## ✨ Assumptions

Requirements were clear about the pages to fetch, and the information to gather.

> ### Data:
>* The most challenging piece of data to scrape were the measurements (width and height), so my assumption was that those data points would come presented as ¨width x height cm¨ which I extracted directly on the xpath.
>
>
> * I just took the first set of width and height because the requirements specified only one datapoint for each.
>
>
> * For images, I retrieved the respective url.
>
>### Scrape Flow:
>* First off I specified both requested categories as start_urls. That´s one thing I let slide on my previous try, on that occasion I scraped all categories.
>
>
> * The spider first looks for artworks on each page, since even ¨larger¨ category pages have artworks.
>
>
> * Then it looks for pagination, another step I let slide the last time.
>
>
> * And last it looks for subcategories within the current category.
>
> ### Code
> * I separated the locators from the actual code in a SimpleNamespace, so they would be easier to change without 
> going through all the file.
> 
> 
> * The clean_artist method under items.py is not a generator expression for better readability.
> 
> 
> * Used pre-commit for linting and formatting.
> 
> 