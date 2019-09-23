from flask import Flask, render_template
from datasets.daily_kos import DailyKos
from datasets import DistrictType
from datasets.asthma import Asthma
from datasets.polling import Polling
from datasets.voting import Voting
import jinja2

app = Flask(__name__)
dk = DailyKos()
dk.join_with_dataset(Asthma())
dk.join_with_dataset(Polling())
dk.join_with_dataset(Voting())

from xhtml2pdf import pisa
# from django.template.loader import get_template
# from django.template import Context
# template = get_template("templates/index.html")
# context = Context({'pagesize':'A4'})

html = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates/')
).get_template('index.html').render(district=dk.states['VA'].state_sentate_districts['5'],
                                    DistrictType=DistrictType)
with open('VA5.pdf', "w+b") as outfile:
    pisa.CreatePDF(html, dest=outfile)
    # pdf = pisa.pisaDocument(StringIO.StringIO(html), dest=result)

@app.route('/')
def home():
    return

# if __name__ == '__main__':
#     app.run(debug=True)
