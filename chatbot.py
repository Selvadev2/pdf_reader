import streamlit as st
import streamlit_authenticator as stauth
from utils import extract_pdf, text_splitter, embedding, embedding_openai, run_chain, run_chain_openai
# from dotenv import load_dotenv



# load_dotenv()


st.set_page_config(page_title= 'pdf_reader_chatbot', layout= "wide")
st.title('PDF Reader Chatbot')


st.markdown("""
<style>
.st-emotion-cache-15ecox0.ezrtsby0          
{
    visibility: hidden;
}
.styles_terminalButton__JBj5T
{
    visibility: hidden;
}          
</style>""", unsafe_allow_html= True)


names = ["software@scube.net.in","tender@scube.net.in", "ankit@scube.net.in","ceo@devharshinfotech.com","bhavin@scube.net.in"]
usernames = ["software", "tender","ankit","waman","bhavin"]
passwords = ["s12345", "t12345", "a12345","w12345","b1235"]  


hashed_passwords = stauth.Hasher(passwords).generate()


authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                    "pdf_chatbot_cookie", "some_signature_key")


name, authentication_status, username = authenticator.login("Login", "main")


if authentication_status:
    api_key_google = st.secrets["api_key_g"] # os.getenv("api_key_g")
    api_key_openai = st.secrets["api_key_o"] # os.getenv("api_key_o")



    st.markdown("""      
    ### Ask question related to
    - Penalties for Delay
    - Pre Qualification Criteria
    - Due date & Last offline tender submission date
    - Terms and Conditions of tender
    - Delivery Time and Place ,Packing details
    - Tender Fee EMD And Security Deposit
    - Financial Turnover Requirement for Bidders
    - Specifications
    - Required Documents for Bidders
    - Address
    - Specification
    - "Delivery Place,Contact Details,Contact Details,Pre-bid Meeting,Estimated Cost,
        IBA Required,Summarize:,Required Document,Sample Printing Details"
    - Tender Schedule
    """)

    # st.header('PDF READER CHATBOT FOR TENDERS')


    with st.sidebar:
        st.header("Menu:")

        language = st.selectbox('language', options= ['Select','English','Marathi', 'Hindi', 'Gujarati'])

        if language != 'Select':
            docs_file = st.file_uploader('upload pdf files:', accept_multiple_files= True, type = 'pdf',key = 'files')
        

        model_selection = st.radio("select the model:", options = ['gemini','chatgpt'])


        if st.button('submit', key= 'submit button') and docs_file:
            with st.spinner('processing........'):
                pdf = extract_pdf(docs_file, language)
                split = text_splitter(pdf)
                if model_selection == 'gemini':
                    embedding(split, api_key_google)
                else:
                    embedding_openai(split, api_key_openai)
                st.success('done.')

            
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    if prompt := st.chat_input("ask something"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role":"user", "content": prompt}) 

        if prompt:
            if model_selection == 'gemini':
                response = run_chain(user_question = prompt,  language=language, api_key_google = api_key_google)
            else:
                response = run_chain_openai(user_question = prompt, language=language, api_key_openai = api_key_openai)

        with st.chat_message("assistant"):
            st.markdown(response)
            
        st.session_state.messages.append({"role":"assistant", "content": response}) 
    authenticator.logout("Logout", "sidebar")
elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    st.warning("Please enter your username and password")

