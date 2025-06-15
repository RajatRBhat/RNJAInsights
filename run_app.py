import streamlit as st
import webbrowser
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import timedelta

st.set_page_config(
                        page_title='🚩Rama Nama Japa Abhiyana 🚩',
                        initial_sidebar_state='auto',
                        layout="wide"
                        )

if 'gform' not in st.session_state:
    st.session_state.gform = 0

if 'selected_week' not in st.session_state:
    st.session_state['selected_week'] = None

if 'button_clicked' not in st.session_state:
    st.session_state['button_clicked'] = False

@st.cache_data(show_spinner=False)
def get_data():
    file_path = "https://docs.google.com/spreadsheets/d/1pT8TOekAR_SRe999KEMKls4H2w09B-LG9VpvTB3sxo0/export?format=csv"
    return pd.read_csv(file_path)

def clear_cache():
    st.cache_data.clear()


st.sidebar.button("Refresh Page",key="main_page", on_click=clear_cache,help="Click to get latest updated data",type="primary")

class RNJA:

    def __init__(self):
        self.file_path = "https://docs.google.com/spreadsheets/d/1pT8TOekAR_SRe999KEMKls4H2w09B-LG9VpvTB3sxo0/export?format=csv"
        self.df = get_data()
        self.final_cols = ['Date','Week Day','Week No','Session Id','No of Japakas','No of Japa','Total Japa']
        self.preprocess_data()

    def load_dataframe(self):
        self.df = pd.read_csv(self.file_path)
        return self.df
    
    @staticmethod
    def formatINR(number):
        s, *d = str(number).partition(".")
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)
    
    def preprocess_data(self):
        self.df.drop(columns=['Timestamp'], inplace=True)
        self.df['No of Japa'] = self.df['No of Japa'].fillna(0).astype(int)
        self.df['No of Japakas'] = self.df['No of Japakas'].fillna(0).astype(int)
        self.df['Total Japa'] = self.df['No of Japakas'] * self.df['No of Japa']
        self.df['Total Japa'] = np.where(self.df['Total Japa']==0, self.df['Total Japa Count'], self.df['Total Japa']).astype(int)
        self.df['Archak Name'].fillna(self.df['Archak Name'][0], inplace=True)
        self.df['Event date'] = pd.to_datetime(self.df['Event date'])
        self.df['Week Day'] = self.df['Event date'].dt.day_name()
        self.df['week_iso'] = self.df['Event date'].dt.strftime('%Y-%U')
        self.df['week_iso'] = np.where(self.df['week_iso']=='2025-00', '2024-52', self.df['week_iso'])
        self.df['Week No'] = self.df['week_iso'].rank(method='dense').astype(int)
        self.df['Date'] = self.df['Event date'].dt.date
        self.df['DayOfWeek'] = self.df['Event date'].dt.dayofweek
        self.df['DayOfWeek'] = np.where(self.df['DayOfWeek']==6,-1,self.df['DayOfWeek'])

        self.df = self.df.sort_values(by=['Date', 'Session Id'],ascending=[False,True])

    def button_clicked(self):
        st.session_state['button_clicked'] = True

    def load_ui(self):
        with st.sidebar:
            with st.form("form_rnja"):
                st.markdown("<h3 style='text-align: center; color:  Yellow;'> 🛕 Rama Nama Japa Abhiyana 🚩 </h3>", 
                    unsafe_allow_html=True)
                st.image("rnja_math.png")
                selected_option = st.selectbox(label='Select Option',options=['Home', 'Summary', 'Insights', 'Detailed Data'],index=1)
                submit_button = st.form_submit_button("Submit", on_click=self.button_clicked)
        
        if st.session_state['button_clicked']:
            if selected_option == "Summary":
                self.display_summary()
            elif selected_option == "Insights":
                self.show_insights()
            elif selected_option == "Detailed Data":
                self.show_detailed_data()
            else:
                self.show_home_page()
        else:
            self.display_summary()
    
    def show_home_page(self):
        st.markdown("<h2 style='text-align: center; color:  orange;'> Welcome to Rama Nama Japa Abhiyana Page </h2>", 
                unsafe_allow_html=True)
        st.header("", divider='rainbow')
        
        col1,col2 = st.columns([0.75,0.25])

        with col1:
            st.markdown(f"<h3 style='text-align: center; font-family:Didot; color:  #9999ff;'> 🚩 Japa Center Details 🚩 </h3>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: left; font-family:cursive; color:  #ff9933;'> Center Name : Raghunatha </h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: left; font-family:cursive; color:  #ff9933;'> Center Address : Raghunath Temple, Bhatkal </h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: left; font-family:cursive; color:  #ff9933;'> Japa Timings : Daily at 05:30 pm </h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: left; font-family:cursive; color:  #ff9933;'> Contact Details : +91-8123486470 </h4>", unsafe_allow_html=True)

            st.divider()
            st.markdown(f"<h6 style='text-align: left; font-family:Tahoma; color:  #cc3399;'> * Select any options from left side and click on Submit button to proceed... </h6>", unsafe_allow_html=True)

        with col2:
            st.image("srt.jpeg", caption="Lord RamDev, Raghunath Temple, Bhatkal",use_column_width="always")

    def display_summary(self):
        latest_date = self.df.head(1)['Date'].values[0]
        st.markdown("<h1 style='text-align: center; color:  red;'> 🛕 Rama Nama Japa Abhiyana 🕉️ </h1>", 
                unsafe_allow_html=True)
        st.header("", divider='rainbow')
        colx, coly = st.columns([0.2,0.8])

        with colx:
            #st.button("Fill Japa Details",key=f"japa_details{st.session_state.gform}", on_click= open_link, help="Click here to access google form")
            st.link_button("Fill Japa Details", "https://docs.google.com/forms/d/e/1FAIpQLSfs3Ll7uH0_7KK6KJQEY0dQdwdIviNSuN_4hr2dbbX9OJ3aHw/viewform?fbzx=8395130956874425028", type="primary")

        with coly:
            st.markdown("<h3 style='text-align: center; font-family:Cambria; color:  #9999ff;'> 🚩 Japa Center : Raghunatha 🏹</h3>", 
                    unsafe_allow_html=True)
        
        col11, col22 = st.columns([0.2,0.8])
        with col11:
            st.button("Refresh Data 🔄",key="summary_page",on_click=clear_cache,help="Click to get latest updated data",type="primary")
        with col22:
            st.markdown(f"<h5 style='text-align: center; font-family:cursive; color:  #99ff66;'> * Last Updated for Date : {self.df.head(1)['Date'].values[0]}, {self.df.head(1)['Week Day'].values[0]} 🕰️ </h5>", 
                    unsafe_allow_html=True)
        st.text("")
        col1, col2, col3 = st.columns(3)
        with col1:
            total_japa = self.df['Total Japa'].sum()
            st.metric(label=":blue[Total Japa Till Today 🏆]",value=self.formatINR(total_japa))
        with col2:
            current_week_japa = self.df[self.df['Week No'] == self.df['Week No'].max()]['Total Japa'].sum()
            last_week_japa = self.formatINR(self.df[self.df['Week No'] == self.df['Week No'].max()-1]['Total Japa'].sum())
            #current_week_japa = f"{current_week_japa:,}"
            st.metric(label=":orange[Current Week Total Japa 🗓️]", value=self.formatINR(current_week_japa), help=f"Last Week Total Japa : {last_week_japa}")
        with col3:
            no_of_days = (self.df['Date'].max() - self.df['Date'].min()).days+1
            total_duration = 550
            days_remaining = total_duration - no_of_days
            st.metric(label=":violet[Days Passed / Days Remaining 🚀]", value=f"{no_of_days}/{days_remaining}")

        col4, col5 = st.columns([0.38,0.78])

        with col4:
            today_japa_count = self.df[self.df['Date'] == latest_date]['Total Japa'].sum()
            prev_date = latest_date - timedelta(days=1)
            prev_day_japa_count = self.df[self.df['Date'] == prev_date]['Total Japa'].sum()
            perc_change = int((today_japa_count- prev_day_japa_count)*100/prev_day_japa_count)
            st.metric(label=":blue[Today's Japa 🎰]",value=self.formatINR(today_japa_count), delta=f"{perc_change}%")

        with col5:
            tmp_df = self.df[self.df['Date'] == latest_date][['Session Id', 'No of Japakas', 'No of Japa']]
            tmp_df.rename(columns={'Session Id':'Session', 'No of Japakas':'Japakas', 'No of Japa':'Japa Count'},inplace=True)
            tmp_df.set_index('Session',inplace=True)
            st.metric(label=":orange[Today's Session Wise Japa Details 📝]",value="")
            styled_df = tmp_df.style.set_table_styles(
                                                        [{
                                                            'selector': 'th',
                                                            'props': [
                                                                ('background-color', '#FFBD33'),
                                                                ('color', 'Blue'),
                                                                ('font-family', 'Arial, sans-serif'),
                                                                ('font-size', '16px'),
                                                                ('border', '2px solid black')
                                                            ]
                                                        }, 
                                                        {
                                                            'selector': 'td',
                                                            'props': [
                                                                ('border', '2px solid black'),
                                                                ('background-color', 'white'),
                                                                ('color', 'Black'),
                                                                ('font-family', 'Tahoma'),
                                                                ('font-weight', 'bold'),
                                                                ('font-size', '22px')
                                                            ]
                                                        }]
                                                    )
            with st.expander(":red[Expand this to see today's Japakas and Japa Count 👇]"):
                #st.dataframe(tmp_df.style.applymap(lambda val: 'color: violet'),width=500)
                st.write(styled_df.to_html(), unsafe_allow_html=True)
            
        col6,col7,col8 = st.columns(3)

        with col6:
            target_japa = 55000000
            remaining_japa = target_japa-total_japa
            st.metric(label=":orange[Japa to be Completed 🏅]",value=self.formatINR(remaining_japa))
        
        with col7:
            avg_japa_per_day = round(total_japa/no_of_days)
            st.metric(label=":violet[Daily Average Japa 🧭]",value=self.formatINR(avg_japa_per_day))

        with col8:
            avg_target_japa = round(remaining_japa/days_remaining)
            st.metric(label=":violet[Targeted Average Japa 🎯]",value=self.formatINR(avg_target_japa))

    def show_dataframe(self):
        copy_df = self.df[self.final_cols].copy()
        copy_df.set_index('Date',inplace=True)
        if st.session_state['selected_week'] is not None and st.session_state['selected_week'] != 'Data':
            copy_df = copy_df[copy_df['Week No'] == int(st.session_state['selected_week'])]
        style_df = copy_df.style.set_table_styles(
                                                        [{
                                                            'selector': 'th',
                                                            'props': [
                                                                ('background-color', '#FFBD33'),
                                                                ('color', 'Blue'),
                                                                ('font-family', 'Arial, sans-serif'),
                                                                ('font-size', '18px'),
                                                                ('border', '2px solid black')
                                                            ]
                                                        }, 
                                                        {
                                                            'selector': 'td',
                                                            'props': [
                                                                ('border', '2px solid black'),
                                                                ('background-color', 'white'),
                                                                ('color', 'Black'),
                                                                ('font-family', 'Tahoma'),
                                                                ('font-weight', 'bold'),
                                                                ('font-size', '16px')
                                                            ]
                                                        }]
                                                    )
        #st.dataframe(self.df[self.final_cols],hide_index=True,use_container_width=True)
        with st.expander(":violet[Expand this to see complete japa data 👇]"):
            st.write(style_df.to_html(), unsafe_allow_html=True)

    def get_week_no_options(self):
        week_options = []
        start_date = self.df['Date'].min()
        end_date = self.df['Date'].max()
        week_val = f"Overall Data ({str(start_date)} to {str(end_date)})"
        week_options.append(week_val)

        for week in self.df['Week No'].unique():
            start_date = self.df[self.df['Week No'] == week]['Date'].min()
            end_date = start_date + timedelta(days=6)
            week_val = f"Week {week} ({str(start_date)} to {str(end_date)})"
            week_options.append(week_val)
        
        return week_options


    def show_detailed_data(self):
        st.markdown("<h1 style='text-align: center; color:  red;'> 🛕 Rama Nama Japa Abhiyana 🕉️ </h1>", 
                unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; font-family:cursive; color:  #ff9933;'> Japa Center Name : Raghunatha </h4>", unsafe_allow_html=True)
        st.header("", divider='rainbow')
        st.markdown("<h3 style='text-align: center; color:  yellow;'> Complete Data of Daily Japa Activity  📊</h3>", 
                unsafe_allow_html=True)
        week_options = self.get_week_no_options()
        col111, col112 = st.columns(2)
        with col111:
            selected_week = st.selectbox(":violet[Select Week]", week_options)
        st.session_state['selected_week'] = selected_week.split(' ')[1]
        with col112:
            if st.session_state['selected_week'] != 'Data':
                selected_week_total = self.df[self.df['Week No'] == int(st.session_state['selected_week'])]['Total Japa'].sum()
            else:
                selected_week_total = self.df['Total Japa'].sum()
            st.metric(label=":orange[Total Japa for the selected week 🗓️]", value=self.formatINR(selected_week_total))
        
        self.show_dataframe()

    def show_insights(self):
        st.markdown("<h1 style='text-align: center; color:  red;'> 🛕 Rama Nama Japa Abhiyana 🕉️ </h1>", 
                unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; font-family:cursive; color:  #ff9933;'> Japa Center Name : Raghunatha </h4>", unsafe_allow_html=True)
        st.header("", divider='rainbow')

        current_week = self.df['Week No'].max()
        temp_df2 = self.df[self.df['Week No'] == current_week].groupby(['Week Day','DayOfWeek'])['Total Japa'].sum().reset_index()
        fig2 = px.bar(temp_df2.sort_values('DayOfWeek'),x='Week Day',y='Total Japa',
                      text_auto=True,title=f"Current Week (week no : {current_week}) Japa Day Wise",color_discrete_sequence=['#C0E9B9'])
        fig2.update_xaxes(tickmode='linear')
        st.plotly_chart(fig2,use_container_width=True)

        df11 =self.df.groupby('Week No')['Total Japa'].sum().reset_index()
        fig = px.bar(df11,x='Week No',y='Total Japa',text_auto=True,title="Weekwise Japa Trend")
        fig.update_xaxes(tickmode='linear')
        st.plotly_chart(fig,use_container_width=True)

        temp_df = self.df.groupby(['Week No','Week Day'])['Total Japa'].sum().reset_index()
        fig1 = px.bar(temp_df,x='Week No',y='Total Japa',color='Week Day',
                      barmode="stack",text_auto=True,title="Daywise breakup trend",
                      category_orders={'Week Day':['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']})
        fig1.update_xaxes(tickmode='linear')
        st.plotly_chart(fig1,use_container_width=True)

rnja_srt = RNJA()
rnja_srt.load_ui()
    

        
