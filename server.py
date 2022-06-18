from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        STOCK_NAME = request.form.get("company")
        COMPANY_NAME = request.form.get("company")

        STOCK_ENDPOINT = "https://www.alphavantage.co/query"
        NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

        STOCK_API_KEY = "XCIGZYIDUPOPC1DL"
        NEWS_API_KEY = "a20f52f2ea3142aa9ba538b7f12fa6b0"

        def get_yesterday_closing_price():
            API_PARAMS = {
                "function": "TIME_SERIES_DAILY",
                "symbol": STOCK_NAME,
                "apikey": STOCK_API_KEY
            }

            response = requests.get(url=STOCK_ENDPOINT, params=API_PARAMS)
            data = response.json()["Time Series (Daily)"]

            stock_prices = [stock for (key, stock) in data.items()]

            return float(stock_prices[0]["4. close"])

        def get_day_before_last_closing_price():
            API_PARAMS = {
                "function": "TIME_SERIES_DAILY",
                "symbol": STOCK_NAME,
                "apikey": STOCK_API_KEY
            }

            response = requests.get(url=STOCK_ENDPOINT, params=API_PARAMS)
            data = response.json()["Time Series (Daily)"]

            stock_prices = [stock for (key, stock) in data.items()]

            return float(stock_prices[1]["4. close"])

        price_difference = abs(get_yesterday_closing_price() - get_day_before_last_closing_price())

        difference_percentage = round((price_difference / get_day_before_last_closing_price()) * 100, 2)

        def get_news():
            API_HEADER = {
                "X-Api-Key": NEWS_API_KEY
            }

            API_PARAMS = {
                "q": STOCK_NAME
            }

            response = requests.get(url=NEWS_ENDPOINT, headers=API_HEADER, params=API_PARAMS)
            data = response.json()["articles"]

            news = (data[0]["title"], data[0]["description"])
            return news

        news = get_news()

        if get_yesterday_closing_price() > get_day_before_last_closing_price():
            message = f"Subject:TSLA 🔺{difference_percentage}%\n\nHeadline: {news[0]}\nBrief: {news[1]}"

        return render_template("stock.html", message=message)

    return render_template("form.html")

app.run()