import pandas as pd

pd.set_option('display.max_rows', 700)
pd.set_option('display.max_columns', 100)


# read the data
# rename cols to english
# convert lat and long values to float64
def setup_data(path, delimiter):

    df = pd.read_csv(path, delimiter)

    # removing columns where everything is NA
    df.dropna(axis=1, how='all', inplace=True)

    df = df.rename(columns={'MaStR-Nr. der Einheit': 'mastr_no_the_unit'})
    df = df.rename(columns={'Anzeige-Name der Einheit': 'unit_friendly_name'})
    df = df.rename(columns={'Betriebs-Status': 'operational_status'})
    df = df.rename(columns={'Energieträger': 'energy_sources'})
    df = df.rename(columns={'Bruttoleistung der Einheit': 'gross_power_of_the_unit'})
    df = df.rename(columns={'Nettonennleistung der Einheit': 'net_power_rating_of_the_unit'})
    df = df.rename(columns={'Inbetriebnahmedatum der Einheit': 'commissioning_date_of_the_unit'})
    df = df.rename(columns={'Registrierungsdatum der Einheit': 'registration_date_of_the_unit'})
    df = df.rename(columns={'Bundesland': 'federal_state'})
    df = df.rename(columns={'Postleitzahl': 'postal_code'})
    df = df.rename(columns={'Ort': 'location'})
    df = df.rename(columns={'Straße': 'street'})
    df = df.rename(columns={'Hausnummer': 'house_number'})
    df = df.rename(columns={'Gemarkung': 'district'})
    df = df.rename(columns={'Flurstück': 'parcel'})
    df = df.rename(columns={'Gemeindeschlüssel': 'community_key'})
    df = df.rename(columns={'Koordinate: Breitengrad (WGS84)': 'latitude'})
    df = df.rename(columns={'Koordinate: Längengrad (WGS84)': 'longitude'})
    df = df.rename(columns={'Anzahl der Solar-Module': 'number_of_solar_modules'})
    df = df.rename(columns={'Hauptausrichtung der Solar-Module': 'main_orientation_of_the_solar_modules'})
    df = df.rename(columns={'Lage der Einheit': 'location_of_the_unit'})
    df = df.rename(columns={'Letzte Aktualisierung': 'last_update'})
    df = df.rename(columns={'Datum der endgültigen Stilllegung': 'final_decommissioning_date'})
    df = df.rename(columns={'Datum der geplanten Inbetriebnahme': 'date_of_planned_commissioning'})
    df = df.rename(columns={'Name des Anlagenbetreibers (nur Org.)': 'name_of_the_plant_operator'})
    df = df.rename(columns={r'MaStR-Nr. des Anlagenbetreibers': 'mastr_no_of_the_plant_operator'})
    df = df.rename(columns={'Volleinspeisung oder Teileinspeisung': 'full_feed_or_partial_feed'})
    df = df.rename(columns={'MaStR-Nr. der Genehmigung': 'mastr_no_of_approval'})
    df = df.rename(columns={'Name des Anschluss-Netzbetreibers': 'name_of_the_connection_network_operator'})
    df = df.rename(columns={'MaStR-Nr. des Anschluss-Netzbetreibers': 'mastr_no_of_the_connection_network_operator'})
    df = df.rename(columns={'Netzbetreiberprüfung': 'network_operator_check'})
    df = df.rename(columns={'Spannungsebene': 'voltage_level'})
    df = df.rename(columns={'MaStR-Nr. der Lokation': 'mastr_no_the_location'})
    df = df.rename(columns={'MaStR-Nr. der EEG-Anlage': 'mastr_no_the_eeg_system'})
    df = df.rename(columns={'EEG-Anlagenschlüssel': 'eeg_system_key'})
    df = df.rename(columns={'Inbetriebnahmedatum der EEG-Anlage': 'commissioning_date_of_the_eeg_system'})
    df = df.rename(columns={'Installierte Leistung': 'installed_capacity'})
    df = df.rename(columns={'Zuschlagnummer (EEG/KWK-Ausschreibung)': 'surcharge_number'})

    # convert your lat and long to floats
    df['latitude'] = df['latitude'].astype("string")
    df['longitude'] = df['longitude'].astype("string")
    df['latitude'] = df['latitude'].str.replace(',', '.')
    df['longitude'] = df['longitude'].str.replace(',', '.')
    df['latitude'] = df['latitude'].astype("float64")
    df['longitude'] = df['longitude'].astype("float64")

    return df
