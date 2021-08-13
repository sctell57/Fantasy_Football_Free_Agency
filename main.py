import json
import random

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

import responses
from team_id import users


def welcome_script():
    print("\n\n Type 'search' to search for a player \n then you can bid or see his interest\n"
          )
    return


def search_player(records_df, first_name, last_name):
    d = records_df[records_df['First Name'].str.contains(first_name)]
    player = d[d['Last Name'].str.contains(last_name)]
    player_id = player.iat[0, 13]
    return player_id


def check_id(name):
    person_dict = json.loads(users)
    for player in person_dict:
        if name == player['username']:
            print("Welcome", name)
            return True
    return False
    # Pretty Printing JSON string back


def bid_calculator(price, years):
    x = price
    if years == 1:
        x *= .80
    if years == 2:
        x *= .90
    return x


if __name__ == '__main__':
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('players.json', scope)
    # authorize the clientsheet
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open('bid page')

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    records_data = sheet_instance.get_all_records()
    records_df = pd.DataFrame.from_dict(records_data)

    username = input("\n\n Type in your login:")

    print("Welcome to Fantasy Football for the Boys Free Agency!")
    run = True
    while run:
        b = check_id(username)
        if not b:
            print("\nSorry invalid username\n")
            exit(1)
        input_player = input("enter the name of the player:")
        input_player = input_player.split()
        player_current = search_player(records_df, input_player[0], input_player[1])

        print("You have selected %s %s is that correct?" % (
            records_df.iloc[player_current - 1, 0], records_df.iloc[player_current - 1, 1]))
        c = input("type yes or no:")
        c = c.lower()
        if c != 'yes':
            print("sorry about that try again or contact Steve")
            break

        print(
            "\n\nPlayer name: %s %s" % (records_df.iloc[player_current - 1, 0], records_df.iloc[player_current - 1, 1]))
        print("2020 owner: %s" % records_df.iloc[player_current - 1, 3])
        print("2020 salary: %s" % records_df.iloc[player_current - 1, 5])
        print("FA Type: %s" % records_df.iloc[player_current - 1, 4])
        d = input("Type bid to make a bid on this player,"
                  "type interest to get the players interest level in free agency:")
        print('here')

        if d == 'bid':
            print("Enter the contract price and years in that order")
            print("*Example*\nPrice:10\nYears:3\n**")
            e = input("Price:")
            f = input("Years:")
            e = int(e)
            f = int(f)
            while f > 3:
                print("WRONG!")
                f = input("Years:")
                f = int(f)
            player_bid = bid_calculator(e, f)
            current_bid = bid_calculator(int(records_df.iloc[player_current - 1, 11]),
                                         int(records_df.iloc[player_current - 1, 14]))

            amount_bids = int(records_df.iloc[player_current - 1, 10])
            amount_salary = int(records_df.iloc[player_current - 1, 11])
            bidder = records_df.iloc[player_current - 1, 12]
            if player_bid > current_bid:
                sheet_instance.update_cell(player_current + 1, 15, f)  # years
                sheet_instance.update_cell(player_current + 1, 13, username)
                sheet_instance.update_cell(player_current + 1, 12, e)  # price
                sheet_instance.update_cell(player_current + 1, 11, amount_bids + 1)
                x = 15
                while records_df.iloc[player_current - 1, x] != "":
                    x += 3
                sheet_instance.update_cell(player_current + 1, x+1,
                                           records_df.iloc[player_current - 1, 12])  # old highest bidder
                sheet_instance.update_cell(player_current + 1, x + 2,
                                           int(records_df.iloc[player_current - 1, 14])) # old highest years
                sheet_instance.update_cell(player_current + 1, x + 3,
                                           int(records_df.iloc[player_current - 1, 11])) # old highest price

                if player_bid > current_bid * 2:
                    print(random.choice(responses.amazing_responses))
                else:
                    print(random.choice(responses.good_responses))
            elif player_bid / current_bid >= .80:
                sheet_instance.update_cell(player_current + 1, 11, amount_bids + 1)
                print(random.choice(responses.good_responses))

            else:
                sheet_instance.update_cell(player_current + 1, 11, amount_bids + 1)
                print(random.choice(responses.bad_responses))


        elif d == 'interest':
            inter = records_df.iloc[player_current - 1, 10]
            if inter == 0:
                print("I haven't received an offer yet")
            elif inter < 2:
                print(random.choice(responses.Interest_low))
            else:
                print(random.choice(responses.Interest_high))
            continue
        else:
            continue

        break
