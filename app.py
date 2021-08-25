import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from readdata import read_data
import pydeck as pdk
import altair as alt

# Title the app
st.title('North Lake Ave Traffic Data and Model')

info = read_data()


#    lake_data =  pd.DataFrame({
#        'lat': lat,
#        'lon': lon,
#        'date'   : date_arr,
#        'injury' : injury,
#        'death' : death
#    })


st.markdown("## Historical collisions on N. Lake Ave")

st.markdown("### 2008-2020")

# -- Stats
count = len(info['lat'])
st.markdown("""
During this time period, there were {0} collisions on the N. Lake Ave
corridor, resulting in {1} injuries and {2} deaths.
""".format(count, info['injury'].sum(), info['death'].sum()))

#st.markdown("Number of collisions: {}".format(count))
#st.markdown("Number of injuries: {}".format(info['injury'].sum()))
#st.markdown("Number of deaths: {}".format(info['death'].sum()))

st.markdown("This map shows their locations:")


midpoint = (np.average(info['lat']), np.average(info['lon']))

col_bar, col_map = st.columns(2)

#with col_map:

st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=34.156,
            longitude=-118.132,
            zoom=15,
            pitch=30,
        ),
        layers=[pdk.Layer(
            'ScatterplotLayer',
            data=info,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=10,
        ),
                ],
    ))


#chart = alt.Chart(info).mark_bar().encode(
#    alt.X("date", bin=True),
#    y='count()',
#    )

#st.write(chart)

bins = np.arange(2008, 2022)
# -- Histogram by year
values, bins = hist_values = np.histogram(
    info['date'].dt.year, bins=bins)

bins = bins[0:-1]

good_values = values[np.where(values > 0)]

avg_collision = np.int(np.mean(good_values))
avg_injury    = np.int(info['injury'].sum() / 12)


#st.write(len(bins), len(values))

histdata = pd.DataFrame({
    'year':bins,
    'collisions':values,
    'average':np.ones(len(values))*avg_collision
})

chart2 = alt.Chart(histdata).mark_bar().encode(
    x = 'year:O',
    y = 'collisions'
    ).properties(title='Collisions on N. Lake Ave')

chart3 = alt.Chart(histdata).mark_line(color='gray').encode(
    x = 'year:O',
    y = 'average'
    )

#with col_bar:
#    st.write(chart2)

# st.markdown("The N. Lake Ave corridor averages {0} collisions per year".format(avg_collision))

st.markdown("## Your voice matters!")
st.markdown("### Will you make a change on N. Lake Avenue?  Choose an option below to run the simulation")


build_choice = st.radio("Choose an option:",
                        ["I'm still thinking ...",
                         "Keep the status quo",
                         "Add protected bike lanes!"
                         ])


if build_choice == "Add protected bike lanes!":
    safety = 0.65
else:
    safety = 1

years = np.arange(2023,2033)
loc = avg_collision*safety
model = np.random.normal( loc, scale=np.sqrt(loc), size=len(years))


modeldata =  pd.DataFrame({
    'year':years,
    'collisions':model,
    'average':np.ones(len(years))*avg_collision
})


chart4 = alt.Chart(modeldata).mark_bar().encode(
    alt.Y('collisions',
          scale=alt.Scale(domain=(0, 60))),
    x = 'year:O',
    ).properties(title='Collisions on N. Lake Ave')

    #y = 'collisions'
chart5 = alt.Chart(modeldata).mark_line(color='gray').encode(
    x = 'year:O',
    y = 'average'
    )

col1, col2 = st.columns(2)

with col2:
    if build_choice !="I'm still thinking ...":
        st.markdown("## Model prediction")
        st.write(chart4+chart5)
        #st.markdown("""
#Future collision rates on N. Lake Avenue.  The gray bar shows the historical average of 47 collisions per year.""")

with col1:
    if build_choice == "Keep the status quo":
        st.markdown("## Oh No!")
        st.image('crash.jpg')
        st.markdown("""
        You kept the current design.  We'll continue to see around 
        47 collisions per year, for a cost of 6 million dollars in 
        damages over the next ten years.
        """)

    elif build_choice == "Add protected bike lanes!":
        st.markdown("## Yay!!")
        st.image("bikeportland-image.jpg")
        st.markdown("""
        By adding protected bike lanes, you've reduced the collision rate
        by 35%, saving your neighbors around 2 million dollars in 
        damages and preventing over 100 injuries during the next 10 years.
        """)

if build_choice != "I'm still thinking ...":

    st.markdown("""## Please [TAKE ACTION](https://www.pasadenacsc.org/lakeave#support) to support safety on North Lake Ave
""")


st.markdown("***")
    
with st.expander("See notes"):

    st.markdown("""
 * Historical traffic data from [City of Pasadena Open Data Site](https://data.cityofpasadena.net/datasets/85f49ea583c24056968bee6e28162da4_0/explore?location=34.155947%2C-118.127334%2C12.93)

 * Collision rate reduction due to protected bike lanes is based on a [number of studies](https://www.peopleforbikes.org/statistics/economic-benefits), 
  including a [case study in New York](http://www.nyc.gov/html/dot/downloads/pdf/2011_columbus_assessment.pdf), showing a 34% reduction in collisions. 

 * A [comprehensive study](https://www.pasadenacsc.org/blog/protected-bike-lanes-increase-traffic-safety-for-everyone) of bike lane safety showed dramatic reductions in injuries and fatalities for all road users when adding protected bicycle lanes.

 * You can read more about [North Lake Avenue project](https://www.pasadenacsc.org/lakeave)

 * This app made with [open source code](https://github.com/jkanner/traffic-data)
""")

