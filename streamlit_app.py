import pandas as pd
import streamlit as st
import altair as alt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse
import pickle
import plotly.express as px
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Arxiv Dashboard")

if st.toggle("Rest Of Program On"):
    df = pd.read_csv("reduced.csv")
    # if st.toggle("Paper Search"):
    #     st.write("Search Papers")
    #     # search for papers by title
    #     search = st.text_input("Search Papers by Title")
    #     # display the papers that match the search
    #     st.write(df[df["title"].str.contains(search,case=False)].head(20))
    
    # if st.toggle("Add Filters"):
    #     search = st.text_input("Must Include")
    #     df = df[df["title"].str.contains(search,case=False)]
        
    df["year"] = df["versions"].str[-20:-16]
    df["papers"] = 1
    
    # add_sidebar = st.sidebar.selectbox("Select Display",("Barchart","Exponential Fit","Top Authors","Abstract Lengths", "Paper Recommender"))
    # make a barplot of the year column based on freqeuncy of each year sorted by year
    # if add_sidebar == "Barchart":
    #     tab1, tab2 = st.tabs(["Default", "Grouped By Category"])
    #     #  barchart of paper frequency by year grouped by category
    #     chart = alt.Chart(df).mark_bar(opacity=0.7).encode(
    #         x='year:T',
    #         y='papers',
    #         color='categories:N',
    #     )
    #     with tab1:
    #         st.write("Paper Frequency by Year")
    #         st.bar_chart(df["year"].value_counts().sort_index())
    #     with tab2:
    #         st.write("Paper Frequncy by Year")
    #         st.altair_chart(chart, theme=None, use_container_width=True)
        
        
    # display the above plot in the streamlit app
    
    
    # fit papers per year to a function of form 2^(a(x-1992)) from 2000 to 2006
    from scipy.optimize import curve_fit
    import numpy as np
    import matplotlib.pyplot as plt
    
    
    def func(x, a,b):
        return b*2**(a*(x-1992))
    
    # print the fitted function
    
    
    # display the distribution of years in the year column in df
    papers_per_year = df['year'].value_counts().sort_index()
    # change index of papers_per_year to integers
    papers_per_year.index = papers_per_year.index.astype(int)
    
    popt, pcov = curve_fit(func, papers_per_year.index[:-2], papers_per_year[:-2])
    
    # if add_sidebar == "Exponential Fit":
    #     st.write("Doubling Time")
    #     # plot papers per year and the fitted function
    #     plt.scatter(papers_per_year.index[:-2], papers_per_year[:-2], label="y = b*2^(a(x-1992))"+"\na = " + str(popt[0]) + "\nb = " + str(popt[1]))
    #     plt.plot(papers_per_year.index[:-2], func(papers_per_year.index[:-2], *popt), 'r-', label='Fit')
    #     plt.scatter(papers_per_year.index[:-2],papers_per_year[:-2],color = "b", label = "Data")
    #     # add text to the legend of the graph
        
    #     print("y = b*2^(a(x-1992))")
    #     print("a = " + str(popt[0]))
    #     print("b = " + str(popt[1]))
        
    #     # add appropriate labels
    #     plt.xlabel('Year')
    #     plt.ylabel("Number of Papers Per Year")
    #     plt.title("Doubling Time is "+ str(1/popt[0]) + "years")
    #     # html figure
    #     plt.legend()
    #     st.pyplot()
    #     #plt.savefig('doubling.png')
    
    # if add_sidebar == "Top Authors":
    #     st.write("Top Authors")
    #     top_authors = df["submitter"].value_counts().sort_values(ascending=False).head(20)
    #     # sort top_authors by number of papers submitted
    #     top_authors_index = sorted(top_authors)
    #     # st.write(top_authors)
        
    #     st.bar_chart(top_authors)
    
    # if add_sidebar == "Abstract Lengths":
    #     # get the length of each abstract
    #     df["abstract_length"] = df["abstract"].str.len()
    #     # plot the distribution of abstract lengths
    #     st.write("Distribution of Abstract Lengths")
    #     plt.hist(df["abstract_length"],bins = 100)
    #     st.pyplot()
    #     #st.write(df["abstract_length"].describe())
    
    # if add_sidebar == "Paper Recommender":
    #  barchart of paper frequency by year grouped by category
    x = df.groupby("year").size().index
    y = df.groupby(["year"]).size().values
    x2 = df.groupby(["year","categories"]).size().index.get_level_values(0)
    y2 = df.groupby(["year","categories"]).size().values
    z2 = df.groupby(["year","categories"]).size().index.get_level_values(1)
    st.write("Paper Frequncy by Year")
    st.write("Doubling Time is "+ str(1/popt[0])[:4] + "years")
    fig = px.line(x = x, y = y)
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Papers", 
    )
    fig2 = px.line(x = x2, y = y2, color = z2)
    fig2.update_layout(
        xaxis_title="Year",
        yaxis_title="Papers",
        legend_title="Categories",
        legend=dict(font=dict(size = 1)),
        #showlegend=False
    )
    tab1, tab2 = st.tabs(["Default", "Grouped By Category"])
    tab1.plotly_chart(fig)
    tab2.plotly_chart(fig2)
    
    # if st.button("Train Model"):
    #     trainer= TfidfVectorizer(stop_words='english') 
    #     trainer.fit(df.iloc[:,11]) # need to save trainer as a pickle file
    #     temp = trainer.transform(df.iloc[:,11])# transformed papers #save as scipy sparsecsr matrix
    #     scipy.sparse.save_npz("/tmp/tester.npz", temp)
tester = scipy.sparse.load_npz("tester.npz")
#TFIDF = pd.DataFrame(tester.toarray(), columns=trainer.get_feature_names_out())
# search for papers by title
fileObj = open('data.obj', 'rb')
trainer = pickle.load(fileObj)
fileObj.close()

power_search = st.text_input("Search Papers by Title")
power_vector = trainer.transform([power_search])
# word_list = power_search.split(" ") 
# word_vector = trainer.transform(word_list) 
# st.write(word_vector)
# find the cosine similarity between the power search and the first 200 papers
cos_sim = cosine_similarity(power_vector, tester)
# find the index of the paper with the highest cosine similarity
matching_index = cos_sim.argmax()
# find the indexis of the top 10 papers with the highest cosine similarity
top_ten = cos_sim.argsort()[0][-10:]

# reverse the order of top_ten
top_ten = top_ten[::-1]
top_sim = cos_sim[0][top_ten]
#st.write(top_ten)
# st.write(matching_index)
# st.write(top_ten)
# st.write(len(df))
# find the title of the paper with the highest cosine similarity
matching_title = df.iloc[matching_index,4]
top_ten_titles = df.iloc[top_ten,4]
# change the index of top_ten_titles to the similarity scores
top_ten_titles.index = top_sim
top_ten_titles.index.name = "Similarity Score"
#st.write(matching_title)
st.write("Top Ten Results")
st.write(top_ten_titles)

    
