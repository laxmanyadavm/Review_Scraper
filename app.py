from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/scrap',methods=['POST']) # route with allowed method as POST
def index():
    if request.method == 'POST':
        product = request.form['content'] # obtaining the search string entered in the form
        try:
            url = "https://www.flipkart.com/search?q=" + product.replace(" ", "")
            page = requests.get(url)
            soup = bs(page.content, "html.parser")
            products = soup.find("div", attrs={"class": "_13oc-S"})
            firstProduct = products.find("a")["href"]
            productUrl = "https://www.flipkart.com" + firstProduct
            productPage = requests.get(productUrl)
            reviewsUrl = productUrl.replace("/p/", "/product-reviews/")

            # totalReviewsPages = int(soup3.find("div", attrs={"class": "_2zg3yZ _3KSYCY"}).text[10:-15])
            reviews = []

            for i in range(1, 5):
                try:
                    reviewslink = reviewsUrl + "&page=" + str(i)
                    reviews_page = requests.get(reviewslink)
                    soup3 = bs(reviews_page.content, "html.parser")
                    Bigbox = soup3.find('div', attrs={"class": "_1YokD2 _3Mn1Gg col-9-12"})
                    reviewBoxes = Bigbox.find_all("div", attrs={"class": "_1AtVbE col-12-12"})[2:-1]
                    productName = Bigbox.find("div", attrs={"class": "_1AtVbE col-10-12"}).text[:-7]

                    for review_box in reviewBoxes:

                        try:
                            Name = review_box.find('div', attrs={"class": "row _3n8db9"}).p.text
                        except:
                            Name = "No Name"
                        try:
                            Rating = review_box.find("div", attrs={"class": "row"}).div.div.div.text
                        except:
                            Rating = "-"
                        try:
                            Tagline = review_box.find("p", attrs={"class": "_2-N8zT"}).text
                        except:
                            Tagline = "No Tagline"
                        try:
                            Reviews = review_box.find("div", attrs={"class": ""}).text.replace("READ MORE", "")
                        except:
                            Reviews = "No review"

                        mydict = {"Product": productName, "Name": Name, "Rating": Rating, "Tagline": Tagline,
                                  "Reviews": Reviews}

                        reviews.append(mydict)
                except:
                    break

            return render_template('results.html', reviews=reviews)  # showing the review to the user
        except:
            return 'something is wrong'


if __name__ == "__main__":
    app.run(port=8000,debug=True) # runni m  ng the app on the local machine on port 8000