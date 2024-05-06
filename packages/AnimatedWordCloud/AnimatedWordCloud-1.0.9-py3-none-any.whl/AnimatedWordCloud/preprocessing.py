from ftfy import fix_encoding
import re
import numpy as np


# Function to split a column by a specified delimiter
def split_string(s):
    return pd.Series(str(s).split(':'))


# Function to rename all columns
def rename_columns(df, prefix='col_'):
    new_columns = [prefix + str(i) for i in range(len(df.columns))]
    return df.rename(columns=dict(zip(df.columns, new_columns)))


def replace_commas_after_integer(s):
    return re.sub(r'(\d+),', r'\1+', s)



def prep(text_prep: str,
         time: str,
         date_format: str,
         max_words: int,
         ngram: str,
         freq:str,
         stopwords: [],
         skip: []):

    import pandas as pd
    from arabica import arabica_freq

    global matrix
    if ngram == 1:
        cool=pd.DataFrame()
        cool['text']=text_prep
        text = text_prep
        text = text.apply(fix_encoding)
        cool['time']=time
        cool['time']=cool['time'].astype(str)
        cool['time'] = pd.to_datetime(cool['time'], errors= 'coerce')

        if freq == "Y":
            df = arabica_freq(text = text,
                              time = time,
                              date_format = date_format,
                              time_freq = 'Y',
                              max_words = max_words,
                              stopwords = stopwords,
                              skip = skip,
                              numbers = True,
                              lower_case = True)

            unigram = df[["period", "unigram"]]
            values = unigram["unigram"]
            period = unigram["period"]
            values = values.str.split(pat=',',expand=True)
            period = period.astype(str)
            test = pd.concat([period, values], axis=1)

            colnames = []

            for name in test.columns:
                name = str(name)
                name = "word" + name
                colnames.append(name)

            test.columns = colnames
            test["period"] = test["wordperiod"].rename("period", inplace = True)
            test=test.iloc[:,1:]
            l = test.melt(id_vars = "period")
            l = l[["period","value"]]
            l = test.melt(id_vars = "period")
            l = l[["period","value"]]
            l.columns = ["period", "word"]
            freq = l["word"].str.split(pat = ":", expand = True)
            freq.columns = ["word", "freq"]
            period = l["period"]
            freq.columns = ["word", "freq"]
            pokus = pd.concat([period, freq],axis=1)
            df = pokus.reset_index().pivot_table(values="freq", index="word", columns="period", aggfunc='mean')
            df.reset_index(inplace=True)
            df = df[df['word'] != 'NaT']
            df = df.fillna(0)
            df.rename(columns={df.columns[0]: ' '}, inplace=True)
            df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding)
            total_sum = df.iloc[1:, 1:].sum().sum()
            sliced_df = df.iloc[1:, 2:]
            total_sum = sliced_df.iloc[1:, 1:].sum().sum()

            print(total_sum)

            if total_sum > 30000:
                category = "top"
                scaling_factor = 0.5

            elif total_sum > 20000:
                category = "high"
                scaling_factor = 1


            elif total_sum > 10000:
                category = "medium"
                scaling_factor = 25


            elif total_sum > 5000:
                category = "low"
                scaling_factor = 50


            elif total_sum > 1500:
                category = "very_low"
                scaling_factor = 60

            else:
                category = "bottom"
                scaling_factor = 50

            print("Scaling applied:", category)

            # Define clipping limits for each category
            clipping_limits = {"top": 300, "high": 300, "medium": 300, "low": 300, "very_low": 300, "bottom": 300}

            # Apply scaling factor
            df.iloc[1:, 1:] = df.iloc[1:, 1:] * scaling_factor

            # Clip values
            clip_limit = clipping_limits[category]
            df.iloc[:, 1:] = np.clip(df.iloc[:, 1:].values, a_min=None, a_max=clip_limit)


            df.to_excel("df_final.xlsx")


        elif freq == "M":
            df = arabica_freq(text=text,
                              time=time,
                              date_format=date_format,
                              time_freq='M',
                              max_words=max_words,
                              stopwords=stopwords,
                              skip=skip,
                              numbers=True,
                              lower_case=True)

            unigram = df[["period", "unigram"]]
            values = unigram["unigram"]
            period = unigram["period"]
            values = values.str.split(pat=',', expand=True)
            period = period.astype(str)
            test = pd.concat([period, values], axis=1)

            colnames = []

            for name in test.columns:
                name = str(name)
                name = "word" + name
                colnames.append(name)

            test.columns = colnames
            test["period"] = test["wordperiod"].rename("period", inplace=True)
            test = test.dropna()
            test = test.iloc[:, 1:]
            l = test.melt(id_vars="period")
            l = l[["period", "value"]]
            l = test.melt(id_vars="period")
            l = l[["period", "value"]]
            l.columns = ["period", "word"]
            freq = l["word"].str.split(pat=":", expand=True)
            freq.columns = ["word", "freq"]
            print("freq")
            period = l["period"]
            freq.columns = ["word", "freq"]
            pokus = pd.concat([period, freq], axis=1)
            df = pokus.reset_index().pivot_table(values="freq", index="word", columns="period", aggfunc='mean')
            df.reset_index(inplace=True)
            df = df[df['word'] != 'NaT']
            df = df.fillna(0)
            df.rename(columns={df.columns[0]: ' '}, inplace=True)
            df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding)
            total_sum = df.iloc[1:, 1:].sum().sum()
            sliced_df = df.iloc[1:, 2:]
            sliced_df = sliced_df.applymap(lambda x: 500 if x > 500 else x)
            total_sum = sliced_df.iloc[1:, 1:].sum().sum()

            print(total_sum)

            if total_sum > 30000:
                category = "top"
                scaling_factor = 2

            elif total_sum > 20000:
                category = "high"
                scaling_factor = 3


            elif total_sum > 10000:
                category = "medium"
                scaling_factor = 25


            elif total_sum > 5000:
                category = "low"
                scaling_factor = 50


            elif total_sum > 1500:
                category = "very_low"
                scaling_factor = 60

            else:
                category = "bottom"
                scaling_factor = 50

            print("Scaling applied:", category)

            # Define clipping limits for each category
            clipping_limits = {"top": 300, "high": 300, "medium": 300, "low": 300, "very_low": 300, "bottom": 300}

            # Apply scaling factor
            df.iloc[1:, 1:] = df.iloc[1:, 1:] * scaling_factor

            # Clip values
            clip_limit = clipping_limits[category]
            df.iloc[:, 1:] = np.clip(df.iloc[:, 1:].values, a_min=None, a_max=clip_limit)


            df.to_excel("df_final.xlsx")


    elif ngram == 2:
        cool=pd.DataFrame()
        cool = cool.dropna()
        cool['text']=text_prep
        text = text_prep
        text = text.apply(fix_encoding)
        cool['time']=time
        cool['time']=cool['time'].astype(str)
        cool['time'] = pd.to_datetime(cool['time'], errors= 'coerce')

        if freq == "Y":
            df = arabica_freq(text = text,
                              time = time,
                              date_format = date_format,
                              time_freq = 'Y',
                              max_words = max_words,
                              stopwords = stopwords,
                              skip = skip,
                              numbers = True,
                              lower_case = True)

            unigram = df[["period", "bigram"]]
            period = pd.DataFrame(unigram["period"])
            unigram["bigram"] = unigram["bigram"].apply(replace_commas_after_integer)
            split_values  = unigram["bigram"].str.split(pat='+', expand=True)
            result = pd.merge(period, split_values, left_index=True, right_index=True)
            new_columns = ['period'] + [f'col_{col}' for col in result.columns[1:]]
            result.columns = new_columns
            finals = pd.wide_to_long(result, ["col_"], i="period", j="year")
            finals = finals.reset_index()
            finals = finals[['period','col_']]
            period_final = finals['period']
            frequencies = finals['col_'].str.split(':', expand=True)
            pokus = pd.merge(period_final, frequencies, left_index=True, right_index=True)
            pokus.columns = ['period',"word", "freq"]
            pokus['word'] = pokus['word'].str.replace(',', ' ')

            df = pokus.reset_index().pivot_table(values="freq", index="word", columns="period", aggfunc='mean')
            df.reset_index(inplace=True)
            df = df[df['word'] != 'NaT']
            df = df.fillna(0)
            df.rename(columns={df.columns[0]: ' '}, inplace=True)
            df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding)
            df = pd.DataFrame(df)
            df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
            total_sum = df.iloc[1:, 1:].sum().sum()
            print(total_sum)

            if total_sum > 30000:
                category = "top"
                scaling_factor = 0.8

            elif total_sum > 20000:
                category = "high"
                scaling_factor = 1


            elif total_sum > 10000:
                category = "medium"
                scaling_factor = 5


            elif total_sum > 5000:
                category = "low"
                scaling_factor = 15


            elif total_sum > 1500:
                category = "very_low"
                scaling_factor = 25

            else:
                category = "bottom"
                scaling_factor = 17



            print("Scaling applied:", category)

            # Define clipping limits for each category
            clipping_limits = {"top": 300, "high": 300, "medium": 300, "low": 300, "very_low": 300, "bottom": 300}

            # Apply scaling factor
            df.iloc[1:, 1:] = df.iloc[1:, 1:] * scaling_factor

            # Clip values
            clip_limit = clipping_limits[category]
            df.iloc[:, 1:] = np.clip(df.iloc[:, 1:].values, a_min=None, a_max=clip_limit)

            df.to_excel("df_final.xlsx")



        elif freq == "M":
            df = arabica_freq(text = text,
                                  time = time,
                                  date_format = date_format,
                                  time_freq = 'M',
                                  max_words = max_words,
                                  stopwords = stopwords,
                                  skip = skip,
                                  numbers = True,
                                  lower_case = True)

            unigram = df[["period", "bigram"]]
            period = pd.DataFrame(unigram["period"])
            unigram["bigram"] = unigram["bigram"].apply(replace_commas_after_integer)
            split_values  = unigram["bigram"].str.split(pat='+', expand=True)
            result = pd.merge(period, split_values, left_index=True, right_index=True)
            new_columns = ['period'] + [f'col_{col}' for col in result.columns[1:]]
            result.columns = new_columns
            finals = pd.wide_to_long(result, ["col_"], i="period", j="year")
            finals = finals.reset_index()
            finals = finals[['period','col_']]
            period_final = finals['period']
            frequencies = finals['col_'].str.split(':', expand=True)
            pokus = pd.merge(period_final, frequencies, left_index=True, right_index=True)
            pokus.columns = ['period',"word", "freq"]
            pokus['word'] = pokus['word'].str.replace(',', ' ')

            df = pokus.reset_index().pivot_table(values="freq", index="word", columns="period", aggfunc='mean')
            df.reset_index(inplace=True)
            df = df[df['word'] != 'NaT']
            df = df.fillna(0)
            df.rename(columns={df.columns[0]: ' '}, inplace=True)
            df.iloc[:,0] = df.iloc[:,0].apply(fix_encoding)
            total_sum = df.iloc[1:, 1:].sum().sum()
            
            print(total_sum)

            if total_sum > 30000:
                category = "top"
                scaling_factor = 2

            elif total_sum > 20000:
                category = "high"
                scaling_factor = 3


            elif total_sum > 10000:
                category = "medium"
                scaling_factor = 25


            elif total_sum > 5000:
                category = "low"
                scaling_factor = 50


            elif total_sum > 1500:
                category = "very_low"
                scaling_factor = 60

            else:
                category = "bottom"
                scaling_factor = 65



            print("Scaling applied:", category)

            # Define clipping limits for each category
            clipping_limits = {"top": 300, "high": 300, "medium": 300, "low": 300, "very_low": 300, "bottom": 300}

            # Apply scaling factor
            df.iloc[1:, 1:] = df.iloc[1:, 1:] * scaling_factor

            # Clip values
            clip_limit = clipping_limits[category]
            df.iloc[:, 1:] = np.clip(df.iloc[:, 1:].values, a_min=None, a_max=clip_limit)

            df.to_excel("df_final.xlsx")

    return df