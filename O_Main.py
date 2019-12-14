import Crawler
import pandas as pd


def check_all_websites(start, end):
    try:
        # Empty lists
        is_exist_list = []
        is_welcome_list = []
        html_list = []
        base_html = "https://store.steampowered.com/app/"
        # Create DataFrame Consists website condition
        for i in range(start, end, -1):
            start = i
            app_number_rest = ""
            if len(str(i)) <= 6:
                miss_length = 6 - len(str(i))
                for a in range(miss_length):
                    app_number_rest = app_number_rest + "0"
                app_number_rest = app_number_rest + str(i)
            else:
                app_number_rest = str(i)
            whole_html = str(base_html + app_number_rest) + "/"
            # Check whether website exists
            is_exist, is_welcome = Crawler.check_page_condition(whole_html)
            # print checking result
            if is_exist == "1":
                if is_welcome == "0":
                    # Append checking list
                    is_exist_list.append(is_exist)
                    is_welcome_list.append(is_welcome)
                    html_list.append(whole_html)
                    print("Now Crawling: ", whole_html, ": The app exists.")
                else:
                    print("Now Crawling: ", whole_html)
            else:
                print("Now Crawling: ", whole_html)
            # append the dataframe while reach limit
            if i % 1000 == 0:
                website_condition_df = pd.DataFrame({
                    'html_link': html_list,
                    'is_exist': is_exist_list,
                    'is_welcome': is_welcome_list
                })
                website_condition_df.to_csv("./AllWebsiteCondition.csv", header=False, index=False, mode='a')
                html_list = []
                is_exist_list = []
                is_welcome_list = []
    except:
        print(str(start), ": Error Occured")
        start = start - 1
    finally:
        # Create website condition dataframe, and output
        website_condition_df = pd.DataFrame({
            'html_link': html_list,
            'is_exist': is_exist_list,
            'is_welcome': is_welcome_list
        })
        website_condition_df.to_csv("./AllWebsiteCondition.csv", header=False, index=False, mode='a')
    return start


if __name__ == '__main__':
    start = 903000
    end = 5066
    while True:
        start = check_all_websites(start, end)





