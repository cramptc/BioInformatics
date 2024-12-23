import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def read_tsv_file(file_path):
    try:
        # Read the TSV file into a DataFrame
        data = pd.read_csv(file_path, sep='\t')
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    # Example usage:
    # Replace 'your_file.tsv' with the path to your TSV file
file_path = 'gencc-submissions.tsv'
df = read_tsv_file(file_path)
def get_entries(data, column_name):
    try:
        vc = data[column_name].value_counts(sort=False)
        unique_entries = data[column_name].unique()
        return unique_entries.tolist(), vc.tolist()
    except KeyError:
        print(f"Column '{column_name}' not found in the DataFrame.")
        return None

def q1():
    diseases, counts = get_entries(df, "disease_title")
    nkd = []
    for r,i in df.loc[:,['uuid','disease_title','classification_title']].iterrows():
        if not i[0].startswith("GENCC_"):
            continue
        if i[2] == "No Known Disease Relationship":
            nkd.append(i[1])

    for i in nkd:
        for j in range(len(diseases)):
            if i == diseases[j]:
                counts[j] -=1
                continue

    a = list(zip(diseases,counts))
    sorted_pairs = sorted(a, key=lambda x: x[1], reverse=True)
    # Get the top 10 name-value pairs with the highest values
    top_10_pairs = sorted_pairs[:10]

    print(top_10_pairs)

def q3():
    classes, counts = get_entries(df, "classification_title")
    a = list(zip(classes,counts))
    sorted_pairs = sorted(a, key=lambda x: x[1], reverse=True)
    print(sorted_pairs)

def q4():
    #pmid,doi,None
    counts = [0,0,0]
    nrows = 0
    for n,i in df.loc[:,['uuid','submitted_as_assertion_criteria_url']].iterrows():
        if not i[0].startswith("GENCC_"):
            continue
        if str(i[1]).startswith("PMID"):
            counts[0]+= 1
        elif str(i[1]) == "nan":
            counts[2]+=1
        else:
            counts[1]+=1
        nrows+=1
    print(counts)
    print(nrows)

def makemathsable(s,t):
    s = str(s)
    t = str(t)
    #if s[0] == '3':
     #   s[0]='2'
    s = s[:10]
    t = t[:10]
    s = pd.to_datetime(s,format="%d/%m/%Y")
                       #format="%Y/%m/%d",yearfirst=True)
    t = pd.to_datetime(t,format="%d/%m/%Y")
                       #format="%Y/%m/%d",yearfirst=True)
    #print(int((s-t).split(" ")[0]))
    delt = s-t
    if delt < datetime.timedelta(days=0):
        return t-s
    if delt > datetime.timedelta(days=10000):
        print(s)
        print(t)
        return datetime.timedelta(days=0)
    return delt

def ext():
    mdf = df.apply(lambda row: makemathsable(row['submitted_run_date'], row['submitted_as_date']), axis=1)
    print(mdf.describe())
    print(mdf.median())
    print(df['submitted_run_date'].median())
    print(df['submitted_as_date'].median())
    subdates, subcounts = get_entries(df, "submitted_as_date")
    subdates= [date_str[:4] for date_str in subdates]
    counts = []
    dates = []
    for i in range(len(subdates)):
        if subdates[i] in dates:
            counts[dates.index(subdates[i])]+=subcounts[i]
        else:
            dates.append(subdates[i])
            counts.append(subcounts[i])
    a = list(sorted(zip(dates,counts),key = lambda x: x[0]))[:-1]
    pda = []
    pc = []
    for i in a:
        pda.append(i[0])
        pc.append(i[1])
    print(sum(pc))
    fig,ax = plt.subplots()
    ax.plot(pda,pc, '-', label = 'Paper submissions')
    ax.set_xlabel('Year')

    rundates, runcounts = get_entries(df, "submitted_run_date")
    print(sum(runcounts))
    rundates= [date_str[:4] for date_str in rundates]
    rcounts = []
    rdates = []
    for i in range(len(rundates)):
        if rundates[i] in rdates:
            rcounts[rdates.index(rundates[i])]+=runcounts[i]
        else:
            rdates.append(rundates[i])
            rcounts.append(runcounts[i])
    ra = list(sorted(zip(rdates,rcounts),key = lambda x: x[0]))
    rpda = []
    rpc = []
    for i in ra:
        rpda.append(i[0])
        rpc.append(i[1])
    print(sum(rpc))
    # Set the y-axis label
    ax.set_ylabel('Number of Papers')
    ax.plot(rpda,rpc, '-', label = 'Papers run')

    # Add a legend
    ax.legend()
    plt.show()

ext()
