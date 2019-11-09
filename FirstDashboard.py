from flask import Flask, render_template, request
import plotly
import plotly.graph_objs as go
# import datetime
# from calendar import monthrange
import pandas as pd
import numpy as np
import json

app = Flask(__name__)

# declaration of constants
LIST_OF_ISLANDS = ['Oahu', 'Hawaii Island', 'Maui', 'Sample']
LIST_OF_OAHU_SITES = ['Dole Plantation','Ko\'olau Center', 'Kapolei Commons', 'Hawai\'i Kai 7-Eleven', 'Ward 1', 'Ward 2', 'Wai\'anae Mall', '801 Dilingham'] 
LIST_OF_HAWAII_ISLAND_SITES = ['HELCO Hilo', 'HELCO Kona', 'Waimea KTA', 'The Shops at Mauna Lani']
LIST_OF_MAUI_SITES = ['MECO Kahului', 'Kaunakakai']
LIST_OF_SAMPLE_SITES = ['SiteA', 'SiteB']
LIST_OF_DURATIONS = ['Yearly', 'Monthly', 'Weekly', 'Daily', 'Hourly', 'Sample']


class Site:
    def __init__(self, siteName):
        self.siteName = siteName

    def printSiteName(self):
        print('Analyzing site: ' + self.siteName)

    def gatherPowerData(self):
        # open file containing power data for site
        self.powerDataFrame = pd.read_excel(self.siteName + ' power.xlsx', sheet_name='Power Data')

    def gatherTransactions(self):
        # open csv file containing transactions
        allData = pd.read_csv("Data_HACC.csv") 
        
        # if-else: For sample data purposes only. For real data, use only 'else' condition
        if self.siteName == 'SiteA':  
            self.transactions = allData[allData['Charge Station Name'] == 'A']
        elif self.siteName == 'SiteB':
            self.transactions = allData[allData['Charge Station Name'] == 'B']
        else:
            self.transactions = allData[allData['Charge Station Name'] == self.siteName]


def main():

    # For testing purposes:
    site = Site('SiteA')
    #site = Site(chooseSite())
    print('')
    site.printSiteName()

    # Gather power data from site
    site.gatherPowerData()
    print('Gathering Power Data...')
    print(site.powerDataFrame)

    # Gather transactions from site
    site.gatherTransactions()
    print('\nGathering Transactions...')
    print(site.transactions)

    #graphDuration = chooseDurationForGraph()
    #print(graphDuration)
    #createPowerTimeGraph(site.powerDataFrame, graphDuration)
    createPowerTimeGraph(site.powerDataFrame)


def chooseSite():

    # Choose which site to analyze data from
    print('Choose an island from list below:')
    for island in LIST_OF_ISLANDS:
        print('[' + str(LIST_OF_ISLANDS.index(island)) + '] ' + island)
    islandInput = int(input("Island Choice (index): "))

    print('Choose a site from list below:')
    if (islandInput == 0):
        for site in LIST_OF_OAHU_SITES:
            print('[' + str(LIST_OF_OAHU_SITES.index(site)) + '] ' + site)
        siteName = LIST_OF_OAHU_SITES[int(input("Site Choice (index): "))]
    elif (islandInput == 1):
        for site in LIST_OF_HAWAII_ISLAND_SITES:
            print('[' + str(LIST_OF_HAWAII_ISLAND_SITES.index(site)) + '] ' + site)
        siteName = LIST_OF_HAWAII_ISLAND_SITES[int(input("Site Choice (index): "))]
    elif (islandInput == 2):
        for site in LIST_OF_MAUI_SITES:
            print('[' + str(LIST_OF_MAUI_SITES.index(site)) + '] ' + site)
        siteName = LIST_OF_MAUI_SITES[int(input("Site Choice (index): "))]
    elif (islandInput == 3):
        for site in LIST_OF_SAMPLE_SITES:
            print('[' + str(LIST_OF_SAMPLE_SITES.index(site)) + '] ' + site)
        siteName = LIST_OF_SAMPLE_SITES[int(input("Site Choice (index): "))]

    return siteName


@app.route('/')
def index():
    feature = 'Bar'
    bar = create_plot(feature)
    return render_template('testbootstrap.html', plot=bar)

# @app.route('/')
# def index():
#     feature = 'Bar'
#     bar = create_plot(feature)
#     return render_template('page.html', plot=bar)


def create_plot(feature):
    if feature == 'Bar':
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({'x': x, 'y': y})  # creating a sample dataframe
        data = [
            go.Bar(
                x=df['x'],  # assign x as the dataframe column 'x'
                y=df['y']
            )
        ]
    else:
        N = 1000
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x=random_x,
            y=random_y,
            mode='markers'
        )]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


@app.route('/bar', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']
    graphJSON = create_plot(feature)

    return graphJSON


if __name__ == '__main__':
    app.run()


def createPowerTimeGraph(data):

    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=list(data['Start Date and Time']), y =list(data['Power (kW)']))
    )

    # Title of graph
    fig.update_layout(
        title_text = 'Power vs. Time'
    )

    # Add range selector and slider
    fig. update_layout(
        xaxis = go.layout.XAxis(
            rangeselector = dict(
                buttons = list([
                    dict(count = 1,
                         label = 'YTD',
                         step = 'year',
                         stepmode = 'todate'),
                    dict(count = 1,
                         label = 'Yearly',
                         step = 'year',
                         stepmode = 'backward'),
                    dict(count = 6,
                         label = '6 Months',
                         step = 'month',
                         stepmode = 'backward'),
                    dict(count = 1,
                         label = 'Monthly',
                         step = 'month',
                         stepmode = 'backward'),
                    dict(count = 7,
                         label = 'Weekly',
                         step = 'day',
                         stepmode = 'backward'),
                    dict(count = 1,
                         label = 'Daily',
                         step = 'day',
                         stepmode = 'backward'),
                    dict(count = 1,
                         label = 'Hourly',
                         step = 'hour',
                         stepmode = 'backward'),
                    dict(count = 30,
                         label = '30 Minutes',
                         step = 'minute',
                         stepmode = 'backward'),
                    dict(step = 'all')
                ])
            ),
            rangeslider = dict(
                visible = True
            ),
            type = 'date'
        )
    )

    fig.show()

def createGraph():
    return

main()