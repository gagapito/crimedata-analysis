import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# SETTING UP DATAFRAME #
la_crime_data = 'data/Crime_Data_from_2020_to_Present.csv'

@st.cache
def get_data(filename):
    df = pd.read_csv(filename)
    return df

# STREAMLIT CODE #
header = st.container()
dataset = st.container()
map_model = st.container()
vict_model = st.container()
crime_model = st.container()
race_crime_model = st.container()

with header:
    st.title('Los Angeles Crime Data Analysis')
    st.text('In this project I look into the crime data for the City of Los Angeles. The dataset is analyzed using different models while' '\n' 'focusing on different parts of the data. I was interested in this data because I am from Los Angeles and I thought it would be' '\n' 'a great way to use a dataset to develop into a project for my resume.')

with dataset:
    st.header('LA Crime Dataset')
    st.text('I found this dataset on the LA City website. The data is reflective of incidents of crime in the City of Los' '\n' 'Angeles dating back to 2020. The data is as accurate as the data in the database as it is transcribed by data' '\n' 'typed on paper as provided by the Los Angeles Police Department(LAPD).')
    link = '[Dataset Link](https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8)'
    st.markdown(link, unsafe_allow_html=True)

with map_model:
    st.header('Map Crime Model')
    st.text('In this map model we can look at the geographical coordinates where crimes have been reported. These data points' '\n' 'can be filtered by the different reporting sections of the Los Angeles area used by the LAPD.')

    # crime map model
    map_col, sel_col = st.columns(2)

    map_option = sel_col.selectbox('Filter crime data points based on area selection:', 
    options=['Southwest','Central','N Hollywood','Mission','Harbor','Hollenbeck','Rampart'])

    def map_filter():
        df = get_data(la_crime_data)
        df = df[(df.iloc[:, 1:] != 0).all(1)]

        if 'Southwest' in map_option:
            df_filter = df[(df['AREA NAME'] == 'Southwest')]
        if 'Central' in map_option:
            df_filter = df[(df['AREA NAME'] == 'Central')]
        if 'N Hollywood' in map_option:
            df_filter = df[(df['AREA NAME'] == 'N Hollywood')]
        if 'Mission' in map_option:
            df_filter = df[(df['AREA NAME'] == 'Mission')]
        if 'Harbor' in map_option:
            df_filter = df[(df['AREA NAME'] == 'Harbor')]
        if 'Hollenbeck' in map_option:
            df_filter = df[(df['AREA NAME'] == 'Hollenbeck')]
        if 'Rampart' in map_option:
            df_filter = df[(df['AREA NAME'] == 'Rampart')]

        return df_filter
        
    df_selected = map_filter()
    map_data = df_selected[['latitude', 'longitude']]
    map = map_col.map(map_data.head(50))

with vict_model:
    st.header('Victim Analysis')

    df = get_data(la_crime_data)
    df = df[(df.iloc[:, 1:] != 0).all(1)]

    # age distribution bar chart
    st.subheader('Bar Chart - Age Distribution')
    st.text('The bar chart shows the age distribution of victims of crimes in the City of Los Angeles. From the data, we can interpret that' '\n' 'crimes are commited towards younger individuals (ages 18 - 40) than older individuals (ages 40+). The highest amount of crimes' '\n' 'are committed against 30 and 35 year olds while the lowest number of crimes are committed towards victims that are in their' '\n' 'late 60s.')

    age_distribution = pd.DataFrame(df['Vict Age'].value_counts()).head(50)
    st.bar_chart(age_distribution)
    
    # gender distribution pie chart
    st.subheader('Pie Chart - Gender Distribution')
    st.text('The pie chart shows the gender distribution of victims of crimes in the City of Los Angeles. From the data, we can conclude that' '\n' 'more men than women are affected by crimes with men being victims of 53% of crimes and women being victims of 48% of crimes.')

    gender = ['M', 'F']
    m_value = df['Vict Sex'].value_counts()[0]
    f_value = df['Vict Sex'].value_counts()[1]
    values = [m_value, f_value]

    fig = go.Figure(
        go.Pie(
            labels = gender,
            values = values,
            hoverinfo = "label+percent",
            textinfo = "value"
    ))

    st.plotly_chart(fig)

with crime_model:
    st.header('Crime Analysis')

    st.text('The chart is a distribution of the occurence of different crime codes reported in incidents throughout Los Angeles.' '\n' 'Click the link below to view a document explaining the different crime codes.')

    # crime code distribution bar chart
    df = get_data(la_crime_data)
    crmcd_distribution = pd.DataFrame(df['Crm Cd'].value_counts()).head(50)
    st.bar_chart(crmcd_distribution)

    link = '[Crime Codes](https://oag.ca.gov/sites/all/files/agweb/pdfs/cjsc/prof10/codes.pdf)'
    st.markdown(link, unsafe_allow_html=True)

with race_crime_model:
    st.header('Types of Crimes')
    st.text('This feature allows users to determine the number of specific crimes committed towards the specificed race of the victim.' '\n' 'Here you get to choose the hyperparameters of the model and see how the performance changes.')

    df = get_data(la_crime_data)

    sel_col, disp_col = st.columns(2)

    crime_option = sel_col.selectbox("Filter the selection for the crime you want to select:", 
    options=[
        'ARSON', 'ASSAULT WITH DEADLY WEAPON ON POLICE OFFICER', 'ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT', 'ATTEMPTED ROBBERY',
        'BATTERY - SIMPLE ASSAULT', 'BATTERY WITH SEXUAL CONTACT', 'BIKE - STOLEN', 'BOMB SCARE', 'BRIBERY', 'BUNCO, GRAND THEFT', 'BURGLARY', 'BURGLARY FROM VEHICLE',
        'CHILD ABANDONMENT', 'CHILD ABUSE (PHYSICAL) - AGGRAVATED ASSAULT', 'CHILD ABUSE (PHYSICAL) - SIMPLE ASSAULT', 'CHILD NEGLECT (SEE 300 W.I.C.)', 'CHILD PORNOGRAPHY', 'CHILD STEALING', 'CONSPIRACY', 'COUNTERFEIT', 'CREDIT CARDS, FRAUD USE ($950.01 & OVER)', 'CRIMINAL HOMICIDE',
        'DISCHARGE FIREARMS/SHOTS FIRED', 'DISHONEST EMPLOYEE - GRAND THEFT', 'DISHONEST EMPLOYEE - PETTY THEFT', 'DISRUPT SCHOOL', 'DOCUMENT FORGERY / STOLEN FELONY',
        'EMBEZZLEMENT, GRAND THEFT ($950.01 & OVER)', 'EXTORTION',
        'HUMAN TRAFFICKING - COMMERCIAL SEX ACTS',
        'ILLEGAL DUMPING', 'INTIMATE PARTNER - AGGRAVATED ASSAULT', 'INTIMATE PARTNER - SIMPLE ASSAULT',
        'KIDNAPPING',
        'PICKPOCKET',
        'RAPE, FORCIBLE', 'RECKLESS DRIVING', 'ROBBERY',
        'SEX OFFENDER REGISTRANT OUT OF COMPLIANCE', 'SHOPLIFTING-GRAND THEFT ($950.01 & OVER)', 'SHOTS FIRED AT MOVING VEHICLE, TRAIN OR AIRCRAFT', 'STALKING',
        'THEFT FROM MOTOR VEHICLE - GRAND ($400 AND OVER)', 'THEFT OF IDENTITY', 'THEFT, PERSON', 'TRESPASSING',
        'VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)', 'VANDALISM - MISDEAMEANOR ($399 OR UNDER)', 'VEHICLE - STOLEN', 'VIOLATION OF COURT ORDER', 'VIOLATION OF RESTRAINING ORDER',
        'WEAPONS POSSESSION/BOMBING',
        'OTHER MISCELLANEOUS CRIME'
    ])
    
    race_option = sel_col.radio("Filter the selection for race:",
    options=['Black', 'Hispanic/Latino', 'White', 'Asian', 'Other', 'Unknown'])

    def crime_count():
         r = race_finder()
         groupby = df.groupby(['Crm Cd Desc', 'Vict Descent'], axis=0).size().reset_index(name='count')
         groupby = groupby.set_index(['Crm Cd Desc', 'Vict Descent'])
         count = groupby.at[(crime_option, r), 'count']
         return count

    def race_finder():
        if 'Black' in race_option:
            return 'B'
        if 'Hispanic/Latino' in race_option:
            return 'H'
        if 'White' in race_option:
            return 'W'
        if 'Asian' in race_option:
            return 'A'
        if 'Other' in race_option:
            return 'O'
        else:
            return 'X'

    disp_col.subheader('The number of ' + crime_option + ' crimes committed against victims of this race ' + race_option + ':')
    disp_col.text(crime_count())