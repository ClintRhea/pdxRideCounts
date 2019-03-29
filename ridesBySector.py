import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

filename = 'daily_estimates.csv'

daily_estimates = pd.read_csv(filename, header=1, na_values='-')

last_decade_columns = ['Sector', 'Site #', 'Location', '2018', '2017', '2016', '2015',
                       '2014', '2013', '2012', '2011', '2010', '2009', '2008']

last_decade_estimates = daily_estimates[last_decade_columns]

melted = pd.melt(last_decade_estimates, id_vars=[
                 'Sector', 'Site #', 'Location'], value_name='rides', var_name='year')

melted.rides = pd.to_numeric(melted.rides, errors='coerce')
melted.Sector = melted.Sector.astype('category')
melted.year = pd.to_datetime(melted.year)

melted.head()

melted_group = melted.groupby(['Sector', 'year']).rides.sum()

df = pd.DataFrame(melted_group).reset_index()

plt.style.use('seaborn-darkgrid')
palette = plt.get_cmap('Dark2')

RIDE_MAX = 17000

num = 0
for sector in df['Sector'].unique():
    num += 1

    plt.subplot(3, 3, num)

    sector_df = df[df['Sector'] == sector]

    plt.plot(sector_df['year'], sector_df['rides'], label=sector,
             color=palette(num), alpha=0.9, linewidth=1.9)

    plt.ylim(0, RIDE_MAX)

    if num in range(6):
        plt.tick_params(labelbottom='off')
    if num not in [1, 4, 7]:
        plt.tick_params(labelleft='off')

    plt.xticks(rotation=75)

    plt.yticks(np.arange(0, RIDE_MAX, step=5000))

    plt.title(sector, loc='left', fontsize=12,
              fontweight=0, color=palette(num))

plt.suptitle("Portland, Oregon manual 2-hour bike counts",
             fontsize=13, fontweight=0, color='black')

plt.gcf().text(0.03, 0.5, 'Daily Estimate',
               ha='center', va='center', rotation='vertical')

plt.show()
