#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 11:54:20 2019

@author: dschn
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QComboBox, QMessageBox, QPushButton, QTextBrowser
from PyQt5.QtGui import *
import sys
# import bikeshare_backend
import pandas as pd
import numpy as np
import os
import datetime
import time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.abspath(BASE_DIR + "/")

cities = ['chicago','new_york_city','washington']
pd.set_option('display.max_columns', None)

class my_window(QWidget): # window inherits from QWidget

    def __init__(self):
        """
        Initialization of an object of the class my_window

        """
        super().__init__()
        self.initMe()

    def initMe(self):
        """
        Control function for the created object of my_window
        Control of design and functionality

        """
        self.setGeometry(50,50, 900, 450)
        self.setWindowTitle("US bikeshare Analysis Tool")

        self.lbl_city=QtWidgets.QLabel(self)
        self.lbl_city.move(100,100)
        self.lbl_city.setText("City:")

        self.lbl_month=QtWidgets.QLabel(self)
        self.lbl_month.move(100,150)
        self.lbl_month.setText("Month:")

        self.lbl_day=QtWidgets.QLabel(self)
        self.lbl_day.move(100,200)
        self.lbl_day.setText("Day:")

        self.lbl_raw=QtWidgets.QLabel(self)
        self.lbl_raw.move(50,350)
        self.lbl_raw.setText("Raw Data \nfor \ncurrent \nselection:")

        self.lbl_browser=QtWidgets.QLabel(self)
        self.lbl_browser.move(300,70)
        self.lbl_browser.setText("Dashboard")

        self.cbo_city=QComboBox(self)
        self.cbo_city.move(150,100)
        self.cbo_city.addItems(cities)

        months=self._extract_items_cbo_month()
        self.cbo_month=QComboBox(self)
        self.cbo_month.move(150,150)
        self.cbo_month.addItems(months)

        days=self._extract_items_cbo_day()
        self.cbo_day=QComboBox(self)
        self.cbo_day.move(150,200)
        self.cbo_day.addItems(days)

        self.btn_select=QPushButton("Start\nAnalysis",self)
        self.btn_select.move(150,250)
        self.btn_select.clicked.connect(self._execute)

        self.btn_raw_data=QPushButton("Raw Data",self)
        self.btn_raw_data.move(150,350)
        self.btn_raw_data.clicked.connect(self._raw_data)
        self.btn_raw_data.clicks = 0
        self.btn_raw_data.setToolTip("Please note: \nThe data displayed depends \non the selection made. \nTherefore it is possible \nto display the data \nand the corresponding analysis.")

        self.btn_clear_browser=QPushButton("Clear\nDashboard",self)
        self.btn_clear_browser.move(150,300)
        self.btn_clear_browser.clicked.connect(self._clear_browser)

        self.browser=QtWidgets.QTextBrowser(self)
        self.browser.setGeometry(QtCore.QRect(300, 100, 500, 250))
        self.browser.setObjectName("Browser")

        QMessageBox.information(self,"US bikeshare Analysis","Hello!\n Let\'s explore some US bikeshare data! \n\nWould you like to filter the data \nby month,\nday,\nboth\n\nor not at all?\nUse the DropDowns.\nFor no time filter, choose all!")
        self.show()

# ########
# Raw data
# ########

    def _raw_data(self):
        """
        Shows 5 rows of raw data of the given selection
        as long as -Yes- is selected.

        Returns
        -------
        None.

        """
        df=self._create_df()
        data_row = 0
        msg_box = QMessageBox
        message = 16384
        print(msg_box.No)
        while message == 16384:
            data = df.iloc[data_row : data_row + 5]
            self.browser.append("########" + "\n" +
                                "Raw Data" + "\n" +
                                "########" + "\n" +
                                str(data))
            print(data_row)
            data_row += 5
            message = msg_box.question(self,"Raw Data","As long as you want to append\n5 more rows\nclick Yes.",QMessageBox.Yes | QMessageBox.No)
        else:
            msg_box.information(self,"Raw Data","The desired lines of data\ncan be analyzed in the dashboard.")


# ###########
# Creation df
# ###########

    def _clear_browser(self):
        """
        Anables the User to clear QtWidgets.QTextBrowser "browser"

        Returns
        -------
        None.

        """
        self.browser.clear()

    def _select_city_1(self):
        """
        Step 1 of DataFrame-Creation
        Processing user selection given by self.cbo_city.currentText()
        Takes user selection of a city to determine the desired .csv-file to analyze.

        Preparation of DataFrame:
            New columns
            month,
            month_name,
            day,
            hour are created based on Start Time

        Returns
        -------
            df - Pandas DataFrame based on choosed .csv
        """
        file=self.cbo_city.currentText()
        data_import = os.path.join(data_path + "/" + file +".csv")
        df = pd.read_csv(data_import)
        df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
        df['month'] = df["Start Time"].dt.month
        df['month_name'] = df["Start Time"].dt.month_name()
        df['day'] = df["Start Time"].dt.weekday_name
        df['hour'] = df['Start Time'].dt.hour
        return df

    def _select_month_2(self):
        """
        Step 2 of DataFrame-Creation
        Recieves the prepared DataFrame from step 1
        Processing user selection given by self.cbo_month.currentText()

        Returns
        -------
        df - Pandas DataFrame filtered by month and city

        """
        df=self._select_city_1()
        month=self.cbo_month.currentText()

        if month != 'All':
            df_filt = df.loc[df['month_name'] == month]
        else:
            df_filt = df
        return df_filt

    def _select_day_3(self):
        """
        Step 3 of DataFrame-Creation
        Recieves the prepared DataFrame from step 2
        Processing user selection given by self.cbo_day.currentText()

        Returns
        -------
        df - Pandas DataFrame filtered by month, city and day

        """

        df=self._select_month_2()
        day=self.cbo_day.currentText()
        if day != 'All':
            df_filt = df[df['day'] == day.title()]
        else:
            df_filt = df
        return df_filt

    def _create_df(self):
        """
        Final step of DataFrame-Creation
        Recieves the prepared DataFrame from step 3
        Used for better overview
        Returns
        -------
        df - Pandas DataFrame filtered by month, city and day

        """
        df=self._select_day_3()
        return df

# #############################
# Fill in cbo items dynamically
# #############################
    def _extract_items_cbo_month(self):
        """
        Dynamically filling of  the cbo_month
        Depends on the choosed .csv (city)

        Returns
        -------
        lst_month : list
            Contains the month names of the chosen .csv without duplicates

        """
        df=self._select_city_1()
        lst_month=df["Start Time"].dt.month_name().unique().tolist()
        lst_month.append("All")
        lst_month.sort()
        return lst_month

    def _extract_items_cbo_day(self):
        """
        Dynamically filling of the cbo_day
        Depends on the choosed .csv (city)
        Recieves the DataFrame filtered by city

        Returns
        -------
        lst_day : list
            Contains the days names of the chosen .csv without duplicates

        """
        df=self._select_city_1()
        lst_day=df["Start Time"].dt.weekday_name.unique().tolist()
        lst_day.append("All")
        lst_day.sort()
        return lst_day

# ##########
# Statistics
# ##########
    def _most_pop_time_to_travel(self):
        """
        Displays statistics on the most frequent times of travel.
        Recieves the finally filtered DataFrame.

        Returns
        -------
        m_pop_month : numpy.float64

        m_pop_weekday : numpy.float64

        m_pop_hour : numpy.float64

        """

        df=self._create_df()
        m_pop_month = df['month'].mode()[0]
        m_pop_weekday = df['day'].mode()[0]
        m_pop_hour = df['hour'].mode()[0]

        return m_pop_month, m_pop_weekday, m_pop_hour

    def _most_pop_route(self):
        """
        Calculates statistics on the most popular stations and trip.
        Recieves the finally filtered DataFrame.

        Returns
        -------
        m_pop_start_station : str

        m_pop_end_station : str

        m_freq_comb : str

        """


        df=self._create_df()
        m_pop_start_station = df['Start Station'].value_counts().idxmax()
        m_pop_end_station = df['End Station'].value_counts().idxmax()
        joined_route = df['Start Station'] + " _to_ " + df['End Station']
        m_freq_comb = joined_route.value_counts().idxmax()

        return m_pop_start_station, m_pop_end_station, m_freq_comb


    def bike_users_type(self):
        """
        Calculates statistics on bikeshare users types
        Recieves the finally filtered DataFrame.

        Returns
        -------
        num_of_user_type : pandas.core.series.Series

        """
        df=self._create_df()
        num_of_user_type = df['User Type'].value_counts()
        return num_of_user_type

    def _bike_users(self):
        """
        Calculates statistics on bikeshare users
        Recieves the finally filtered DataFrame.

        Returns
        -------
        min_b_y: float

        max_b_y: float

        most_pop_b_y: numpy.float64

        num_of_gender: pandas.core.series.Series

        """
        df=self._create_df()
        min_b_y = 0
        max_b_y = 0
        most_pop_b_y = 0
        num_of_gender = 0
        try:
            min_b_y = df['Birth Year'].min()
            max_b_y = df['Birth Year'].max()
            most_pop_b_y = df['Birth Year'].mode()[0]
            num_of_gender = df['Gender'].value_counts()

            return int(min_b_y), int(max_b_y), int(most_pop_b_y), num_of_gender
        except TypeError:
            QMessageBox.information(self,"Please note!","Information about gender and year of birth \nnot given for washington.")
            pass
        except KeyError:
            QMessageBox.information(self,"Please note!","Information about gender and year of birth \nnot given for washington.")
            pass

    def _total_and_average_trip_duration(self):
        """
        Displays statistics on the total and average trip duration.
        Recieves the finally filtered DataFrame.

        Returns
        -------
        converted_total_travel_time : class pandas._libs.tslibs.timedeltas.Timedelta

        converted_mean_travel_time : class pandas._libs.tslibs.timedeltas.Timedelta

        """

        df=self._create_df()
        total_travel_time = df["Trip Duration"].sum()
        mean_travel_time = df["Trip Duration"].mean()
        converted_total_travel_time = pd.to_timedelta(total_travel_time,unit ='s')
        converted_mean_travel_time = pd.to_timedelta(mean_travel_time,unit = 's')

        return converted_total_travel_time, converted_mean_travel_time



    def _execute(self):
        """
        Main function
        Recieves all calculated data
        Is connected to self.btn_select
        Excecutes all functions
        Submits all informations required information to self.browser

        Returns
        -------
        None.

        """
        sel_city=self.cbo_city.currentText()
        sel_month=self.cbo_month.currentText()
        sel_day=self.cbo_day.currentText()
        total_travel_time = self._total_and_average_trip_duration()[0]
        mean_travel_time = self._total_and_average_trip_duration()[1]
        m_pop_month = self._most_pop_time_to_travel()[0]
        m_pop_weekday = self._most_pop_time_to_travel()[1]
        m_pop_hour = self._most_pop_time_to_travel()[2]

        m_pop_start_station = self._most_pop_route()[0]
        m_pop_end_station = self._most_pop_route()[1]
        m_freq_comb = self._most_pop_route()[2]

        num_of_user_type = self.bike_users_type()

        earliest_birth_year = "Information not given"
        most_recent_birth_year = "Information not given"
        common_birth_year = "Information not given"
        num_of_gender = "Information not given"
        try:
            earliest_birth_year = self._bike_users()[0]
            most_recent_birth_year = self._bike_users()[1]
            common_birth_year = self._bike_users()[2]
            num_of_gender = self._bike_users()[3]
        except:
            pass
        self.browser.append("###############################" + "\n" +
                            "Your filtering: " + str(sel_city) + ", " + str(sel_month) + ", " + str(sel_day) + "\n" +
                            "###############################" + "\n" +
                            "Based on your filtering, the following result is obtained:" + "\n\n" +
                            "Stations and Trip:" + "\n" +
                            "------------------" + "\n" +
                            "Most commonly used start station: \n" + str(m_pop_start_station) + "\n\n" +
                            "Most commonly used end station: \n" + str(m_pop_end_station) + "\n\n" +
                            "Most frequent combination of start station and end station trip: " + "\n\n" + str(m_freq_comb) + "\n" +


                            "Most popular hour: " + str(m_pop_hour)+ "\n" +
                            "Most popular weekday: " + str(m_pop_weekday) + "\n" +
                            "Most popular month: " + str(m_pop_month) + "\n\n" +
                            "Travel time:" + "\n" +
                            "-----------" + "\n" +
                            "Total travel time: " + str(total_travel_time) + "\n" +
                            "Mean travel time: " + str(mean_travel_time) + "\n\n" +
                            "Bike Users:" + "\n" +
                            "-----------" + "\n" +
                            "Earliest birth year: " + str(earliest_birth_year) + "\n" +
                            "Most recent birth year: " + str(most_recent_birth_year) + "\n" +
                            "Common birth year: " + str(common_birth_year) + "\n\n" +
                            "Num of User Type: " + "\n" +
                            str(num_of_user_type) + "\n\n" +
                            "Num of Gender: " + "\n" +
                            str(num_of_gender) + "\n"
                            )


if __name__ == "__main__":
    app=QApplication(sys.argv)
    w=my_window()
    sys.exit(app.exec_())
