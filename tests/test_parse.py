from src.parse import parse_detail, parse_listing, rating_to_int

LISTING_HTML = """
<div class="row">
  <article class="product_pod">
    <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in the Attic</a></h3>
    <p class="star-rating Three"></p>
    <p class="price_color">£51.77</p>
    <p class="instock availability">In stock</p>
  </article>
</div>
"""

DETAIL_HTML = """
<ul class="breadcrumb">
  <li><a href="/">Home</a></li>
  <li><a href="/catalogue/category/books/poetry_23/index.html">Books</a></li>
  <li><a href="/catalogue/category/books/poetry_23/index.html">Poetry</a></li>
</ul>
<div id="product_description"><h2>Product Description</h2><p>Это описание книги.</p></div>
<table class="table table-striped">
  <tr><th>UPC</th><td>a897fe39b1053632</td></tr>
  <tr><th>Price (excl. tax)</th><td>£51.77</td></tr>
  <tr><th>Availability</th><td>In stock (22 available)</td></tr>
</table>
"""


def test_rating_to_int():
    assert rating_to_int(["star-rating", "Three"]) == 3
    assert rating_to_int(["star-rating"]) == 0


def test_parse_listing():
    books = parse_listing(LISTING_HTML, "https://books.toscrape.com/")
    assert len(books) == 1
    book = books[0]
    assert book["title"] == "A Light in the Attic"
    assert book["price_raw"] == "£51.77"
    assert book["rating"] == 3
    assert book["url"].endswith("a-light-in-the-attic_1000/index.html")


def test_parse_detail():
    detail = parse_detail(DETAIL_HTML)
    assert detail["category"] == "Poetry"
    assert detail["upc"] == "a897fe39b1053632"
    assert detail["price_excl_tax"] == "£51.77"
