import pandas as pd
import matplotlib.pyplot as plt

#Ecologie delfland
data_2024 = pd.read_excel("..\Ecologie_tot_2024.xlsx")
# data_macrofyten_aanvullend_richness = pd.read_excel("..\Macrofyten_Hackathon_update25_06.xlsx", sheet_name = "Macrofyten_Richness")
# data_macrofyten_aanvullend_EKR = pd.read_excel("..\Macrofyten_Hackathon_update25_06.xlsx", sheet_name = "Macrofyten_EKR")
data_macrofyten_aanvullend_Chemie = pd.read_excel("..\Macrofyten_Hackathon_update25_06.xlsx", sheet_name = "Chemie_meetgegevens")
data_macrofyten_aanvullend_Meetpunt = pd.read_excel("..\Macrofyten_Hackathon_update25_06.xlsx", sheet_name = "Meetpunt_informatie")
# data_macrofyten_aanvullend_Weer = pd.read_excel("..\Macrofyten_Hackathon_update25_06.xlsx", sheet_name = "Weer_historie")

data_macrofyten_aanvullend_Chemie['datum'] = pd.to_datetime(dict(year=data_macrofyten_aanvullend_Chemie['Jaar'], month = data_macrofyten_aanvullend_Chemie['Maand'], day=1)) + pd.offsets.MonthEnd(0)
data_macrofyten_aanvullend_Chemie = data_macrofyten_aanvullend_Chemie.sort_values(by='datum')
parameters = ['Ptot', 'Ntot', 'pH', 'Temp_water', 'Doorzicht']
eenheden = ['mg/l', 'mg/l', '-', '$^\circ$ C', 'm']
ymin = [0, 0, 6, 0, 0]
ymax = [2, 15, 10, 30, 2.5]

#plot data in time
for meetpunt in data_macrofyten_aanvullend_Meetpunt['MeetObject']:

    fig, axes = plt.subplots(nrows = len(parameters), ncols = 1, sharex = True, sharey = False, figsize = (15, 15))
    axes_flattened = axes.flatten()

    df_sub = data_macrofyten_aanvullend_Chemie[data_macrofyten_aanvullend_Chemie['MeetObject']==meetpunt]

    for i, axis in enumerate(axes_flattened):
        if not parameters[i] in df_sub.columns:
            continue
        else:
            axis.plot(df_sub['datum'], df_sub[parameters[i]], linestyle = '--', marker = 'o')
            axis.set_ylabel(parameters[i] + ' [' + eenheden[i] + ']')
            axis.set_ylim(ymin[i], ymax[i])

    plt.close(fig)

    save_dir = "..\Python_folder\Plots"
    fig.savefig(save_dir + '/' + meetpunt + '.jpg')

##plot in space
#add coordinates to dataframe
chemie_merged = pd.merge(data_macrofyten_aanvullend_Chemie, data_macrofyten_aanvullend_Meetpunt, om = 'MeetObject', how = 'left')
chemie_average = data_macrofyten_aanvullend_Chemie.groupby(['MeetObject', 'Jaar']).mean()