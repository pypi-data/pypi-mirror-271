import json
import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

import config
from synch2jira.issue_csv import IssueCSV
from synch2jira.issue_json import IssueJSON

matplotlib.use('Agg')


def generate_issue_data_mining_csv(state1=config.workflow_status1, state2=config.workflow_status2):
    with open(config.json_issues_file, 'r') as file:
        json_data = json.load(file)
    issue_list = [IssueJSON.json_to_issue(issue_data, json_data, state1, state2) for issue_data in
                  json_data]
    IssueCSV.generate_csv_data(issue_list, config.csv_issue_file)


def csv_to_dataframe(file_path):
    df = pd.read_csv(file_path)
    return df


def str_df_to_dt_df(dataframe, use_workflow=config.use_workflow):
    if use_workflow:
        dataframe['created'] = pd.to_datetime(dataframe['workflow_start_time'], utc=True)
        dataframe['resolutiondate'] = pd.to_datetime(dataframe['workflow_end_time'], utc=True)
        dataframe = dataframe.dropna(subset=['workflow_start_time', 'workflow_end_time'])
        return dataframe
    dataframe['created'] = pd.to_datetime(dataframe['created'], utc=True)
    dataframe['resolutiondate'] = pd.to_datetime(dataframe['resolutiondate'], utc=True)
    dataframe = dataframe.dropna(subset=['resolutiondate', 'created'])
    return dataframe


def genarate_creation_resolution_figure(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe.sort_values(by='created', inplace=True)

    plt.figure(figsize=(12, 6))
    plt.scatter(dataframe.index, dataframe['created'], label='Date de création', color='blue')
    plt.scatter(dataframe.index, dataframe['resolutiondate'], label='Date de résolution', color='green')
    plt.xlabel('ticket')
    plt.ylabel('dates creation_resolution')
    plt.title('Tendances creation_resolution des tickets ')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(config.image_directory + 'creation_resolution_by_issue_type.png')
    plt.show()


def genarate_creation_resolution_figure_by_issue_field(dataframe, field):
    dataframe = str_df_to_dt_df(dataframe)

    dataframe.sort_values(by='created', inplace=True)

    types_issues = dataframe[field].unique()

    fig, axes = plt.subplots(nrows=len(types_issues), ncols=1, figsize=(12, 6 * len(types_issues)))

    for i, issue_type in enumerate(types_issues):
        data_filtered = dataframe[dataframe[field] == issue_type]

        axes[i].scatter(data_filtered.index, data_filtered['created'], label='Date de création', color='blue')

        axes[i].scatter(data_filtered.index, data_filtered['resolutiondate'], label='Date de résolution', color='green')

        axes[i].set_xlabel('ticket')
        axes[i].set_ylabel('dates creation_resolution')
        axes[i].set_title(f'Tendances creation_resolution des tickets ({issue_type})')
        axes[i].legend()
        axes[i].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(config.image_directory + f'/creation_resolution_by_issue_{field}.png')
    plt.show()


def get_creation_resolution_time_statistics(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['creation_resolution_time'] = dataframe.apply(lambda row: row['resolutiondate'] - row['created'], axis=1)
    # Différence de temps moyenne entre création et résolution
    average_resolution_time = dataframe['creation_resolution_time'].mean()
    return dataframe['creation_resolution_time'].describe()


def get_month_statistics(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['created_month'] = dataframe['created'].dt.month
    dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']  #
    dataframe = dataframe[['created_month', 'resolution_time']]
    statistics_by_month = dataframe.groupby('created_month')['resolution_time'].describe()
    return statistics_by_month


def get_period_statistics(dataframe, period):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['period'] = get_data_by_period(dataframe, period)
    dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']
    dataframe = dataframe[['period', 'resolution_time']]
    statistics_by_period = dataframe.groupby('period')['resolution_time'].describe()
    return statistics_by_period


# def get_statistics_by_issue_type(dataframe):
#     dataframe = str_df_to_dt_df(dataframe)
#     dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']
#     statistics_by_issue_type = dataframe.groupby('issuetypename')['resolution_time'].describe()
#
#     return statistics_by_issue_type


def get_statistics_by_field(dataframe, field):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']
    statistics_by_issue_field = dataframe.groupby(field)['resolution_time'].describe()
    return statistics_by_issue_field


def get_double_group_by_statistics(dataframe, period):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['resolution_time'] = dataframe['resolutiondate'] - dataframe['created']
    dataframe['period'] = get_data_by_period(dataframe, period)

    statistics = dataframe.groupby(['period', "issuetypename"])['resolution_time'].describe()
    return statistics


def get_data_by_period(dataframe, period):
    if period == 'week':
        return dataframe['created'].dt.isocalendar().week
    elif period == 'month':
        return dataframe['created'].dt.month
    elif period == 'year':
        return dataframe['created'].dt.year
    else:
        raise ValueError("Période non valide. Veuillez spécifier 'day', 'month' ou 'year'.")


def get_number_issues_solved_within_preriod_graph(dataframe, period):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['resolution_time_days'] = (dataframe['resolutiondate'] - dataframe['created']).dt.days
    print(dataframe['resolution_time_days'].describe())
    # 3. Identify and visualize the proportion of issues resolved within 30 days
    dataframe['resolved_within'] = dataframe['resolution_time_days'] <= period

    resolution_proportion = dataframe['resolved_within'].value_counts(normalize=True) * 100
    plt.figure(figsize=(6, 6))
    resolution_proportion.plot(kind='pie', autopct='%1.1f%%', startangle=140,
                               labels=[f'en plus de  {period} jour', f'en moins de  {period} jour'],
                               colors=['lightgreen', 'lightcoral'])
    plt.ylabel('')
    plt.title(f'Proportion des tickets resolu en  {period} jour')
    plt.tight_layout()
    plt.savefig(config.image_directory + f'issues_resolved_within_{period}_days.png')
    plt.show()


#################################
def tickets_status_data(status, dataframe, date_min, date_max, pas_de_temps):
    date_resolution = dataframe[status]
    dataframe_intervalles = dataframe[
        (date_resolution.dt.year >= date_min.date().year) & (date_resolution.dt.year <= date_max.date().year)]
    return dataframe_intervalles.groupby(
        getattr(dataframe_intervalles[status].dt, pas_de_temps)).size()


def tickets_status_par_intervalles_de_temps(status, dataframe, date_min, date_max, pas_de_temps):
    dataframe = str_df_to_dt_df(dataframe)
    date_min = pd.Timestamp(date_min)
    date_max = pd.Timestamp(date_max)
    type_ticket = "créés" if status == 'created' else "cloturés"

    tickets_clotures_par_date = tickets_status_data(status, dataframe, date_min, date_max, pas_de_temps)
    if pas_de_temps == 'dayofweek':
        return plot_and_save(tickets_clotures_par_date, 'Jour',
                             f'Nombre de tickets {type_ticket}',
                             f'Nombre de tickets {type_ticket} du {date_min.date()} '
                             f'au {date_max.date()} par jour', "line", 'jour')
    else:
        return plot_and_save(tickets_clotures_par_date, 'Année',
                             f'Nombre de tickets {type_ticket}',
                             f'Nombre de tickets {type_ticket} du {date_min.date()} '
                             f'au {date_max.date()} ', 'points', '')


def tickets_status_par_intervalles_de_temps_version_yaml(dataframe):
    file_data = read_config()['tickets_status_par_intervalles_de_temps_par_mois']
    dataframe = str_df_to_dt_df(dataframe)
    for label in file_data:
        date_min = pd.Timestamp(label['date_min'])
        date_max = pd.Timestamp(label['date_max'])

        tickets_clotures_par_date = tickets_status_data(label['status'], dataframe, date_min, date_max,
                                                        label['pas_de_temps'])
        xticks_type = label['xtitre'] if label['xtitre'] == 'jour' else ''
        plot_and_save(tickets_clotures_par_date, label['xtitre'], label['ytitre'],
                      f"{label['titre_graphe']} du {date_min.date()} au {date_max.date()}"
                      , label['type_graphe'], xticks_type)


def tickets_status_par_mois_par_intervalle(dataframe, date_min, date_max, status='resolutiondate'):
    dataframe = str_df_to_dt_df(dataframe)
    mask = (dataframe[status] >= date_min) & (dataframe[status] <= date_max)
    annees = dataframe.loc[mask, status].dt.year.unique()
    plt.figure(figsize=(10, 6))
    type_ticket = "créés" if status == 'created' else "cloturés"
    values_exist = False
    for annee in annees:
        dataframe_annee = dataframe[dataframe[status].dt.year == annee]
        tickets_clotures_par_mois = dataframe_annee.groupby(dataframe_annee[status].dt.month).size()
        if not tickets_clotures_par_mois.empty:
            values_exist = True
        plt.plot(tickets_clotures_par_mois.index, tickets_clotures_par_mois.values, marker='o', label=annee)
    completer_graphe(plt, 'Mois', f'Nombre de tickets {type_ticket}', f'Nombre de tickets {type_ticket}',
                     values_exist)


def tickets_status_par_mois_par_intervalle_version_yaml(dataframe):
    file_data = read_config()['tickets_status_par_intervalles_de_temps_par_mois']
    dataframe = str_df_to_dt_df(dataframe)
    for label in file_data:
        mask = (dataframe[label['status']] >= label['date_min']) & (dataframe[label['status']] <= label['date_max'])
        annees = dataframe.loc[mask, label['status']].dt.year.unique()
        plt.figure(figsize=(10, 6))
        values_exist = False
        for annee in annees:
            dataframe_annee = dataframe[dataframe[label['status']].dt.year == annee]
            tickets_clotures_par_mois = dataframe_annee.groupby(dataframe_annee[label['status']].dt.month).size()
            if not tickets_clotures_par_mois.empty:
                values_exist = True
            plt.plot(tickets_clotures_par_mois.index, tickets_clotures_par_mois.values, marker='o', label=annee)
        completer_graphe(plt, label['xtitre'], label['ytitre'], label['titre_graphe'], values_exist)


def lead_time_par_intervalles_de_temps(dataframe, date_min, date_max, pas_de_temps):
    dataframe = str_df_to_dt_df(dataframe)

    date_min = pd.Timestamp(date_min)
    date_max = pd.Timestamp(date_max)

    date_created = dataframe['created']
    date_resolution = dataframe['resolutiondate']
    dataframe_intervalles = dataframe[
        (date_created.dt.date >= date_min.date()) & (date_resolution.dt.date <= date_max.date())]
    dataframe_intervalles['lead_time'] = (
            dataframe_intervalles['resolutiondate'] - dataframe_intervalles['created']).dt.days

    lead_time_moyen = dataframe_intervalles.groupby(getattr(dataframe_intervalles['created'].dt, pas_de_temps))[
        'lead_time'].mean()

    if pas_de_temps == 'dayofweek':
        return plot_and_save(lead_time_moyen, 'Jour',
                             f'Lead time moyen (jours)',
                             f'Lead time moyen du {date_min.date()} au {date_max.date()}'
                             , "line", 'jour')
    else:
        return plot_and_save(lead_time_moyen, 'Année',
                             f'Lead time moyen (jours)',
                             f'Lead time moyen du {date_min.date()} au {date_max.date()}'
                             , 'points', '')


def lead_time_par_intervalles_de_temps_version_yaml(dataframe):
    file_data = read_config()['lead_time_par_intervalles_de_temps']
    dataframe = str_df_to_dt_df(dataframe)

    for label in file_data:
        date_min = pd.Timestamp(label['date_min'])
        date_max = pd.Timestamp(label['date_max'])

        date_created = dataframe['created']
        date_resolution = dataframe['resolutiondate']
        dataframe_intervalles = dataframe[
            (date_created.dt.date >= date_min.date()) & (date_resolution.dt.date <= date_max.date())]
        dataframe_intervalles['lead_time'] = (
                dataframe_intervalles['resolutiondate'] - dataframe_intervalles['created']).dt.days

        lead_time_moyen = \
            dataframe_intervalles.groupby(getattr(dataframe_intervalles['created'].dt, label['pas_de_temps']))[
                'lead_time'].mean()
        xticks_type = label['xtitre'] if label['xtitre'] == 'jour' else ''
        plot_and_save(lead_time_moyen, label['xtitre'], label['ytitre'],
                      f"{label['titre_graphe']} du {date_min.date()} au {date_max.date()}"
                      , label['type_graphe'], xticks_type)


def lead_time_par_mois(dataframe, date_min, date_max):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['lead_time'] = (dataframe['resolutiondate'] - dataframe['created']).dt.days
    filtered_data = dataframe[(dataframe['created'] >= date_min) & (dataframe['created'] <= date_max)]
    years = filtered_data['created'].dt.year.unique()
    plt.figure(figsize=(10, 6))
    values_exist = False
    for annee in years:
        dataframe_annee = dataframe[dataframe['created'].dt.year == annee]
        # Calculer la moyenne du lead time par mois
        lead_time_moyen = dataframe_annee.groupby(dataframe_annee['created'].dt.month)['lead_time'].mean()
        if not lead_time_moyen.empty:
            values_exist = True
        plt.plot(lead_time_moyen.index, lead_time_moyen.values, marker='o', label=annee)
    completer_graphe(plt, 'Mois', f'Lead time moyen (jours)', f'Lead time moyen du {date_min} au {date_max}',
                     values_exist)
    # if not values_exist:
    #     return values_exist
    # else:
    #     plt.xlabel('Mois')
    #     plt.ylabel(f'Lead time moyen (jours)')
    #     plt.title(f'Lead time moyen du {date_min} au {date_max}')
    #     plt.xticks(range(1, 13),
    #                ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
    #     plt.legend()
    #     filename = os.path.join(config.output_directory, f'Lead time moyen.png')
    #     plt.savefig(filename)
    #     return f'Lead time moyen.png'


def lead_time_par_mois_version_yaml(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    dataframe['lead_time'] = (dataframe['resolutiondate'] - dataframe['created']).dt.days
    file_data = read_config()['lead_time_par_mois']
    for label in file_data:
        filtered_data = dataframe[
            (dataframe['created'] >= label['date_min']) & (dataframe['created'] <= label['date_max'])]
        years = filtered_data['created'].dt.year.unique()
        plt.figure(figsize=(10, 6))
        values_exist = False
        for annee in years:
            dataframe_annee = dataframe[dataframe['created'].dt.year == annee]
            # Calculer la moyenne du lead time par mois
            lead_time_moyen = dataframe_annee.groupby(dataframe_annee['created'].dt.month)['lead_time'].mean()
            if not lead_time_moyen.empty:
                values_exist = True
            plt.plot(lead_time_moyen.index, lead_time_moyen.values, marker='o', label=annee)
        completer_graphe(plt, label['xtitre'], label['ytitre'], label['titre_graphe'], values_exist)


def reliquat_par_intervalle(dataframe, date_min, date_max, pas_de_temps):
    # nb ticket cloturés- nb ticket créés
    dataframe = str_df_to_dt_df(dataframe)
    date_min = pd.Timestamp(date_min)
    date_max = pd.Timestamp(date_max)
    tickets_crees_par_date = tickets_status_data('created', dataframe, date_min, date_max, pas_de_temps)
    tickets_clotures_par_date = tickets_status_data('resolutiondate', dataframe, date_min, date_max, pas_de_temps)

    reliquat_tickets = (tickets_clotures_par_date.fillna(0) - tickets_crees_par_date.fillna(0)).replace(
        [np.inf, -np.inf], np.nan).fillna(0).astype(int)
    reliquat_tickets.index = list(reliquat_tickets.index)
    if pas_de_temps == 'year':
        plot_and_save(reliquat_tickets, 'Année', 'Reliquat',
                      f'Reliquat du {date_min.date()} au {date_max.date()} par année', 'line',
                      '')
    elif pas_de_temps == 'dayofweek':
        plot_and_save(reliquat_tickets, 'Jour', 'Reliquat',
                      f'Reliquat du {date_min.date()} au {date_max.date()} par jour', 'line',
                      'jour')


def reliquat_par_intervalle_version_yaml(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    file_data = read_config()['reliquat_par_intervalle']
    for label in file_data:
        date_min = pd.Timestamp(label['date_min'])
        date_max = pd.Timestamp(label['date_max'])
        tickets_crees_par_date = tickets_status_data('created', dataframe, date_min, date_max, label['pas_de_temps'])
        tickets_clotures_par_date = tickets_status_data('resolutiondate', dataframe, date_min, date_max,
                                                        label['pas_de_temps'])

        reliquat_tickets = (tickets_clotures_par_date.fillna(0) - tickets_crees_par_date.fillna(0)).replace(
            [np.inf, -np.inf], np.nan).fillna(0).astype(int)
        reliquat_tickets.index = list(reliquat_tickets.index)
        xticks_type = label['xtitre'] if label['xtitre'] == 'jour' else ''
        plot_and_save(tickets_clotures_par_date, label['xtitre'], label['ytitre'],
                      f"{label['titre_graphe']} du {date_min.date()} au {date_max.date()}"
                      , label['type_graphe'], xticks_type)


def reliquat_par_mois(dataframe, date_min, date_max):
    dataframe = str_df_to_dt_df(dataframe)
    plt.figure(figsize=(10, 6))
    years = range(pd.Timestamp(date_min).date().year, pd.Timestamp(date_max).year + 1)
    values_exist = False

    for year in years:
        mask = (dataframe['created'].dt.year == year) & (dataframe['created'] >= date_min) & (
                dataframe['created'] <= date_max)
        tickets_crees_par_mois = dataframe[mask].groupby(dataframe[mask]['created'].dt.month).size()

        mask = (dataframe['resolutiondate'].dt.year == year) & (dataframe['resolutiondate'] >= date_min) & (
                dataframe['resolutiondate'] <= date_max)
        tickets_clotures_par_mois = dataframe[mask].groupby(dataframe[mask]['resolutiondate'].dt.month).size()

        reliquat_tickets = tickets_clotures_par_mois - tickets_crees_par_mois

        if not reliquat_tickets.empty:
            values_exist = True
            plt.plot(reliquat_tickets.index, reliquat_tickets.values, marker='o', label=f'Year {year}')
    return completer_graphe(plt, 'Mois', 'Reliquat de tickets', 'Reliquat de tickets par mois', values_exist)


def reliquat_par_mois_version_yaml(dataframe):
    dataframe = str_df_to_dt_df(dataframe)
    file_data = read_config()['reliquat_par_mois']
    plt.figure(figsize=(10, 6))
    for label in file_data:
        years = range(pd.Timestamp(label['date_min']).date().year, pd.Timestamp(label['date_max']).year + 1)
        values_exist = False

        for year in years:
            mask = (dataframe['created'].dt.year == year) & (dataframe['created'] >= label['date_min']) & (
                    dataframe['created'] <= label['date_max'])
            tickets_crees_par_mois = dataframe[mask].groupby(dataframe[mask]['created'].dt.month).size()

            mask = (dataframe['resolutiondate'].dt.year == year) & (
                        dataframe['resolutiondate'] >= label['date_min']) & (
                           dataframe['resolutiondate'] <= label['date_max'])
            tickets_clotures_par_mois = dataframe[mask].groupby(dataframe[mask]['resolutiondate'].dt.month).size()

            reliquat_tickets = tickets_clotures_par_mois - tickets_crees_par_mois

            if not reliquat_tickets.empty:
                values_exist = True
                plt.plot(reliquat_tickets.index, reliquat_tickets.values, marker='o', label=f'Year {year}')
        completer_graphe(plt, label['xtitre'], label['ytitre'], label['titre_graphe'], values_exist)


def completer_graphe(plt, x_titre, y_titre, graphe_titre, values_exist):
    if not values_exist:
        return None
    plt.xlabel(x_titre)
    plt.ylabel(y_titre)
    plt.title(graphe_titre)
    plt.xticks(range(1, 13), ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
    plt.legend()
    plt.tight_layout()

    filename = os.path.join(config.output_directory, f' {graphe_titre}.png')
    plt.savefig(filename)
    plt.close()

    return filename


def plot_and_save(Serie, title_x, title_y, title_graphique, plot_type, xticks_type):
    if Serie.empty:
        return False
    plt.figure(figsize=(10, 6))
    if plot_type == 'points':
        plt.scatter(Serie.index, Serie.values)
    elif plot_type == 'line':
        plt.plot(Serie.index, Serie.values, marker='o')
    plt.xlabel(title_x)
    plt.ylabel(title_y)
    plt.title(title_graphique)
    # if xticks_type == 'jour':
    #     plt.xticks(range(7), ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'])
    if xticks_type == 'mois':
        plt.xticks(range(1, 13),
                   ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'])
    else:
        plt.xticks(rotation=40)
    plt.show()
    filename = os.path.join(config.output_directory, f'{title_graphique}.png')
    plt.savefig(filename)
    plt.clf()
    return f'{title_graphique}.png'


def read_config():
    with open(config.yaml_file, 'r') as file:
        return yaml.safe_load(file)
