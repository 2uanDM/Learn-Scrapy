"""
body = response.css(".item-cells-wrap.border-cells.items-grid-view.four-cells.expulsion-one-cell")

items = body.css(".item-container")

item = items[0]

# href to item
href = item.css("a::attr(href)").get()

"""