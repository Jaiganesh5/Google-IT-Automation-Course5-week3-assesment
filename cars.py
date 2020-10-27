#!/usr/bin/env python3

import json
import locale
import sys
import emails
import reports

def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
  max_revenue = {"revenue": 0}
  most_sales = 0
  most_selled_car = ""
  year_of_sales = {}
  most_sales_year_count = []
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    #  also handle max sales
    if item["total_sales"] > most_sales:
      most_sales = item["total_sales"]
      most_selled_car = format_car(item["car"])
    #  also handle most popular car_year
    if item["car"]["car_year"] in year_of_sales:
      year_of_sales[item["car"]["car_year"]] += item["total_sales"]
    else:
      year_of_sales[item["car"]["car_year"]] = item["total_sales"]
 
  most_sales_year_count = sorted(year_of_sales.items(),key =lambda x: x[1],reverse = True )
  most_selled_year,most_selled_year_count = most_sales_year_count[0]

  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]), "The {} had the most sales:{}".format(most_selled_car,most_sales), "The most popular year was {} with {} sales.".format(most_selled_year,most_selled_year_count)
  ]
  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data(argv[1])
  summary = process_data(data)
  table_data = cars_dict_to_table(data)
  #  turn this into a PDF report
  reports.generate("/tmp/cars.pdf","Sales Summary for last month","{}<br/>{}<br/>{}<br/>".format(summary[0],summary[1],summary[2]),table_data)
  #  send the PDF report as an email attachment
  sender = "<user>@example.com"
  receiver = "automation@example.com"
  subject = "Sales Summary for last month"
  body = "{}\n{}\n{}\n".format(summary[0],summary[1],summary[2])

  message = emails.generate(sender, receiver, subject, body, "/tmp/cars.pdf")
  emails.send(message)


if __name__ == "__main__":
  main(sys.argv)
