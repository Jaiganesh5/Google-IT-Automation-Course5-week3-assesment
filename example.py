#!/usr/bin/env python3

import emails
import os
import reports

table_data=[
  ['Name', 'Amount', 'Value'],
  ['elderberries', 10, 0.45],
  ['figs', 5, 3],
  ['apples', 4, 2.75],
  ['durians', 1, 25],
  ['bananas', 5, 1.99],
  ['cherries', 23, 5.80],
  ['grapes', 13, 2.48],
  ['kiwi', 4, 0.49]]
reports.generate("/home/jaiganesh/Automation/Email_course/report.pdf", "A Complete Inventory of My Fruit", "This is all my fruit.", table_data)

sender = "jaiganeshboopathy@gmail.com"
receiver = "jaiganeshboopathy2000@gmail.com"
password = "Akshitha411"
subject = "List of Fruits"
body = "Hi\n\nI'm sending an attachment with all my fruit."

message = emails.generate(sender, receiver, subject, body, "/home/jaiganesh/Automation/Email_course/report.pdf")
emails.send(message)
