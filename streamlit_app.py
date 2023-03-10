import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.let_it_rain import rain
from whoosh import index
from whoosh.qparser import QueryParser, query

ix = index.open_dir("indexdir")


# Define a function to perform the search
def search(query_str, top_n=5):
    if query_str.strip() == "":
        return []
    # Open a searcher to search the index
    searcher = ix.searcher()

    # Define the query
    qp = QueryParser("prompt", ix.schema,termclass=query.Variations).parse(query_str)

    # Search the index and retrieve the top n results
    results = searcher.search(qp, limit=top_n)

    # Return the results
    return results


# Perform the search when the user clicks the search button
def display(results):
    for result in results:
        prompt = result["prompt"]
        image_url = result["images"].replace("[", "").replace("]", "")[1:-1]
        st.image(
            image_url,
            caption=prompt,
            use_column_width=True,
        )


def add_footer():
    """Add footer"""
    _, mid, _ = st.columns([1, 6, 1])
    with mid:
        add_vertical_space(2)
        st.markdown(
            """<span id="twitter-link"> ❤️ Built by <a href="https://twitter.com/saikatkrdey" target="_blank">Saikat Kumar Dey</a>""",
            unsafe_allow_html=True,
        )


def app():

    st.set_page_config(
        page_title="PromptQuest: search for midjourney prompt ideas",
        page_icon="🔍",
        layout="centered",
        initial_sidebar_state="collapsed",
        )

    _, mid, _ = st.columns([1, 6, 1])

    with mid:
        st.title("🔍 PromptQuest")
        st.markdown("Explore a world of midjourney prompt ideas!")
        st.markdown("<br>", unsafe_allow_html=True)

        query_str = st.text_input(
            label="search",
            key="query",
            placeholder="enter search query like 'cute dog' or 'landscape photography'",
            label_visibility="collapsed",
        )

        with st.sidebar:
            num_results = st.slider("Max results", 1, 20, step=1, value=5)

        if query_str.strip():
            results = search(query_str, num_results)
            if results:
                display(results)
            else:
                st.write("Sorry, no results found. Try another query (say, **cute dog**)!")
        add_footer()


if __name__ == "__main__":
    app()
